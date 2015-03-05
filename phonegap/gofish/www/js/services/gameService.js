goFish.factory("GameService", ["$http", "$rootScope", function($http, $rootScope) {

	var API_URL = "http://sjakobsen.pythonanywhere.com/gofish/api/";
	var thisService = this;
	var game = {};
	var currentLevel = {};
	var results = {};
	var caught = null;

	var errorMessage = function() {
		alert("Error getting response from server.");
		return {};
	};

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
				return errorMessage();
			})
	};

	updateGame = function() {
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
				return errorMessage();
			})
	};

	return {
		getJSON: function(urlExtension) {
			return getJSON(urlExtension);
		},
		updateGame: function() {
			return updateGame();
		},
		getGame: function() {
			return game;
		},
		startLevel: function(levelIndex) {
			$rootScope.$broadcast("showLoadingBanner");
			$http.get(API_URL+"start/"+levelIndex+"/").
				success(function(data) {
					$rootScope.$broadcast("hideLoadingBanner");
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
					$rootScope.$broadcast("hideLoadingBanner");
					return errorMessage();
				})
		},
		getCurrentLevel: function() {
			return currentLevel;
		},
		move: function(direction) {
			$rootScope.$broadcast("showLoadingBanner");
			$http.get(API_URL+"action/move/"+direction+"/").
				success(function(data) {
					$rootScope.$broadcast("hideLoadingBanner");
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
		            	currentLevel.level.position = data.position;
		            	currentLevel.level.time = data.time;
		            	currentLevel.cues = data.cues;
						$rootScope.$broadcast("levelUpdated");
						$rootScope.$broadcast("moved");
					};
				}).
				error(function() {
					$rootScope.$broadcast("hideLoadingBanner");
					return errorMessage();
				})
		},
		fish: function() {
			$rootScope.$broadcast("showLoadingBanner");
			$http.get(API_URL+"action/catchall/1/").
				success(function(data) {
					$rootScope.$broadcast("hideLoadingBanner");
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
		            	currentLevel.level.time = data.time;
		            	currentLevel.cues = data.cues;
		            	caught = data.fishList[0];
		            	if (caught) {
			                currentLevel.caught.push(caught);
			                currentLevel.money = (currentLevel.money + caught.value);
			            }
						$rootScope.$broadcast("levelUpdated");
					};
				}).
				error(function() {
					$rootScope.$broadcast("hideLoadingBanner");
					return errorMessage();
				})
		},
		getCaught: function() {
			return caught;
		},
		endLevel: function() {
			$rootScope.$broadcast("showLoadingBanner");
			$http.get(API_URL+"end/").
				success(function(data) {
					$rootScope.$broadcast("hideLoadingBanner");
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
		            	results["earned"] = data.earned;
		            	results["total"] = (data.money + data.earned);
		            	results["caught"] = currentLevel.caught;
		            	currentLevel = {};
		            	caught = null;
						$rootScope.$broadcast("levelEnded");
					};
				}).
				error(function() {
					$rootScope.$broadcast("hideLoadingBanner");
					return errorMessage();
				})
		},
		getResults: function() {
			return results;
		},
		buyUpgrade: function(category) {
			$rootScope.$broadcast("showLoadingBanner");
			$http.get(API_URL+"update/"+category+"/").
				success(function(data) {
					$rootScope.$broadcast("hideLoadingBanner");
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
						updateGame();
					};
				}).
				error(function() {
					$rootScope.$broadcast("hideLoadingBanner");
					return errorMessage();
				})
		},
		buyBait: function(name) {
			$rootScope.$broadcast("showLoadingBanner");
			$http.get(API_URL+"buy/"+name+"/").
				success(function(data) {
					$rootScope.$broadcast("hideLoadingBanner");
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
						updateGame();
					};
				}).
				error(function() {
					$rootScope.$broadcast("hideLoadingBanner");
					return errorMessage();
				})
		},
		changeBait: function(name) {
			$rootScope.$broadcast("showLoadingBanner");
			$http.get(API_URL+"choose/"+name+"/").
				success(function(data) {
					$rootScope.$broadcast("hideLoadingBanner");
					if(data.error) {
						alert(data.error);
						return {};
					}
					else {
						console.log("BAIT CHANGED");
						console.dir(data);
						updateGame();
						// game.player = data ???
						// $rootScope.broadcast("baitChanged");
					};
				}).
				error(function() {
					$rootScope.$broadcast("hideLoadingBanner");
					return errorMessage();
				})
		}
	}

} ]);
