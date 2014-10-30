goFish.directive("shopItemCategory", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shopItemCategory.html",
		scope: {
			category: "=",
			items: "="
		},
		controller: function($scope) {

		},
		controllerAs: "shopItemCategoryCtrl"
	};

} ]);