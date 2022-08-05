function varargout = DefaultFuncVector(varargin)
      if length(varargin) == 2 && isa(varargin{1},'std.vectornumeric') && isa(varargin{2},'std.vectorchar')
        functions_wrapper(22, varargin{:});
      elseif length(varargin) == 1 && isa(varargin{1},'std.vectornumeric')
        functions_wrapper(23, varargin{:});
      elseif length(varargin) == 0
        functions_wrapper(24, varargin{:});
      else
        error('Arguments do not match any overload of function DefaultFuncVector');
      end
