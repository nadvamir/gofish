goFish.directive("level", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/level.html",
		scope: {
			levelData: "="
		},
		controller: function($scope, GameService) {
			$scope.selectLevel = function() {
				var playerMoney = GameService.getGame().player.money;
				if (playerMoney < $scope.levelData.cost) {
					alert("You don't have enough money to fish in "+$scope.levelData.name);
					GameService.startLevel($scope.levelData["index"]);
					GameService.updateGame();
				}
				else {
					GameService.startLevel($scope.levelData["index"]);
					GameService.updateGame();
				}
			};


			// Remove spaces for css image selection
			$scope.levelNoSpace = ($scope.levelData.name).replace(/\s/g, '');
		},
		controllerAs: "levelCtrl"
	};

} ]);
