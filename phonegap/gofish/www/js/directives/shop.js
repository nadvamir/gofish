goFish.directive("shop", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shop.html",
		scope: {},
		controller: function($http, $scope, GameService) {
			$scope.game = {};
			$scope.updateGame = function() {
				$scope.game = GameService.getGame();
			};

			$scope.$on("gameUpdated", function() {
				$scope.updateGame();
			});
		},
		controllerAs: "shopCtrl"
	};

} ]);
