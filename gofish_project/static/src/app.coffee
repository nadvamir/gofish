#namespace
app = {}

#model
app.PageList = -> m.prop [
    {
        title: "Getting Started",
        url: "getting-started.html"
    },
    {
        title: "Documentation",
        url: "mithril.html"
    },
    {
        title: "Mithril Blog",
        url: "http://lhorie.github.io/mithril-blog/"
    },
    {
        title: "Mailing List",
        url: "https://groups.google.com/forum/#!forum/mithriljs"
    }
]

#controller
app.controller = ->
    pages = app.PageList()

    pages: pages,
    rotate: -> pages().push(pages().shift())

#view
app.view = (ctrl) -> [
    ctrl.pages().map((page) ->  m("a", {href: page.url}, page.title)),
    m("button", {onclick: ctrl.rotate}, "Rotate links")
]

#initialize
m.module(document, app)
