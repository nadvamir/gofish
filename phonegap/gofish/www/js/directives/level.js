goFish.directive("level", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/level.html",
		scope: {
			levelData: "="
		},
		controller: function($scope) {
			this.selectLevel = function() {
				alert("You have chosen to fish in "+$scope.levelData.name);
			};
		},
		controllerAs: "levelCtrl"
	};

} ]);