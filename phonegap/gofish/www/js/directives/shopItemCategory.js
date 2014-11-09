goFish.directive("shopItemCategory", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shopItemCategory.html",
		scope: {
			category: "=",
			items: "=",
			key: "@"
		},
		controller: function($scope) {

		},
		controllerAs: "shopItemCategoryCtrl"
	};

} ]);