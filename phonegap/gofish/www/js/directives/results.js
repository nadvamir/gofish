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

			var parseResults = function() {
				for (var i = 0; i < $scope.results.caught.length; i++) {
					var caught = $scope.results.caught[i];
					// Fish exists in parsed
					if ($scope.parsed[caught.name]) {
						$scope.parsed[caught.name].weight += caught.weight;
						$scope.parsed[caught.name].value += caught.value;
						// Check if max needs to be updated
						if ($scope.max[caught.name].value < caught.value) {
							$scope.max[caught.name].weight = caught.weight;
							$scope.max[caught.name].length = caught.length;
							$scope.max[caught.name].value = caught.value;
						}
					} else {
						$scope.parsed[caught.name] = {"weight":caught.weight, "value":caught.value};
						$scope.max[caught.name] = {"weight":caught.weight, "value":caught.value};
					}
				};
			};

			// Initialisation
			$scope.results = {};
			$scope.parsed = {};
			$scope.max = {};

			// Watch for level updates
			$scope.$on("levelEnded", function() {
				$scope.results = GameService.getResults();
				parseResults();
			});
		},
		controllerAs: "resultsCtrl"
	};

} ]);