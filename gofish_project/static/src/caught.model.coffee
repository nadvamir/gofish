# --------------------------------------------------------------
# caught module
# --------------------------------------------------------------
# namespace
caught = {}

# view-model
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

