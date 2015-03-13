goFish.directive("game", ["$rootScope", function($rootScope){

	return {
		restrict: "E",
		templateUrl: "./partials/game.html",
		scope: {},
		controller: function($http, $scope, GameService) {
			// Functions
			$scope.updateLevel = function() {
				$scope.level = GameService.getCurrentLevel();
				$scope.player = GameService.getGame().player;
				if ($scope.player && $scope.player.updates && $scope.player.updates.boats) {
					$scope.boat = (scope.player.updates.boats).replace(/\s/g, '');
				} else {
					$scope.boat = "DefaultBoat"
				}
				if ($scope.level && $scope.level.level) {
					$scope.levelName = ($scope.level.level.name).replace(/\s/g, '');
				}
			};

			$scope.fish = function() {
				GameService.fish();
			};

			$scope.end = function() {
				GameService.endLevel();
			};

			// Initialisation
			$scope.updateLevel();
			$scope.showResults = false;

			// Watch for level updates
			$scope.$on("levelStarted", function() {
				$scope.updateLevel();
				// Set appropriate background image after variables have been initialised
				$('.level-screen').css('background-image', "url('./img/levels/"+$scope.levelName+"/background.png')");
				$('.above-water').css('background-image', "url('./img/levels/"+$scope.levelName+"/landscape.png')");
			});
			$scope.$on("levelUpdated", function() {
				$scope.updateLevel();
			});
			$scope.$on("levelEnded", function() {
				$scope.showResults = true;
			});
			$scope.$on("exitResults", function() {
				$scope.showResults = false;
			});
		},
		controllerAs: "gameCtrl"
	};

} ]);
