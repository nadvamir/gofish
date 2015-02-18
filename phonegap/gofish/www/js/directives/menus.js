goFish.directive("menus", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/menus.html",
		scope: {},
		controller: function($scope, GameService) {

			$scope.setTab = function(value) {
				if ($scope.tab != value) {
					$scope.tab=value;
					var levelStyleCpy = $scope.levelStyle;
					$scope.levelStyle = $scope.shopStyle;
					$scope.shopStyle = levelStyleCpy;
				}
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
			$scope.levelStyle = {color:'white'};
			$scope.shopStyle = {color:'black'};

			$scope.updatePlayer();
		},
		controllerAs: "menusCtrl"
	};

} ]);