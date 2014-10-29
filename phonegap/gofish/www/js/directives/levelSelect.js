goFish.directive("levelSelect", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/levelSelect.html",
		scope: {},
		controller: function($http, $scope, GameService) {
			$scope.game = {};

			GameService.updateGame();

			$scope.$on("gameUpdated", function() {
				$scope.game = GameService.getGame();
			});
		},
		controllerAs: "lsCtrl"
	};

} ]);