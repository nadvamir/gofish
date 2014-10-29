goFish.directive("shopItem", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shopItem.html",
		scope: {
			shopItemData: "=",
			playerData: "="
		},
		controller: function($scope) {
			this.buy = function() {
				console.dir($scope.playerData);
				if ($scope.playerData.money < $scope.shopItemData.price) {
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