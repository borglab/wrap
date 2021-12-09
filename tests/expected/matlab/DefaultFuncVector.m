function varargout = DefaultFuncVector(varargin)
      if length(varargin) == 2 && isa(varargin{1},'std.vectornumeric') && isa(varargin{2},'std.vectorchar')
        functions_wrapper(26, varargin{:});
      elseif length(varargin) == 1 && isa(varargin{1},'std.vectornumeric')
        functions_wrapper(27, varargin{:});
      elseif length(varargin) == 1 && isa(varargin{1},'std.vectorchar')
        functions_wrapper(28, varargin{:});
      elseif length(varargin) == 0
        functions_wrapper(29, varargin{:});
      else
        error('Arguments do not match any overload of function DefaultFuncVector');
      end
