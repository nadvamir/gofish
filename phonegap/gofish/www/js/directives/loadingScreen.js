goFish.directive("loadingScreen", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/loadingScreen.html",
		scope: {
			message: "="
		},
		controller: function($scope, GameService) {

		},
		controllerAs: "loadingScreenCtrl"
	};

} ]);
