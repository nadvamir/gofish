goFish.directive("game", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/game.html",
		scope: {},
		controller: function($http, $scope, GameService) {
			// Functions
			$scope.updateLevel = function() {
				$scope.level = GameService.getCurrentLevel();
			};

			// Initialisation
			$scope.updateLevel();

			// Watch for level updates
			$scope.$on("levelStarted", function() {
				$scope.updateLevel();
			});
		},
		controllerAs: "gameCtrl"
	};

} ]);