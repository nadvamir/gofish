goFish.controller("hubController", ["$scope", "$timeout", "GameService", function($scope, $timeout, GameService) {

	$scope.updatePlaying = function() {
		$scope.playing = (GameService.getCurrentLevel().level !== undefined);
		if (!$scope.playing) {
			$scope.splash = true;
		}
	};
	
	$scope.updateState = function() {
		$scope.updatePlaying();
		GameService.updateGame();
	};

	$scope.play = function() {
		$scope.splash = false;
		$scope.menus = true;
	};

	// Handling view switching
	$scope.$on("splashPlay", function() {
		$scope.play();
	});

	$scope.$on("levelStarted", function() {
		$scope.playing = true;
		$scope.menus = false;
		$scope.splash = false;
		$scope.showresults = false;
	});

	$scope.$on("levelEnded", function() {
		$scope.playing = false;
		GameService.updateGame();
		$scope.showResults = true;
	});

	$scope.$on("exitResults", function() {
		$scope.showResults = false;
		$scope.menus = true;
	});

	// Initialisation
	$scope.splash = false;
	$scope.menus = false;
	$scope.playing = false;
	$scope.showResults = false;
	// Use timeout as occasionally $scope.$on in certain directives wouldn't be given enough time to setup
	$timeout(function() {$scope.updateState();}, 100);
	

} ]);
