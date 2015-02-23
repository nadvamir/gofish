goFish.directive("baitMenu", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/baitMenu.html",
		scope: {},
		controller: function($rootScope, $scope, GameService) {

			$scope.confirm = function() {

				$rootScope.$broadcast("hideBaitMenu");
			}

			$scope.cancel = function() {
				$rootScope.$broadcast("hideBaitMenu");
			}

		},
		controllerAs: "baitMenuCtrl"
	};

} ]);
