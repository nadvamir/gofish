goFish.directive("levelSelect", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/levelSelect.html",
		scope: {},
		controller: function($http, $scope, GameService) {
			$scope.updateGame = function() {
				$scope.game = GameService.getGame();
				if ($scope.game.levels) {
					angular.forEach($scope.game.levels, function(level, index) {
						level["index"] = index;
					});
				}
			};

			$scope.game = {};

			$scope.$on("gameUpdated", function() {
				$scope.updateGame();
			});
		},
		controllerAs: "lsCtrl"
	};

} ]);