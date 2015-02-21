# view
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

