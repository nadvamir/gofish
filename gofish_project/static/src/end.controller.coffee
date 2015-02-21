# controller
class end.controller
    constructor: ->
        get('/end').then (r) =>
            @earned = m.prop r.earned
            @money  = m.prop r.money
            @stars  = m.prop r.stars

