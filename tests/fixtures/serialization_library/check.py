"""Exercise installed modules in a fresh process with no search-path overrides."""
import ctypes
import importlib
from pathlib import Path
import pickle
import sys

# This script lives outside the installed prefix; emulate an installed package
# on sys.path, without adding any native library search-path override.
sys.path.insert(0, str(Path.cwd()))

if sys.argv[1] == 'legacy':
    from consumer_a import HolderA
    archive = Path(sys.argv[2])
    value = HolderA()
    value.deserialize(archive.read_text())
    assert value.get() == 42
    assert value.serialize() == archive.read_text()
    archive.write_text(value.serialize())
else:
    unrelated = None
    if sys.argv[2] == 'static':
        name = ('unrelated.dll' if sys.platform == 'win32' else
                'libunrelated.dylib' if sys.platform == 'darwin' else 'libunrelated.so')
        unrelated = ctypes.CDLL(str(Path.cwd() / name), mode=ctypes.RTLD_GLOBAL)
        assert unrelated.unrelated_roundtrip() == 0
    classes = []
    for name in sys.argv[1].split(','):
        module = importlib.import_module(name)
        classes.append(getattr(module, 'HolderA' if name == 'consumer_a' else 'HolderB'))
        assert classes[-1](1).get() == 42
    # Exercise both consumers only after all requested libraries have loaded.
    for cls in classes:
        for kind, expected in ((1, 42), (2, 7), (3, 3)):
            value = cls(kind)
            serialized = value.serialize()
            assert ('example::' in serialized or 'examplePairintdouble' in serialized)
            assert 'unrelated::' not in serialized
            assert pickle.loads(pickle.dumps(value)).get() == expected
            for other in classes:
                restored = other()
                restored.deserialize(serialized)
                assert restored.get() == expected
            try:
                cls().deserialize('not an archive')
            except RuntimeError:
                pass
            else:
                raise AssertionError('invalid archives must raise RuntimeError')
    if unrelated:
        assert unrelated.unrelated_roundtrip() == 0
