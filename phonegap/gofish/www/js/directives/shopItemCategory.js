goFish.directive("shopItemCategory", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shopItemCategory.html",
		scope: {
			category: "=",
			items: "=",
			playerData: "="
		},
		controller: function($scope) {

		},
		controllerAs: "shopItemCategoryCtrl"
	};

} ]);