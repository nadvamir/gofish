goFish.controller("hubController", ["$scope", "GameService", function($scope, GameService) {

	GameService.updateGame();

	$scope.updatePlaying = function() {
		$scope.playing = (GameService.getCurrentLevel().level !== undefined);
	};

	$scope.updateState = function() {
		$scope.updatePlaying();
		GameService.updateGame();
	};

	$scope.$on("levelStarted", function() {
		level =  GameService.getCurrentLevel();
		$scope.updatePlaying();
	});

	$scope.updateState();

} ]);