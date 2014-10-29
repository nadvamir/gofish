goFish.factory("GameService", ["$http", "$rootScope", function($http, $rootScope) {

	var API_URL = "http://nadvamir.pythonanywhere.com/gofish/api/";
	var game = {};
	var currentLevel = {};

	var getJSON = function(urlExtension) {
		$http.get(API_URL+urlExtension).
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
			$http.get(API_URL+"getgame/").
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
		},
		startLevel: function(levelIndex) {
			$http.get(API_URL+"start/"+levelIndex+"/").
				success(function(data) {
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
						currentLevel = data;
						$rootScope.$broadcast("levelStarted");
					};
				}).
				error(function() {
					alert("Error getting response from server.");
					return {};
				})
		},
		getCurrentLevel: function() {
			return currentLevel;
		}
	}

} ]);