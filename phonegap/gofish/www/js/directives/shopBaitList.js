goFish.directive("shopBaitList", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shopBaitList.html",
		scope: {},
		controller: function($scope, GameService) {
			var update = function() {
				if (GameService.getGame().modifiers) {
					$scope.all = GameService.getGame().modifiers;
				}
			};

			$scope.$on("gameUpdated", function() {
				update();
			});

			// Initialisation
			$scope.all = {};
			update();
		},
		controllerAs: "shopBaitListCtrl"
	};

} ]);
