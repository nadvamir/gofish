goFish.factory("gameService", ["$http", function($http) {

	var game = {};

	return {
		getJSON: function(urlExtension) {
			$http.get("http://nadvamir.pythonanywhere.com/gofish/api/"+urlExtension).
				success(function(data) {
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
						game = data;
						console.dir(game);
						return game;
					};
				}).
				error(function() {
					alert("Error getting response from server.");
					return {};
				})
		}
	}

} ]);