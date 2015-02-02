var game, nav, shop, trophies;

nav = {};

nav.LinkList = function() {
  return m.prop([
    {
      url: '/',
      title: 'Game'
    }, {
      url: '/shop',
      title: 'Shop'
    }, {
      url: '/trophies',
      title: 'Trophies'
    }
  ]);
};

nav.controller = function() {
  return {
    links: nav.LinkList()
  };
};

nav.view = function(ctrl) {
  return [
    ctrl.links().map(function(link) {
      return m('a', {
        href: link.url,
        config: m.route
      }, link.title);
    })
  ];
};

m.module(document.getElementById('nav'), nav);

game = {};

game.controller = function() {};

game.view = function() {
  return ['game'];
};

shop = {};

shop.controller = function() {};

shop.view = function() {
  return ['shop'];
};

trophies = {};

trophies.controller = function() {};

trophies.view = function() {
  return ['trophies'];
};

m.route.mode = 'hash';

m.route(document.getElementById('page'), '/', {
  '/': game,
  '/shop': shop,
  '/trophies': trophies
});

//# sourceMappingURL=app.js.map
