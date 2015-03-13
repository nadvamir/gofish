goFish.directive("baitMenu", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/baitMenu.html",
		scope: {},
		controller: function($rootScope, $scope, GameService) {

			$scope.exit = function() {
				$rootScope.$broadcast("hideBaitMenu");
			}

			$scope.select = function(bait) {
				if (bait != $scope.equippedBait) {
					GameService.changeBait(bait);
				}
				console.dir($scope.player);
			}

			$scope.getEquipped = function() {
				for (var bait in $scope.player.modifiers) {
					if ($scope.player.modifiers[bait] == true) {
						console.log("FOUND EQUIPPED: "+bait);
						return bait;
					}
				}
				return null;
			}

			$scope.ownsBait = function() {
				if (!$scope.player || !$scope.player.modifiers) return false;
			    for(var prop in $scope.player.modifiers) {
			        if($scope.player.modifiers.hasOwnProperty(prop))
			            return true;
			    }
			    return false;
			}

			var update = function() {
				$scope.player = GameService.getGame().player;
				$scope.selected = "";
				if ($scope.player) {
					$scope.equippedBait = $scope.getEquipped();
				} else {
					console.log("PLAYER DOESN'T EXIST");
					$scope.equippedBait = null;
				}
				console.log("EQUIPPED: "+$scope.equippedBait);

			};

			// Initialisation

			update();

			// Watch for events

			$scope.$on("gameUpdated", function() {
				update();
			});

		},
		controllerAs: "baitMenuCtrl"
	};

} ]);
