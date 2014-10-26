goFish.service("gameService", ["$scope", "$http", function($scope, $http) {

	var game = {};

	this.updateGame = function() {
		$http.get("http://nadvamir.pythonanywhere.com/gofish/api/getgame/").
			success(function(data) {
				if(data.error) {
					alert(data.error);
				}
				else {
					game = data;
				};
			}).
			error(function() {
				alert("Error getting game.");
			})
	};

	this.getGame = function() {
		return game;
	};

} ]);