goFish.directive("splash", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/splash.html",
		scope: {},
		controller: function($scope, $rootScope) {
			$scope.play = function() {
				$rootScope.$broadcast("splashPlay");
			};
		},
		controllerAs: "splashCtrl"
	};

} ]);