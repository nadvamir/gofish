goFish.directive("shopBait", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shopBait.html",
		scope: {
			name: "=",
			bait: "="
		},
		controller: function($scope, GameService) {
			var update = function() {
				$scope.owned = (GameService.getGame().player.modifiers[$scope.name] !== undefined);
				if (GameService.getGame().player) {
					$scope.player = GameService.getGame().player;
				}
			};

			$scope.buy = function() {
				// Get current money
				var playerMoney = $scope.player.money;
				// Attempt purchase
				if (playerMoney < $scope.bait.price) {
					alert("You cannot afford this item.");
				}
				else if (!$scope.owned) {
					GameService.buyBait($scope.name);
				}
			};

			$scope.$on("gameUpdated", function() {
				update();
			});

			// Initialisation
			$scope.owned = false;
			$scope.player={};
			update();
		},
		controllerAs: "shopBaitCtrl"
	};

} ]);
