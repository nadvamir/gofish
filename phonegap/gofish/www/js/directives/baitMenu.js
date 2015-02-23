goFish.directive("baitMenu", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/baitMenu.html",
		scope: {
			player: "="
		},
		controller: function($rootScope, $scope, GameService) {

			$scope.confirm = function() {
				GameService.changeBait($scope.selected);
				$rootScope.$broadcast("hideBaitMenu");
				$(".list-item").removeClass("selected");
				$scope.selected = "";
			}

			$scope.cancel = function() {
				$rootScope.$broadcast("hideBaitMenu");
				$(".list-item").removeClass("selected");
				$scope.selected = "";
			}

			$scope.select = function(bait) {
				console.log("selected");
				$(".list-item").removeClass("selected");
				$("#listItem-"+bait).addClass("selected");
				$scope.selected = bait;
			}

			$scope.selected = "";

		},
		controllerAs: "baitMenuCtrl"
	};

} ]);
