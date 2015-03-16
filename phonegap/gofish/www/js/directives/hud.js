goFish.directive("hud", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/hud.html",
		scope: {},
		controller: function($rootScope, $scope, $timeout, GameService) {

			$scope.startupHUD = function() {
				$scope.player = GameService.getGame().player;
				$scope.equippedBait = $scope.getEquipped();
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
				$scope.waitCount = 0;
				$scope.moveSuccess = true;
				$scope.showHint = true;
			}

			$scope.getTimePercentage = function() {
				return ($scope.timeSpent/$scope.totalTime*100);
			}

			$scope.showBaitMenu = function() {
				if (!$scope.fishing) $scope.baitVisible = true;
			}

			$scope.moveLeft = function() {
				if (!$scope.fishing) GameService.move("left");
			};

			$scope.moveRight = function() {
				if (!$scope.fishing) GameService.move("right");
			};

			$scope.fish = function() {
				if (!$scope.fishing) GameService.fish();
			};

			$scope.endLevel = function() {
				if (!$scope.fishing) GameService.endLevel();
			};

			$scope.getEquipped = function() {
				for (var bait in $scope.player.modifiers) {
					if ($scope.player.modifiers[bait] == true) {
						return bait;
					}
				}
				return "default";
			}

			// Initialisation
			$scope.reset();

			// Listen for updates
			$scope.$on("levelStarted", function() {
				$scope.startupHUD();
			});

			$scope.$on("levelUpdated", function() {
				$scope.showHint = false;
				$scope.startupHUD();
				$rootScope.$broadcast("fishing");
				$scope.fishing = true;
				$scope.caught = GameService.getCaught();
				$scope.caughtMsg = ".";
				$timeout(handleCaughtMsg, 500);
			});

			var handleCaughtMsg = function () {
				if ($scope.waitCount >= 2) {
					if ($scope.caught == null) {
						$scope.caughtMsg = "Nothing's biting...";
					} else {
						$scope.caughtMsg = $scope.caught.weight+"kg "+$scope.caught.name+" +£"+$scope.caught.value;
					}
					$scope.waitCount = 0;
					$scope.fishing = false;
					$rootScope.$broadcast("fishingEnded");
				} else {
					$scope.caughtMsg += " .";
					$scope.waitCount += 1;
					$timeout(handleCaughtMsg, 750);
				}
			}

			$scope.$on("moved", function() {
				$scope.startupHUD();
				$scope.caughtMsg = "";
			});

			$scope.$on("moveFail", function() {
				GameService.endLevel();
			});

			$scope.$on("gameUpdated", function() {
				$scope.player = GameService.getGame().player;
				$scope.equippedBait = $scope.getEquipped();
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
