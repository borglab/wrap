"""Required CI integration suite; opt in locally with GTWRAP_TEST_SERIALIZATION=1."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/fixtures/serialization_library'


def check_public_exports(actual, expected, platform, linkage):
    """Require every bridge and reject exports outside the reviewed exception."""
    allowed = set()
    if platform == 'win32' and linkage == 'static':
        # Precompiled MSVC objects carry dllexport directives that our DLL's
        # source-level visibility settings cannot suppress. Match exact names,
        # never a Boost namespace pattern or exports discovered during this run.
        allowed = {line for line in
                   (FIXTURE / 'windows_static_boost_exports.txt').read_text().splitlines()
                   if line and not line.startswith('#')}
    missing = expected - actual
    unexpected = actual - expected - allowed
    if missing or unexpected:
        raise AssertionError(f'Missing bridge exports: {sorted(missing)}\n'
                             f'Unexpected exports: {sorted(unexpected)}')


class TestExportPolicy(unittest.TestCase):
    def test_exception_is_limited_to_windows_static(self):
        bridge = {'gtwrap_test_save', 'gtwrap_test_load'}
        actual = bridge | {'?lock@singleton_module@serialization@boost@@QEAAXXZ'}
        check_public_exports(actual, bridge, 'win32', 'static')
        for platform, linkage in (('win32', 'shared'), ('linux', 'static'),
                                  ('darwin', 'static')):
            with self.subTest(platform=platform, linkage=linkage):
                with self.assertRaisesRegex(AssertionError, 'Unexpected exports: \\[.+'):
                    check_public_exports(actual, bridge, platform, linkage)

    def test_unknown_boost_helpers_are_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'Unexpected exports: \\[.+'):
            check_public_exports({'?unknown_helper@serialization@boost@@'},
                                 set(), 'win32', 'static')

    def test_exception_cannot_hide_missing_bridges(self):
        with self.assertRaisesRegex(AssertionError, 'Missing bridge exports: \\[.+'):
            check_public_exports(set(), {'gtwrap_test_load'}, 'win32', 'static')


def run(args, **kwargs):
    result = subprocess.run([str(a) for a in args], capture_output=True,
                            text=True, **kwargs)
    if result.returncode:
        raise AssertionError(f'{args}\n{result.stdout}\n{result.stderr}')
    return result.stdout


@unittest.skipUnless(os.environ.get('GTWRAP_TEST_SERIALIZATION') == '1',
                     'enable the required serialization integration suite explicitly')
class TestSerializationRuntime(unittest.TestCase):
    def test_runtime_and_installation(self):
        # CI selects each linkage in its own job; local runs can exercise both.
        linkages = os.environ.get('GTWRAP_TEST_BOOST_LINKAGE', 'static,shared').split(',')
        for linkage in linkages:
            with self.subTest(linkage=linkage), tempfile.TemporaryDirectory() as temporary:
                self.exercise(Path(temporary), linkage)

    def exercise(self, directory, linkage):
        self.assertIn(linkage, ('static', 'shared'))
        source = directory / 'source'
        shutil.copytree(FIXTURE, source)
        wrap = directory / 'wrap'
        wrap.mkdir()
        for name in ('gtwrap', 'cmake', 'scripts', 'templates', 'pybind11'):
            shutil.copytree(ROOT / name, wrap / name,
                            ignore=shutil.ignore_patterns('__pycache__', '.git'))
        for name in ('CMakeLists.txt', 'matlab.h'):
            shutil.copyfile(ROOT / name, wrap / name)
        env = dict(os.environ)
        env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env['PATH']
        cmake_args = ['-DCMAKE_BUILD_TYPE=Release', '-DPYBIND11_FINDPYTHON=ON',
                      f'-DPython_EXECUTABLE={Path(sys.executable).as_posix()}',
                      f'-DWRAP_PYTHON_VERSION={sys.version_info.major}.{sys.version_info.minor}',
                      f'-DBoost_USE_STATIC_LIBS={"ON" if linkage == "static" else "OFF"}']
        # Accept a caller-provided Boost/toolchain installation, never download
        # dependencies or silently change linkage from inside a test.
        for variable in ('CMAKE_PREFIX_PATH', 'CMAKE_TOOLCHAIN_FILE', 'VCPKG_TARGET_TRIPLET'):
            if os.environ.get(variable):
                value = os.environ[variable].replace('\\', '/')
                cmake_args.append(f'-D{variable}={value}')

        for installed in (False, True):
            label = 'installed' if installed else 'source'
            build = directory / (label + '-build')
            prefix = directory / (label + '-prefix')
            arguments = list(cmake_args)
            if installed:
                wrap_build = directory / 'wrap-build'
                wrap_prefix = directory / 'wrap-prefix'
                run(['cmake', '-S', wrap, '-B', wrap_build,
                     f'-DCMAKE_INSTALL_PREFIX={wrap_prefix.as_posix()}', *cmake_args], env=env)
                run(['cmake', '--install', wrap_build, '--config', 'Release'], env=env)
                config = next(wrap_prefix.rglob('gtwrapConfig.cmake'))
                arguments += ['-DWRAP_INSTALLED=ON',
                              f'-Dgtwrap_DIR={config.parent.as_posix()}']
                implementation = wrap_prefix / 'lib/gtwrap/gtwrap/serialization.py'
            else:
                arguments += [f'-DWRAP_ROOT={wrap.as_posix()}']
                implementation = wrap / 'gtwrap/serialization.py'
            run(['cmake', '-S', source, '-B', build,
                 f'-DCMAKE_INSTALL_PREFIX={prefix.as_posix()}', *arguments], env=env)
            run(['cmake', '--build', build, '--config', 'Release', '-j', '6'], env=env)
            generated = build / 'gtwrap_serialization/registry'
            manifest = json.loads((generated / 'registry.json').read_text())
            self.assertEqual(len(manifest['entries']), 5)
            for consumer in ('consumer_a', 'consumer_b'):
                content = (build / f'{consumer}.cpp').read_text()
                self.assertNotIn('BOOST_CLASS_EXPORT(', content)
                self.assertNotIn('boost::archive', content)
                self.assertNotIn('gtsam::', content)

            # A no-op build is stable; edits to either source of truth regenerate
            # the manifest and all consumers before they compile.
            generated_source = generated / 'registry.cpp'
            before = generated_source.stat().st_mtime_ns
            run(['cmake', '--build', build, '--config', 'Release', '-j', '6'], env=env)
            self.assertEqual(before, generated_source.stat().st_mtime_ns)
            for dependency in (source / 'types.i', implementation):
                time.sleep(1.05)
                dependency.touch()
                run(['cmake', '--build', build, '--config', 'Release', '-j', '6'], env=env)
                after = generated_source.stat().st_mtime_ns
                self.assertGreater(after, before)
                before = after

            run(['cmake', '--install', build, '--config', 'Release'], env=env)
            runtime = prefix / 'runtime'
            # Ensure installed tests cannot accidentally find build products.
            build.rename(directory / (label + '-hidden-build'))
            clean_env = {k: v for k, v in env.items()
                         if k not in ('PYTHONPATH', 'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH')}
            for order in ('consumer_a', 'consumer_b',
                          'consumer_a,consumer_b', 'consumer_b,consumer_a'):
                run([sys.executable, source / 'check.py', order, linkage],
                    cwd=runtime, env=clean_env)

            # Compare with the historical full-export owner in a fresh process.
            legacy = runtime / ('legacy.exe' if os.name == 'nt' else 'legacy')
            archive = runtime / 'archive.txt'
            run([legacy, 'save', archive], env=clean_env)
            run([sys.executable, source / 'check.py', 'legacy', archive],
                cwd=runtime, env=clean_env)
            run([legacy, 'load', archive], env=clean_env)
            symbols = {entry[operation] for entry in manifest['entries']
                       for operation in ('save', 'load')}
            if sys.platform == 'darwin':
                exported = run(['nm', '-gU', runtime / 'libregistry.dylib'])
                actual = {line.split()[-1].removeprefix('_') for line in exported.splitlines() if line.strip()}
            elif os.name == 'nt':
                exported = run(['dumpbin', '/EXPORTS', runtime / 'registry.dll'])
                actual = set(re.findall(r'^\s+\d+\s+[0-9A-F]+\s+[0-9A-F]+\s+(\S+)', exported, re.M))
            else:
                exported = run(['nm', '-D', '--defined-only', runtime / 'libregistry.so'])
                actual = {line.split()[-1] for line in exported.splitlines() if line.strip()}
            # Report export-policy failures without skipping installed-package
            # runtime validation. Both consumption modes must still be exercised.
            with self.subTest(consumption=label, check='public exports'):
                check_public_exports(actual, symbols, sys.platform, linkage)
