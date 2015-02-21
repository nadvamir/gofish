# --------------------------------------------------------------
# shop module
# --------------------------------------------------------------
# namespace
shop = {}

# class for all types of updates
class shop.Update
    constructor: (b, type) ->
        @name = m.prop b.name
        @cost = m.prop b.cost
        @perk = m.prop b.perk
        @type = m.prop type

# model to store all updates
shop.Updates = Array

# view-model
shop.vm = do ->
    init: ->
        get('/v2/player').then (r) =>
            @player = new game.Player(r.player)

        @boats = new shop.Updates()
        @lines = new shop.Updates()
        @cues  = new shop.Updates()

        get('/v2/shop').then (r) =>
            for u in r.boats
                @boats.push new shop.Update u, 'boats'
            for u in r.lines
                @lines.push new shop.Update u, 'lines'
            for u in r.cues
                @cues.push new shop.Update u, 'cues'

    currentBoat: -> shop.vm.boats[shop.vm.player.boat() + 1]
    updateBoat: -> shop.vm.boats[shop.vm.player.boat() + 2]
    currentLine: -> shop.vm.lines[shop.vm.player.line() + 1]
    updateLine: -> shop.vm.lines[shop.vm.player.line() + 2]
    currentCue: -> shop.vm.cues[shop.vm.player.cue() + 1]
    updateCue: -> shop.vm.cues[shop.vm.player.cue() + 2]

    update: ->
        get('/update/' + @type()).then -> m.route '/shop'

