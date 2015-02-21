# sub-view to show single trophy item
trophies.item = (userT, gameT) -> m('li', [
    caught.vm.getItemView.apply(userT)
    m('.right', [
        '/ '
        m('strong', gameT.value())
    ])
])

# sub-view to list all trophies
trophies.listTrophies = ->
    m('.list', [trophies.item(@userT[i], @gameT[i]) for i in [0...@userT.length]])

# view
trophies.view = -> [
    topBar('Trophies and records:', trophies.vm.player.money())
    trophies.listTrophies.apply(trophies.vm)
]

