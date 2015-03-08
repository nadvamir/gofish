goFish.directive("fishingSpotDepth", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/fishingSpotDepth.html",
		scope: {
			depth: "=",
			level: "=",
			cues: "="
		},
		controller: function($scope, GameService) {
			
		},
		controllerAs: "fishingSpotDepthCtrl"
	};

} ]);
