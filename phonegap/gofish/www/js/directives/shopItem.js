goFish.directive("shopItem", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shopItem.html",
		scope: {
			shopItemData: "="
		},
		controller: function($scope, GameService) {
			$scope.updatePlayer = function() {
				if (GameService.getGame().player) {
					$scope.player = GameService.getGame().player;
				}
			}

			$scope.buy = function() {
				// Get current money
				var playerMoney = $scope.player.money;
				// Attempt purchase
				if (playerMoney < $scope.shopItemData.price) {
					alert("You cannot afford this item.");
				}
				else {
					alert("You have purchased "+$scope.shopItemData.name);
				}
			};

			$scope.$on("gameUpdated", function() {
				$scope.updatePlayer();
			});

			// Initialisation
			$scope.updatePlayer();
		},
		controllerAs: "shopItemCtrl"
	};

} ]);