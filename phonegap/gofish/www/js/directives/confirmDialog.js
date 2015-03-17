goFish.directive("confirmDialog", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/confirmDialog.html",
		scope: {
			message: "=",
			confirm: "&"
		},
		controller: function($rootScope, $scope, GameService) {

			// Functions
			$scope.exit = function() {
				$rootScope.$broadcast("exitDialog");
			};

		},
		controllerAs: "confirmDialogCtrl"
	};

} ]);