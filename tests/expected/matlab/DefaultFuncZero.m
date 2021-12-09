function varargout = DefaultFuncZero(varargin)
      if length(varargin) == 5 && isa(varargin{1},'numeric') && isa(varargin{2},'numeric') && isa(varargin{3},'double') && isa(varargin{4},'logical') && isa(varargin{5},'logical')
        functions_wrapper(18, varargin{:});
      elseif length(varargin) == 4 && isa(varargin{1},'numeric') && isa(varargin{2},'numeric') && isa(varargin{3},'double') && isa(varargin{4},'logical')
        functions_wrapper(19, varargin{:});
      elseif length(varargin) == 4 && isa(varargin{1},'numeric') && isa(varargin{2},'numeric') && isa(varargin{3},'logical') && isa(varargin{4},'logical')
        functions_wrapper(20, varargin{:});
      elseif length(varargin) == 3 && isa(varargin{1},'numeric') && isa(varargin{2},'numeric') && isa(varargin{3},'logical')
        functions_wrapper(21, varargin{:});
      elseif length(varargin) == 4 && isa(varargin{1},'numeric') && isa(varargin{2},'double') && isa(varargin{3},'logical') && isa(varargin{4},'logical')
        functions_wrapper(22, varargin{:});
      elseif length(varargin) == 3 && isa(varargin{1},'numeric') && isa(varargin{2},'double') && isa(varargin{3},'logical')
        functions_wrapper(23, varargin{:});
      elseif length(varargin) == 3 && isa(varargin{1},'numeric') && isa(varargin{2},'logical') && isa(varargin{3},'logical')
        functions_wrapper(24, varargin{:});
      elseif length(varargin) == 2 && isa(varargin{1},'numeric') && isa(varargin{2},'logical')
        functions_wrapper(25, varargin{:});
      else
        error('Arguments do not match any overload of function DefaultFuncZero');
      end
