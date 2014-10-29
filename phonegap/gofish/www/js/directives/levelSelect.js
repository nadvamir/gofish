goFish.directive("levelSelect", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/levelSelect.html",
		scope: {},
		controller: function($http) {
			
			this.game = {};
			var controller = this;

			this.updateGame = function() {
				$http.get("http://nadvamir.pythonanywhere.com/gofish/api/getgame/").
					success(function(data, scope) {
						if(data.error) {
							alert(data.error);
						}
						else {
							controller.game = data;
						};
					}).
					error(function() {
						alert("Error getting game.");
					})
			};

			this.updateGame();

		},
		controllerAs: "lsCtrl"
	};

} ]);