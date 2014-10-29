goFish.factory("GameService", ["$http", "$rootScope", function($http, $rootScope) {

	var game = {};

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
		updateGame: function() {
			$http.get("http://nadvamir.pythonanywhere.com/gofish/api/getgame/").
				success(function(data) {
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
						game = data;
						$rootScope.$broadcast("gameUpdated");
					};
				}).
				error(function() {
					alert("Error getting response from server.");
					return {};
				})
		},
		getGame: function() {
			return game;
		}
	}

} ]);