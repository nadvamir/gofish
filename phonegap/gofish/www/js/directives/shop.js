goFish.directive("shop", [function(){

	return {
		restrict: "E",
		templateUrl: "./partials/shop.html",
		scope: {},
		controller: function($http) {
			
			//TODO: use gameService to get data

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
		controllerAs: "shopCtrl"
	};

} ]);