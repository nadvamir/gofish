goFish.directive("shopUpgrade", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shopUpgrade.html",
		scope: {
			category: "=",
			items: "="
		},
		controller: function($scope, GameService) {
			var getCurrentUpgrade = function() {
				$scope.current = null;
				var currentName = ($scope.player.updates[$scope.category]);
				var check;
				for (var i = 0; i < $scope.all.length; i++) {
					check = $scope.all[i];
					// Found current position in upgrade tree
					if (currentName === check.name) {
						$scope.current = check;
						break;
					}
				}
			};

			var getNextUpgrade = function() {
				if (!$scope.current) {
					$scope.next = $scope.all[0];
				}
				else {
					var check;
					for (var i = 0; i < $scope.all.length; i++) {
						check = $scope.all[i];
						// Found current position in upgrade tree
						if ($scope.current.name === check.name) {
							// If last upgrade is owned, can't upgrade further
							if (i === ($scope.all.length - 1)) {
								$scope.next = null;
							}
							// Else set next to appropriate upgrade
							else {
								$scope.next = $scope.all[i+1];		
							}
						}
					}
				}
			};

			var update = function() {
				if (GameService.getGame().player) {
					$scope.player = GameService.getGame().player;
				}
				if (GameService.getGame().updates[$scope.category]) {
					$scope.all = GameService.getGame().updates[$scope.category];
				}
				getCurrentUpgrade();
				getNextUpgrade();
				
				// Remove spaces for css image selection
				if($scope.next) {
					$scope.nextNoSpace = ($scope.next.name).replace(/\s/g, '');	
				}
			}

			$scope.buy = function() {
				// Get current money
				var playerMoney = $scope.player.money;
				// Attempt purchase
				if (playerMoney < $scope.next.price) {
					alert("You cannot afford this item.");
				}
				else if ($scope.next != null) {
					GameService.buyUpgrade($scope.category);
				}
			};

			$scope.$on("gameUpdated", function() {
				update();
			});

			// Initialisation
			update();

		},
		controllerAs: "shopUpgradeCtrl"
	};

} ]);
