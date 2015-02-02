# --------------------------------------------------------------
# navigation module
# --------------------------------------------------------------
nav = {}

# model
nav.LinkList = -> m.prop [{
        url: '/',
        title: 'Game',
    }, {
        url: '/shop',
        title: 'Shop',
    }, {
        url: '/trophies',
        title: 'Trophies',
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
game = {}
game.controller = ->
game.view = -> ['game']

# --------------------------------------------------------------
# shop module
# --------------------------------------------------------------
shop = {}
shop.controller = ->
shop.view = -> ['shop']

# --------------------------------------------------------------
# trophies module
# --------------------------------------------------------------
trophies = {}
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

