goFish.factory("GameService", ["$http", "$rootScope", function($http, $rootScope) {

	var API_URL = "http://nadvamir.pythonanywhere.com/gofish/api/";
	var game = {};
	var currentLevel = {};
	var results = {};

	var getJSON = function(urlExtension) {
		$http.get(API_URL+urlExtension).
			success(function(data) {
				if(data.error) {
					alert(data.error);
					return {};
				}
				else {
					console.dir(data);
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
		move: function(direction) {
			$http.get(API_URL+"action/move/"+direction+"/").
				success(function(data) {
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
		            	currentLevel.level.position = data.position;
		            	currentLevel.level.time = data.time;
		            	currentLevel.cues = data.cues;
						$rootScope.$broadcast("levelUpdated");
					};
				}).
				error(function() {
					alert("Error getting response from server.");
					return {};
				})
		},
		fish: function() {
			$http.get(API_URL+"action/catchall/1/").
				success(function(data) {
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
		            	currentLevel.level.time = data.time;
		            	currentLevel.cues = data.cues;
		            	var fish = data.fishList[0];
		            	if (fish) {
			                currentLevel.caught.push(fish);
			                currentLevel.money = (currentLevel.money + fish.value);
			            }
						$rootScope.$broadcast("levelUpdated");
					};
				}).
				error(function() {
					alert("Error getting response from server.");
					return {};
				})
		},
		endLevel: function() {
			$http.get(API_URL+"end/").
				success(function(data) {
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
		            	results["earned"] = data.earned;
		            	results["total"] = (data.money + data.earned);
		            	results["caught"] = currentLevel.caught;
		            	currentLevel = {};
						$rootScope.$broadcast("levelEnded");
					};
				}).
				error(function() {
					alert("Error getting response from server.");
					return {};
				})
		},
		getCurrentLevel: function() {
			return currentLevel;
		},
		getResults: function() {
			return results;
		}
	}

} ]);