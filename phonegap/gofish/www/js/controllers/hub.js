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

	$scope.$on("gameUpdated", function() {
		$scope.initialLoading = false;
	});

	$scope.$on("levelStarted", function() {
		$scope.playing = true;
		$scope.menus = false;
		$scope.splash = false;
	});

	$scope.$on("exitResults", function() {
		$scope.playing = false;
		$scope.menus = true;
	});

	$scope.$on("showLoadingBanner", function() {
		$scope.showLoading = true;
	});

	$scope.$on("hideLoadingBanner", function() {
		$scope.showLoading = false;
	});

	// Initialisation
	$scope.splash = true;
	$scope.menus = false;
	$scope.playing = false;
	$scope.showLoading = false;
	$scope.initialLoading = true;
	// Use timeout as occasionally $scope.$on in certain directives wouldn't be given enough time to setup
	$timeout(function() {$scope.updateState();}, 100);
	

} ]);
