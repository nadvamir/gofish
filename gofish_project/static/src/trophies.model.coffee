# --------------------------------------------------------------
# trophies module
# --------------------------------------------------------------
# namespace
trophies = {}

# a model for storing a list of trophies
# which for now will all be fish
trophies.Trophies = Array

# view-model
trophies.vm = do ->
    init: ->
        get('/v2/player').then (r) =>
            @player = new game.Player(r.player)

        @userT = new trophies.Trophies()
        @gameT = new trophies.Trophies()

        get('/v2/trophies').then (r) =>
            for t in r.userTrophies
                @userT.push new game.Fish t
            for t in r.gameTrophies
                @gameT.push new game.Fish t
            @userT.sort (a, b) -> a.name() > b.name()
            @gameT.sort (a, b) -> a.name() > b.name()

