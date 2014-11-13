goFish.directive("results", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/results.html",
		scope: {},
		controller: function($rootScope, $scope, GameService) {
			// Functions
			$scope.exit = function() {
				$rootScope.$broadcast("exitResults");
			};

			// Initialisation
			$scope.results = {};

			// Watch for level updates
			$scope.$on("levelEnded", function() {
				$scope.results = GameService.getResults();
			});
		},
		controllerAs: "resultsCtrl"
	};

} ]);