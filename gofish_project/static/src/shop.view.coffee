# a sub-view to display current level of update
shop.currentView = (u) -> m('div.shop-item', [
    'You have a '
    m('span', u.name())
    ': '
    u.perk()
])

# a sub-view to display new level of update
shop.updateView = (u) ->
    if not u
        m('div.shop-item', 'Nothing is better!')
    else if shop.vm.player.money() < u.cost()
        m('div.shop-item', [
            'Update to '
            m('span', u.name())
            ' for '
            m('strong', {title: 'Cost in coins'}, u.cost())
            ': '
            u.perk()
        ])
    else
        m('div.shop-item', [
            'Upgrade to '
            m('a[href=#]', {onclick: link shop.vm.update.bind u}, u.name())
            ' for '
            m('strong', {title: 'Cost in coins'}, u.cost())
            ' coins: '
            u.perk()
        ])

# view
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

