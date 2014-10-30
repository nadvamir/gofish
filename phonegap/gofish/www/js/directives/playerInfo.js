goFish.directive("playerInfo", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/playerInfo.html",
		scope: {},
		controller: function($scope, GameService) {
			$scope.player = {};

			$scope.updatePlayer = function() {
				if (GameService.getGame().player) {
					$scope.player = GameService.getGame().player;
				}
			};

			$scope.updatePlayer();

			$scope.$on("gameUpdated", function() {
				$scope.updatePlayer();
			});
		},
		controllerAs: "playerInfoCtrl"
	};

} ]);