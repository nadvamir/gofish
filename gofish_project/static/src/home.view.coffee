# view
home.view = -> [
    topBar('Choose a location:', game.vm.player.money())
    list.view(home.vm.levels, home.vm.getItemView)
]

