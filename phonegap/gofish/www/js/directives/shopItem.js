goFish.directive("shopItem", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shopItem.html",
		scope: {
			shopItemData: "="
		},
		controller: function($scope, GameService) {
			// TODO handle possible error where .player.money not found
			this.buy = function() {
				var playerMoney = GameService.getGame().player.money;
				if (playerMoney < $scope.shopItemData.price) {
					alert("You cannot afford this item.");
				}
				else {
					alert("You have purchased "+$scope.shopItemData.name);
				}
			};
		},
		controllerAs: "shopItemCtrl"
	};

} ]);