# --------------------------------------------------------------
# navigation module
# --------------------------------------------------------------
# namespace
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
        title: 'Troph.',
    }
]


