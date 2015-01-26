goFish.directive("fishingSpot", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/fishingSpot.html",
		scope: {},
		controller: function($scope, GameService) {
			// Functions
			$scope.updateFishingSpot = function() {
				var currentLevel = GameService.getCurrentLevel();
				if (currentLevel.level && (currentLevel.level.position >= 0) && currentLevel.level.map && currentLevel.cues) {
					$scope.position = currentLevel.level.position;
					$scope.map = currentLevel.level.map[0];
					$scope.cues = currentLevel.cues;
					// Generate an array to traverse with ng-repeat to draw depth levels
					var depth = $scope.map[$scope.position];
					$scope.currentDepth = [];
					for (var i = 1; i <= depth; i++) {
						$scope.currentDepth.push(i);
					};
					/*
					console.log("position");
					console.log($scope.position);
					console.log("depth");
					console.log(depth);
					*/
				}
				else {
					console.log("ERROR finding necessary information for rendering fishing spot");
				}
			};

			// Listen for level updates
			$scope.$on("levelStarted", function() {
				$scope.updateFishingSpot();
			});
			$scope.$on("levelUpdated", function() {
				$scope.updateFishingSpot();
			});

			// Initialisation
			$scope.map = null;
			$scope.position = 0;
			$scope.cues = null;
			$scope.currentDepth = [];
		},
		controllerAs: "fishingSpotCtrl"
	};

} ]);
