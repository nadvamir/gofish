goFish.directive("hud", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/hud.html",
		scope: {},
		controller: function($scope, GameService) {

			$scope.updateHUD = function() {
				$scope.player = GameService.getGame().player;

				var currentLevel = GameService.getCurrentLevel();
				if (currentLevel.level) {
					if (currentLevel.level.time) {
						$scope.timeSpent = currentLevel.level.time;
					}
					if (currentLevel.level.totalTime) {
						$scope.totalTime = currentLevel.level.totalTime;
					}
				}
				if (currentLevel.money) {
					$scope.money = currentLevel.money;
				}
				// Check if time is up and end level when necessary
				if ($scope.timeSpent >= $scope.totalTime) {
					console.log("HUD ending level");
					GameService.endLevel();
				}
			};

			$scope.reset = function() {	
				$scope.player = GameService.getGame().player;
				$scope.totalTime = 480;
				$scope.timeSpent = 0;
				$scope.money = 0;
				$scope.baitVisible = false;
			}

			$scope.getTimePercentage = function() {
				return ($scope.timeSpent/$scope.totalTime*100);
			}

			$scope.showBaitMenu = function() {
				$scope.baitVisible = true;
			}

			// Initialisation
			$scope.reset();

			// Listen for updates
			$scope.$on("levelStarted", function() {
				$scope.updateHUD();
			});

			$scope.$on("levelUpdated", function() {
				$scope.updateHUD();
			});

			$scope.$on("baitUpdated", function() {
				$scope.player = GameService.getGame().player;
			});

			$scope.$on("hideBaitMenu", function() {
				$scope.baitVisible = false;
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
