goFish.directive("baitMenu", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/baitMenu.html",
		scope: {
			player: "="
		},
		controller: function($rootScope, $scope, GameService) {

			$scope.confirm = function() {

				$rootScope.$broadcast("hideBaitMenu");
			}

			$scope.cancel = function() {
				console.dir($scope.player);
				$rootScope.$broadcast("hideBaitMenu");
			}

		},
		controllerAs: "baitMenuCtrl"
	};

} ]);
