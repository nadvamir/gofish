goFish.directive("loadingBanner", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/loadingBanner.html",
		scope: {
			message: "="
		},
		controller: function($scope, GameService) {

		},
		controllerAs: "loadingBannerCtrl"
	};

} ]);
