goFish.controller("hubController", ["$scope", "GameService", function($scope, GameService) {

	GameService.updateGame();

	$scope.updatePlaying = function() {
		$scope.playing = (GameService.getCurrentLevel().level !== undefined);
	};
	
	$scope.updateState = function() {
		$scope.updatePlaying();
		GameService.updateGame();
	};

	// Handling view switching
	$scope.$on("levelStarted", function() {
		level =  GameService.getCurrentLevel();
		$scope.updatePlaying();
		$scope.showResults = false;
	});

	$scope.$on("levelEnded", function() {
		$scope.updateState();
		$scope.showResults = true;
	});

	$scope.$on("exitResults", function() {
		$scope.showResults = false;
	});

	// Initialisation
	$scope.updateState();

} ]);
