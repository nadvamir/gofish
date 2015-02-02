# --------------------------------------------------------------
# module declarations
# --------------------------------------------------------------
nav         = {}

game        = {}
ingame      = {}
topBar      = {}
gameActions = {}
infoArea    = {}
gameMap     = {}

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
# game module
# --------------------------------------------------------------
# game model
class game.Game
    constructor: ->
        @totalTime = m.prop 480
        @timeLeft  = m.prop 405
        @money     = m.prop 151
        @valCaught = m.prop 15
        @location  = 7
        @showDepth = true
        @map       = []
        @caught    = []

# view model to switch between game modes
game.vm = do ->
    init: ->
        # game object
        @game = new game.Game()
        # state
        @state = m.prop 'ingame'

class game.controller
    constructor: ->
        game.vm.init()

    showCaught: ->
        console.log 'caught asked'

    act: (action) ->
        console.log 'send a request to server'
        console.log action

# subviews
game.subviews = {ingame}

game.view = (ctrl) ->
    subview = game.subviews[game.vm.state()]
    [subview.view(new subview.controller(ctrl))]

# --------------------------------------------------------------
# game:ingame module
# --------------------------------------------------------------
class ingame.controller
    constructor: (pctrl) ->
        @topBar = new topBar.controller(pctrl)
        @gameActions = new gameActions.controller(pctrl)
        @infoArea = new infoArea.controller(pctrl)
        @gameMap = new gameMap.controller(pctrl)

ingame.view = (ctrl) -> [
    topBar.view ctrl.topBar
    gameActions.view ctrl.gameActions
    infoArea.view ctrl.infoArea
    gameMap.view ctrl.gameMap
]

# --------------------------------------------------------------
# ingame:topBar module
# --------------------------------------------------------------
class topBar.controller
    BAR_W = 400

    constructor: (pctrl) ->
        @showCaught = pctrl.showCaught

    timeLeftW: ->
        g = game.vm.game
        g.timeLeft() / g.totalTime() * BAR_W

    timeFullW: =>
        BAR_W - @timeLeftW()

    valueCaught: ->
        game.vm.game.valCaught()

topBar.timeSW = (ctrl) -> [
    m('i.fa.fa-clock-o')
    m('span.time-indicator.time-left',
        {style: {width: ctrl.timeLeftW()+'px'}}, m.trust '&nbsp;')
    m('span.time-indicator.time-full',
        {style: {width: ctrl.timeFullW()+'px'}}, m.trust '&nbsp;')
]

topBar.moneySW = (ctrl) -> m('div.right.money-ind', [
    '+'
    m('span', {}, ctrl.valueCaught())
    ' coins'
])

topBar.view = (ctrl) -> m('div.top-bar', [
    topBar.timeSW(ctrl)
    m('a.right[href=#]', {onclick: ctrl.showCaught}, 'Caught')
    topBar.moneySW(ctrl)
])

# --------------------------------------------------------------
# ingame:gameActions module
# --------------------------------------------------------------
gameActions.Actions = -> m.prop [{
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

gameActions.controller = (pctrl) ->
    actions: gameActions.Actions()
    act: (action) ->
        -> pctrl.act(action)

gameActions.view = (ctrl) -> [
    m('div#game-actions', [
        ctrl.actions().map((action) ->
            m('a[href="#"]', {onclick: ctrl.act(action.action)},
                action.title))])
]

# --------------------------------------------------------------
# ingame:infoArea module
# --------------------------------------------------------------
infoArea.controller = ->
infoArea.view = (ctrl) -> m('div#info-area', 'infoArea')

# --------------------------------------------------------------
# ingame:gameMap module
# --------------------------------------------------------------
gameMap.controller = ->
gameMap.view = (ctrl) -> m('div#game-map', 'gameMap')

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
m.route document.getElementById('page'), '/', {
    '/'         : game,
    '/shop'     : shop,
    '/trophies' : trophies
}

