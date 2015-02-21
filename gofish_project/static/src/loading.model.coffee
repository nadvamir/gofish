# --------------------------------------------------------------
# loading module
# --------------------------------------------------------------
# namespace
loading = {}

# view-model
loading.vm = do ->
    init: -> @loading = m.prop true
    startLoading: -> @loading(true)
    stopLoading: -> @loading(false)

