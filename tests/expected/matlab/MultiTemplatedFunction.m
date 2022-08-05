function varargout = MultiTemplatedFunction(varargin)
      if length(varargin) == 2 && isa(varargin{1},'char') && isa(varargin{2},'numeric')
        varargout{1} = functions_wrapper(8, varargin{:});
      elseif length(varargin) == 2 && isa(varargin{1},'double') && isa(varargin{2},'numeric')
        varargout{1} = functions_wrapper(9, varargin{:});
      else
        error('Arguments do not match any overload of function MultiTemplatedFunction');
      end
