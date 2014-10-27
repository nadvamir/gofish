goFish.directive("menus", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/menus.html",
		scope: {},
		controller: function() {
			this.tab=0;

			this.setTab = function(value) {
				this.tab=value;
			};
		},
		controllerAs: "menusCtrl"
	};

} ]);