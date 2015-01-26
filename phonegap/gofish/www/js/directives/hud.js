goFish.directive("hud", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/hud.html",
		scope: {},
		controller: function($scope, GameService) {

			$scope.updatePlayer = function() {
				if (GameService.getGame().player) {
					$scope.player = GameService.getGame().player;
				}
			};

			$scope.updateTime = function() {
				var currentLevel = GameService.getCurrentLevel();
				if (currentLevel.level && currentLevel.level.time) {
					$scope.timeSpent = currentLevel.level.time;
				}
				if (currentLevel.level && currentLevel.level.totalTime) {
					$scope.totalTime = currentLevel.level.totalTime;
				}
			};

			$scope.reset = function() {	
				$scope.player = {};
				$scope.totalTime = 480;
				$scope.timeSpent = 0;
			}

			$scope.getTimePercentage = function() {
				return ($scope.timeSpent/$scope.totalTime*100);
			}

			// Initialisation
			$scope.reset();

			// Listen for updates
			$scope.$on("gameUpdated", function() {
				$scope.updatePlayer();
			});

			$scope.$on("levelStarted", function() {
				$scope.updateTime();
			});

			$scope.$on("levelUpdated", function() {
				$scope.updateTime();
			});

			// Ensure a clean HUD on next level
			// Necessary?
			$scope.$on("levelEnded", function() {
				$scope.reset();
			});
		},
		controllerAs: "hudCtrl"
	};

} ]);
