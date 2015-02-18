# --------------------------------------------------------------
# module declarations with their submodules
# --------------------------------------------------------------
nav         = {}

home        = {}

game        = {}
gTopBar     = {}
gameActions = {}
infoArea    = {}
gameMap     = {}

caught      = {}

end         = {}

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
        @highS    = m.prop lvl.highS
        @maxHighS = m.prop lvl.maxHighS

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
        get('/start/' + @id()).then (r) ->
            if r.error
                console.log r
            else
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
                # high score
                m('.right', [
                    m('strong', @highS())
                    ' / '
                    m('strong', @maxHighS())
                ])
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

home.view = -> [
    topBar('Choose a location:', game.vm.player.money())
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
        @day       = m.prop g.day
        @name      = m.prop g.name
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
        @info = m.prop ''
        get('/v2/game').then (r) =>
            @game = new game.Game(r.game)

    act: (action) ->
        urls =
            fish  : '/action/catchall/1'
            left  : '/action/move/left'
            right : '/action/move/right'

        common = (r) ->
            if r.error
                return m.route '/end'
            g = game.vm.game
            g.timeLeft(g.totalTime() - parseInt(r.time, 10))
            g.cues(r.cues)

        move = (r) ->
            common(r)
            game.vm.game.position(r.position)
            game.vm.info ''

        fish = (r) ->
            # if there is no fishes, then it is the end
            if 0 == r.fishList.length
                return m.route '/end'
            # otherwise, common pattern
            common(r)
            fish = r.fishList[0]
            if null != fish
                g = game.vm.game
                g.valCaught(g.valCaught() + fish.value)
                f = new game.Fish(fish)
                game.vm.info ['You\'ve got ', caught.vm.getItemView.apply(f)]
                g.caught().push f
            else
                game.vm.info 'Nothing was caught'

        actions = {fish : fish, left : move, right : move}

        get(urls[action]).then actions[action], -> m.route '/end'

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
    gTopBar.view()
    gameActions.view()
    infoArea.view()
    gameMap.view()
]

# --------------------------------------------------------------
# game:topBar module
# --------------------------------------------------------------
gTopBar.vm = do ->
    BAR_W = 400

    timeLeftW: ->
        g = game.vm.game
        g.timeLeft() / g.totalTime() * BAR_W

    timeFullW: ->
        BAR_W - @timeLeftW()

    valueCaught: ->
        game.vm.game.valCaught()

# Day sub-view
gTopBar.daySW = -> m('.day-ind', [
    'Day '
    m('span', game.vm.game.day())
    '. '
    m('span', game.vm.game.name())
])

# time sub-view
gTopBar.timeSW = -> [
    m('i.fa.fa-clock-o')
    m('span.time-indicator.time-left',
        {style: {width: gTopBar.vm.timeLeftW()+'px'}}, m.trust '&nbsp;')
    m('span.time-indicator.time-full',
        {style: {width: gTopBar.vm.timeFullW()+'px'}}, m.trust '&nbsp;')
]

# money sub-view
gTopBar.moneySW = -> m('div.right.money-ind', [
    '+'
    m('span', {}, gTopBar.vm.valueCaught())
    ' coins'
])

gTopBar.view = (caught) -> m('div.top-bar', [
    gTopBar.timeSW()
    gTopBar.daySW()
    (caught and m('a.right[href=/game]', {config: m.route}, 'Back') or m('a.right[href=/caught]', {config: m.route}, "Caught #{game.vm.game.caught().length} fish"))
    gTopBar.moneySW()
])

# --------------------------------------------------------------
# game:gameActions module
# --------------------------------------------------------------
gameActions.actions = m.prop [{
        action : 'left',
        title  : 'move left',
    }, {
        action : 'fish',
        title  : 'fish here',
    }, {
        action : 'right',
        title  : 'move right',
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
infoArea.view = -> m('div#info-area', game.vm.info())

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
        m('span', @name())
        ', weight '
        @weight()
        ' kg, value '
        m('strong', @value())
    ]
    compare: (a, b) ->
        b.value() - a.value()

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
        m('span', {}, gTopBar.vm.valueCaught())
        ' coins. Total: '
        m('span', {}, game.vm.player.money())
    ])
])

caught.view = -> [
    (game.vm.inGame() and gTopBar.view(true) or caught.topBar())
    list.view(game.vm.game.caught().sort(caught.vm.compare), caught.vm.getItemView)
]


# --------------------------------------------------------------
# end of game module
# --------------------------------------------------------------
class end.controller
    constructor: ->
        get('/end').then (r) =>
            @earned = m.prop r.earned
            @money  = m.prop r.money
            @stars  = m.prop r.stars

end.view = (c) -> [
    m('div.top-bar', [
        'This day is over!'
    ])
    m('ul.list', [
        m('li', [
            'Earned '
            m('strong', c.earned())
        ])
        m('li', [
            'Now you have '
            m('strong', c.money())
            ' coins'
        ])
        (c.stars() > 0 and (
            m('li', [
                'Achieved '
                m('strong', c.stars())
                ' stars'
            ])
        ) or '')
    ])
]

# --------------------------------------------------------------
# shop module
# --------------------------------------------------------------
class shop.Update
    constructor: (b, type) ->
        @name = m.prop b.name
        @cost = m.prop b.cost
        @perk = m.prop b.perk
        @type = m.prop type

shop.Updates = Array

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

shop.controller = ->
    shop.vm.init()

shop.currentView = (u) -> m('div.shop-item', [
    'You have a '
    m('span', u.name())
    ': '
    u.perk()
])

shop.updateView = (u) ->
    if not u
        m('div.shop-item', 'Nothing is better!')
    else if shop.vm.player.money() < u.cost()
        m('div.shop-item', [
            'Update to '
            m('span', u.name())
            ' for '
            m('strong', u.cost())
            ': '
            u.perk()
        ])
    else
        m('div.shop-item', [
            'Upgrade to '
            m('a[href=#]', {onclick: link shop.vm.update.bind u}, u.name())
            ' for '
            m('strong', u.cost())
            ' coins: '
            u.perk()
        ])

shop.view = -> [
    topBar('Shop:', shop.vm.player.money())
    m('h2', 'Boats')
    shop.currentView(shop.vm.currentBoat())
    shop.updateView(shop.vm.updateBoat())
    m('h2', 'Lines')
    shop.currentView(shop.vm.currentLine())
    shop.updateView(shop.vm.updateLine())
    m('h2', 'Cues')
    shop.currentView(shop.vm.currentCue())
    shop.updateView(shop.vm.updateCue())
]

# --------------------------------------------------------------
# trophies module
# --------------------------------------------------------------
trophies.Trophies = Array

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

trophies.controller = ->
    trophies.vm.init()

trophies.item = (userT, gameT) -> m('li', [
    caught.vm.getItemView.apply(userT)
    m('.right', [
        '/ '
        m('strong', gameT.value())
    ])
])

trophies.listTrophies = ->
    m('.list', [trophies.item(@userT[i], @gameT[i]) for i in [0...@userT.length]])


trophies.view = -> [
    topBar('Trophies and records:', trophies.vm.player.money())
    trophies.listTrophies.apply(trophies.vm)
]

# --------------------------------------------------------------
# reusable components and functions
# --------------------------------------------------------------
# list component, produces a list when given an array of items
list.view = (items, view) -> m('ul.list', [
    items.map((item) ->
        m('li', {key: item.id()}, [view.apply(item)]))
])

# gets a top bar with a message and money from a player
topBar = (text, money) -> m('div.top-bar', [
    m('span.large', text)
    m('div.right.money-ind', [
        m('span', money)
        ' coins'
    ])
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
    '/end'      : end,
    '/shop'     : shop,
    '/trophies' : trophies
}

