goFish.directive("level", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/level.html",
		scope: {
			levelData: "="
		},
		controller: function($scope, GameService) {
			this.selectLevel = function() {
				var playerMoney = GameService.getGame().player.money;
				if (playerMoney < $scope.levelData.cost) {
					alert("You don't have enough money to fish in "+$scope.levelData.name);
				}
				else {
					alert("You have chosen to fish in "+$scope.levelData.name);
					GameService.updateGame();
				}
			};
		},
		controllerAs: "levelCtrl"
	};

} ]);