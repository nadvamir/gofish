goFish.directive("fishingSpotDepth", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/fishingSpotDepth.html",
		scope: {
			depth: "="
		},
		controller: function($scope, GameService) {

			$scope.fish = function() {
				GameService.fish();
			};
			
		},
		controllerAs: "fishingSpotDepthCtrl"
	};

} ]);
