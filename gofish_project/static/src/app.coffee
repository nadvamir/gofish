# --------------------------------------------------------------
# module declarations
# --------------------------------------------------------------
nav         = {}

home        = {}

game        = {}
topBar      = {}
gameActions = {}
infoArea    = {}
gameMap     = {}

caught      = {}

shop        = {}

trophies    = {}

# --------------------------------------------------------------
# navigation module
# --------------------------------------------------------------
# model
nav.LinkList = -> m.prop [{
        url: '/',
        title: 'Game',
    }, {
        url: '/shop',
        title: 'Shop',
    }, {
        url: '/trophies',
        title: 'Troph.',
    }
]

nav.controller = ->
    links: nav.LinkList()

nav.view = (ctrl) -> [
    ctrl.links().map((link) ->
        m('a', {href: link.url, config: m.route}, link.title))
]

m.module document.getElementById('nav'), nav

# --------------------------------------------------------------
# home module
# --------------------------------------------------------------
home.controller = ->
home.view = -> ['home']

# --------------------------------------------------------------
# game module
# --------------------------------------------------------------
# game model
class game.Game
    constructor: ->
        @totalTime = m.prop 480
        @timeLeft  = m.prop 405
        @money     = m.prop 151
        @valCaught = m.prop 15
        @showDepth = m.prop true
        @map       = m.prop [[5, 5, 7, 7, 9, 10, 8, 8, 7, 7, 6, 4, 6, 6, 6, 5, 5, 4, 3, 2]]
        @position  = m.prop 3
        @cues      = m.prop [[1.0, 4], [1.0, 4], [0.0, 4], [0.0, 4], [1.0, 0], [-1, 0], [-1, 0]]
        @caught    = m.prop []

game.vm = do ->
    init: ->
        # game object
        @game = new game.Game()

    act: (action) ->
        console.log 'send a request to server'
        console.log action

    getWaterClass: (i, j) ->
        if i < @game.map()[0][j]
            if j != @game.position() or @game.cues()[i][0] + 1 < 0.001
                'dark-water'
            else
                'light-water.fish-' + Math.round(@game.cues()[i][0])
        else
            'ground'

class game.controller
    constructor: ->
        game.vm.init()

game.view = (ctrl) -> [
    topBar.view()
    gameActions.view()
    infoArea.view()
    gameMap.view()
]

# --------------------------------------------------------------
# game:topBar module
# --------------------------------------------------------------
topBar.vm = do ->
    BAR_W = 400

    timeLeftW: ->
        g = game.vm.game
        g.timeLeft() / g.totalTime() * BAR_W

    timeFullW: ->
        BAR_W - @timeLeftW()

    valueCaught: ->
        game.vm.game.valCaught()

# time sub-view
topBar.timeSW = -> [
    m('i.fa.fa-clock-o')
    m('span.time-indicator.time-left',
        {style: {width: topBar.vm.timeLeftW()+'px'}}, m.trust '&nbsp;')
    m('span.time-indicator.time-full',
        {style: {width: topBar.vm.timeFullW()+'px'}}, m.trust '&nbsp;')
]

# money sub-view
topBar.moneySW = -> m('div.right.money-ind', [
    '+'
    m('span', {}, topBar.vm.valueCaught())
    ' coins'
])

topBar.view = (ctrl) -> m('div.top-bar', [
    topBar.timeSW(ctrl)
    m('a.right[href=/caught]', {config: m.route}, 'Caught')
    topBar.moneySW(ctrl)
])

# --------------------------------------------------------------
# game:gameActions module
# --------------------------------------------------------------
gameActions.actions = m.prop [{
        action : 'left',
        title  : 'move left',
    }, {
        action : 'right',
        title  : 'move right',
    }, {
        action : 'fish',
        title  : 'fish here',
    }, {
        action : 'end',
        title  : 'end game',
    }
]

gameActions.view = -> [
    m('div#game-actions', [
        gameActions.actions().map((action) ->
            m('a[href="#"]', {onclick: game.vm.act(action.action)},
                action.title))])
]

# --------------------------------------------------------------
# game:infoArea module
# --------------------------------------------------------------
infoArea.view = -> m('div#info-area', 'infoArea')

# --------------------------------------------------------------
# game:gameMap module
# --------------------------------------------------------------
# tile width
gameMap.TILE_W = 40

# a sub view for displaying boat
gameMap.boatSW = -> m('p', [m('span.boat', {style:
        {marginLeft: gameMap.TILE_W * game.vm.game.position() + 'px'}})
])

# a sub-view for displaying actual water depth map
gameMap.waterSW = ->
    if game.vm.game.showDepth()
        [m('p', [m('span.' + game.vm.getWaterClass(i, j)) for j in [0...20]]) for i in [0...10]]
    else
        [m('span.dark-water') for i in [0...20]]

gameMap.view = -> m('div#game-map', [
    gameMap.boatSW()
    gameMap.waterSW()
])

# --------------------------------------------------------------
# caught module
# --------------------------------------------------------------
caught.controller = ->
caught.view = -> ['caught']

# --------------------------------------------------------------
# shop module
# --------------------------------------------------------------
shop.controller = ->
shop.view = -> ['shop']

# --------------------------------------------------------------
# trophies module
# --------------------------------------------------------------
trophies.controller = ->
trophies.view = -> ['trophies']

# --------------------------------------------------------------
# routing
# --------------------------------------------------------------
m.route.mode = 'hash'
m.route document.getElementById('page'), '/game', {
    '/'         : home,
    '/game'     : game,
    '/caught'   : caught,
    '/shop'     : shop,
    '/trophies' : trophies
}

