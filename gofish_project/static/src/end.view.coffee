# view
end.view = (c) -> [
    m('div.top-bar', [
        'This day is over!'
    ])
    m('ul.list', [
        m('li', [
            'Earned '
            m('strong', c.earned())
            ' out of '
            m('strong', c.maximum())
            ' possible'
        ])
        m('li', [
            'Now you have '
            m('strong', c.money())
            ' coins'
        ])
    ])
]

