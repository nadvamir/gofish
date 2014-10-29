goFish.factory("gameService", ["$http", function($http) {

	var getJSON = function(urlExtension) {
		$http.get("http://nadvamir.pythonanywhere.com/gofish/api/"+urlExtension).
			success(function(data) {
				if(data.error) {
					alert(data.error);
					return {};
				}
				else {
					return data;
				};
			}).
			error(function() {
				alert("Error getting response from server.");
				return {};
			})
	};

	return {
		getJSON: function(urlExtension) {
			return getJSON(urlExtension);
		},
		getGame: function() {
			return getJSON('getgame/');
		}
	}

} ]);