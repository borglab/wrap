function varargout = setPose(varargin)
      if length(varargin) == 1 && isa(varargin{1},'gtsam.Pose3')
        functions_wrapper(25, varargin{:});
      elseif length(varargin) == 0
        functions_wrapper(26, varargin{:});
      else
        error('Arguments do not match any overload of function setPose');
      end
