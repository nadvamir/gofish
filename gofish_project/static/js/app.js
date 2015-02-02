var app;

app = {};

app.PageList = function() {
  return m.prop([
    {
      title: "Getting Started",
      url: "getting-started.html"
    }, {
      title: "Documentation",
      url: "mithril.html"
    }, {
      title: "Mithril Blog",
      url: "http://lhorie.github.io/mithril-blog/"
    }, {
      title: "Mailing List",
      url: "https://groups.google.com/forum/#!forum/mithriljs"
    }
  ]);
};

app.controller = function() {
  var pages;
  pages = app.PageList();
  return {
    pages: pages,
    rotate: function() {
      return pages().push(pages().shift());
    }
  };
};

app.view = function(ctrl) {
  return [
    ctrl.pages().map(function(page) {
      return m("a", {
        href: page.url
      }, page.title);
    }), m("button", {
      onclick: ctrl.rotate
    }, "Rotate links")
  ];
};

m.module(document, app);

//# sourceMappingURL=app.js.map
