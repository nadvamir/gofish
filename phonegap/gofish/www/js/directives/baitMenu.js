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
			}

			$scope.getEquipped = function() {
				for (var bait in $scope.player.modifiers) {
					if ($scope.player.modifiers[bait] == true) {
						return bait;
					}
				}
				return null;
			}

			$scope.ownsBait = function() {
				if (!$scope.player || !$scope.player.modifiers) return false;
			    for (var prop in $scope.player.modifiers) {
			        if ($scope.player.modifiers.hasOwnProperty(prop))
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
					$scope.equippedBait = null;
				};
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
