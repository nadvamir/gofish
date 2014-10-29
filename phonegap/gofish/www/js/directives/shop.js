goFish.directive("shop", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shop.html",
		scope: {},
		controller: function($http, $scope, GameService) {
			$scope.game = {};

			GameService.updateGame();

			$scope.$on("gameUpdated", function() {
				$scope.game = GameService.getGame();
			});
		},
		controllerAs: "shopCtrl"
	};

} ]);