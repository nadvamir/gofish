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
    constructor: (lvl) ->
        @id       = m.prop lvl.id
        @name     = m.prop lvl.name
        @unlocked = m.prop lvl.unlocked
        @active   = m.prop lvl.active
        @cost     = m.prop lvl.cost
        @stars    = m.prop lvl.stars

# model for all game locations
home.Levels = Array

home.vm = do ->
    # initialisaton gets the list of levels
    init: ->
        get('/v2/home').then (r) =>
            @levels = new home.Levels()
            for level in r.levels
                @levels.push new home.Level(level)

    chooseLevel: ->
        console.log @id()
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
        else if @active() and @cost() <= game.vm.player.money()
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
    game.vm.init().then ->
        if game.vm.inGame()
            m.route('/game')

home.topBar = -> m('div.top-bar', [
    'Choose a location:'
    m('div.right.money-ind', [
        m('span', {}, game.vm.player.money())
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
    constructor: (f) ->
        @id     = m.prop new Date().getTime()
        @name   = m.prop f.name
        @value  = m.prop f.value
        @weight = m.prop f.weight

# a player model
class game.Player
    constructor: (p) ->
        @money = m.prop p.money
        @boat  = m.prop p.boat
        @line  = m.prop p.line
        @cue   = m.prop p.cue

# game model
class game.Game
    constructor: (g) ->
        @totalTime = m.prop g.totalTime
        @timeLeft  = m.prop g.timeLeft
        @valCaught = m.prop g.valCaught
        @showDepth = m.prop g.showDepth
        @map       = m.prop g.map
        @position  = m.prop g.position
        @cues      = m.prop g.cues
        @caught    = m.prop []
        for f in g.caught
            @caught().push new game.Fish(f)

game.vm = do ->
    init: ->
        get('/v2/player').then (r) =>
            @player = new game.Player(r.player)
        @game = null
        get('/v2/game').then (r) =>
            @game = new game.Game(r.game)

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
    m('span.boat-' + game.vm.player.boat(), {style:
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
        m('span', {}, game.vm.player.money())
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
        m('span', {}, game.vm.player.money())
    ])
])

caught.view = -> [
    (game.vm.inGame() and topBar.view(true) or caught.topBar())
    list.view(game.vm.game.caught(), caught.vm.getItemView)
]


# --------------------------------------------------------------
# shop module
# -------------------------------------------------------------- shop.controller = ->
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

# returns an onclick for links that runs js instead of defaults
link = (f) ->
    (e) ->
        e.preventDefault()
        f()

# returns an url that works with server
url = (specifics) -> '/gofish/api' + specifics

# makes a get query
get = (q) -> m.request(method: 'GET', url: url(q))
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

