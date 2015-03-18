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
					// alert("You don't have enough money to fish in "+$scope.levelData.name);
					if ($scope.levelData["index"] == 0) {
						GameService.startLevel($scope.levelData["index"]);
						GameService.updateGame();
					} else {
						$scope.levelError = true;
					}
				}
				else {
					GameService.startLevel($scope.levelData["index"]);
					GameService.updateGame();
				}
			};

			$scope.close = function() {
				$scope.levelError = false;
			};


			// Remove spaces for css image selection
			$scope.levelNoSpace = ($scope.levelData.name).replace(/\s/g, '');
		},
		controllerAs: "levelCtrl"
	};

} ]);
