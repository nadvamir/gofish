// TODO
// Break level select out into it's own directive, using this controller (removing this file)

goFish.controller("LevelSelectController", ["$scope", "$http", function($scope, $http){

	this.updateGame = function() {
		$http.get("http://nadvamir.pythonanywhere.com/gofish/api/getgame/").
			success(function(data) {
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


	this.game = {};
	var controller = this;
	this.updateGame();

} ]);