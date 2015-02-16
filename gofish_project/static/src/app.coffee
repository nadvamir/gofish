# --------------------------------------------------------------
# module declarations with their submodules
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
# reusable components
# --------------------------------------------------------------
list        = {}

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
# model for game location
class home.Level
    constructor: (id) ->
        @id       = m.prop id
        @name     = m.prop 'Local Pond'
        @unlocked = m.prop true
        @active   = m.prop true
        @cost     = m.prop 100
        @stars    = m.prop 2
        @index    = m.prop 0

# model for all game locations
home.Levels = Array

home.vm = do ->
    init: ->
        @levels = new home.Levels()
        @levels.push new home.Level(0)
        @levels.push new home.Level(1)
        @levels.push new home.Level(2)
        @levels.push new home.Level(3)
        @levels[1].unlocked(false)
        @levels[2].unlocked(false)
        @levels[2].cost(1000)
        @levels[3].unlocked(false)
        @levels[3].active(false)

    chooseLevel: ->
        console.log @index()
        m.route('/game')

    # an item view function, has to be bound to a model
    getItemView: ->
        # unlocked and playable
        if @unlocked()
            [
                m('a[href=#]', {onclick:
                    link home.vm.chooseLevel.bind(@)}, @name())
                ', unlocked. '
                ['*' for star in [0...@stars()]]
            ]
        # available to unlock
        else if @active() and @cost() <= game.vm.game.money()
            [
                m('a[href=#]', {onclick:
                    link home.vm.chooseLevel.bind(@)}, @name())
                ', cost '
                m('strong', @cost())
            ]
        # not available to unlock
        else if @active()
            [
                @name()
                ', cost '
                m('strong', @cost())
            ]
        # not yet playable
        else
            @name()

home.controller = ->
    home.vm.init()
    game.vm.init()

home.topBar = -> m('div.top-bar', [
    'Choose a location:'
    m('div.right.money-ind', [
        m('span', {}, game.vm.game.money())
        ' coins'
    ])
])

home.view = -> [
    home.topBar()
    list.view(home.vm.levels, home.vm.getItemView)
]

# --------------------------------------------------------------
# game module
# --------------------------------------------------------------
# model of a Fish
class game.Fish
    constructor: ->
        @id     = m.prop new Date().getTime()
        @name   = m.prop 'Bass'
        @value  = m.prop 105
        @weight = m.prop 5.3

# game model
class game.Game
    constructor: ->
        @totalTime = m.prop 480
        @timeLeft  = m.prop 405
        @money     = m.prop 151
        @boat      = m.prop 0
        @line      = m.prop 0
        @valCaught = m.prop 15
        @showDepth = m.prop true
        @map       = m.prop [[5, 5, 7, 7, 9, 10, 8, 8, 7, 7, 6, 4, 6, 6, 6, 5, 5, 4, 3, 2]]
        @position  = m.prop 3
        @cues      = m.prop [[1.0, 4], [3.0, 4], [0.0, 4], [0.0, 4], [5.0, 0], [-1, 0], [-1, 0]]
        @caught    = m.prop []

        @caught().push new game.Fish()
        @caught().push new game.Fish()
        @caught().push new game.Fish()

game.vm = do ->
    init: ->
        # game object
        @game = new game.Game()

    act: (action) ->
        console.log 'send a request to server'
        console.log action

    inGame: ->
        @game != null

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

topBar.view = (caught) -> m('div.top-bar', [
    topBar.timeSW()
    (caught and m('a.right[href=/game]', {config: m.route}, 'Back') or m('a.right[href=/caught]', {config: m.route}, 'Caught'))
    topBar.moneySW()
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
            m('a[href="#"]', {onclick: link game.vm.act.bind(@, action.action)},
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
gameMap.boatSW = -> m('p', [
    m('span.boat-' + game.vm.game.boat(), {style:
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
    home.vm.init()
    game.vm.init()

caught.vm = do ->
    getItemView: -> [
        @name()
        ', weight '
        @weight()
        ' kg, value '
        m('strong', @value())
    ]

caught.topBarGame = -> m('div.top-bar', [
    'Choose a location:'
    m('div.right.money-ind', [
        m('span', {}, game.vm.game.money())
        ' coins'
    ])
])

# a top bar at the end of the game
caught.topBar = -> m('div.top-bar', [
    'Results of this fishing trip:'
    m('div.right.money-ind', [
        '+'
        m('span', {}, topBar.vm.valueCaught())
        ' coins. Total: '
        m('span', {}, game.vm.game.money())
    ])
])

caught.view = -> [
    (game.vm.inGame() and topBar.view(true) or caught.topBar())
    list.view(game.vm.game.caught(), caught.vm.getItemView)
]


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
# reusable components and functions
# --------------------------------------------------------------
# list component, produces a list when given an array of items
list.view = (items, view) -> m('ul.list', [
    items.map((item) ->
        m('li', {key: item.id()}, [view.apply(item)]))
])

link = (f) ->
    (e) ->
        e.preventDefault()
        f()

# --------------------------------------------------------------
# routing
# --------------------------------------------------------------
m.route.mode = 'hash'
m.route document.getElementById('page'), '/', {
    '/'         : home,
    '/game'     : game,
    '/caught'   : caught,
    '/shop'     : shop,
    '/trophies' : trophies
}

