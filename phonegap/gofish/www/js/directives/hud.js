goFish.directive("hud", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/hud.html",
		scope: {},
		controller: function($scope, GameService) {

			$scope.startupHUD = function() {
				$scope.player = GameService.getGame().player;
				$scope.level = GameService.getCurrentLevel();

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
				$scope.caught = null;
				$scope.caughtMsg = "";
			}

			$scope.getTimePercentage = function() {
				return ($scope.timeSpent/$scope.totalTime*100);
			}

			$scope.showBaitMenu = function() {
				$scope.baitVisible = true;
			}

			$scope.moveLeft = function() {
				GameService.move("left");
			};

			$scope.moveRight = function() {
				GameService.move("right");
			};

			// Initialisation
			$scope.reset();

			// Listen for updates
			$scope.$on("levelStarted", function() {
				$scope.startupHUD();
			});

			$scope.$on("levelUpdated", function() {
				$scope.startupHUD();
				$scope.caught = GameService.getCaught();
				if ($scope.caught == null) {
					$scope.caughtMsg = "Nothing's biting...";
				} else {
					$scope.caughtMsg = $scope.caught.weight+"kg "+$scope.caught.name+" +£"+$scope.caught.value;
				}
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
