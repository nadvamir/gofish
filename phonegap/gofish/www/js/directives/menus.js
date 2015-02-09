goFish.directive("menus", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/menus.html",
		scope: {},
		controller: function($scope, GameService) {

			$scope.setTab = function(value) {
				$scope.tab=value;
			};

			$scope.updatePlayer = function() {
				if (GameService.getGame().player) {
					$scope.player = GameService.getGame().player;
				}
			};

			$scope.$on("gameUpdated", function() {
				$scope.updatePlayer();
			});

			// Initialisation
			$scope.player = {};
			$scope.tab = 0;

			$scope.updatePlayer();
		},
		controllerAs: "menusCtrl"
	};

} ]);