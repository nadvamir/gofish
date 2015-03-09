goFish.directive("fishingSpotDepth", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/fishingSpotDepth.html",
		scope: {
			depth: "=",
			level: "=",
			cues: "="
		},
		controller: function($scope, GameService) {

			var processCues = function() {
				$scope.cue = null;
				if ($scope.cues[0] > 5) {
					$scope.cue = 6;
				} else if ($scope.cues[0] > 0) {
					$scope.cue = $scope.cues[0];
				}
			};

			$scope.$watch('$scope.cues', function() {
       			processCues();
   			});

   			processCues();
		},
		controllerAs: "fishingSpotDepthCtrl"
	};

} ]);
