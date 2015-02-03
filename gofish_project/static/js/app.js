var caught, game, gameActions, gameMap, home, infoArea, nav, shop, topBar, trophies;

nav = {};

home = {};

game = {};

topBar = {};

gameActions = {};

infoArea = {};

gameMap = {};

caught = {};

shop = {};

trophies = {};

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
      title: 'Troph.'
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

home.controller = function() {};

home.view = function() {
  return ['home'];
};

game.Game = (function() {
  function Game() {
    this.totalTime = m.prop(480);
    this.timeLeft = m.prop(405);
    this.money = m.prop(151);
    this.valCaught = m.prop(15);
    this.location = 7;
    this.showDepth = true;
    this.map = [[5, 5, 7, 7, 9, 10, 8, 8, 7, 7, 6, 4, 6, 6, 6, 5, 5, 4, 3, 2]];
    this.position = 3;
    this.cues = [[1.0, 4], [1.0, 4], [0.0, 4], [0.0, 4], [1.0, 0], [-1, 0], [-1, 0]];
    this.caught = [];
  }

  return Game;

})();

game.vm = (function() {
  return {
    init: function() {
      return this.game = new game.Game();
    },
    act: function(action) {
      console.log('send a request to server');
      return console.log(action);
    }
  };
})();

game.controller = (function() {
  function controller() {
    game.vm.init();
  }

  return controller;

})();

game.view = function(ctrl) {
  return [topBar.view(), gameActions.view(), infoArea.view(), gameMap.view()];
};

topBar.vm = (function() {
  var BAR_W;
  BAR_W = 400;
  return {
    timeLeftW: function() {
      var g;
      g = game.vm.game;
      return g.timeLeft() / g.totalTime() * BAR_W;
    },
    timeFullW: function() {
      return BAR_W - this.timeLeftW();
    },
    valueCaught: function() {
      return game.vm.game.valCaught();
    }
  };
})();

topBar.timeSW = function() {
  return [
    m('i.fa.fa-clock-o'), m('span.time-indicator.time-left', {
      style: {
        width: topBar.vm.timeLeftW() + 'px'
      }
    }, m.trust('&nbsp;')), m('span.time-indicator.time-full', {
      style: {
        width: topBar.vm.timeFullW() + 'px'
      }
    }, m.trust('&nbsp;'))
  ];
};

topBar.moneySW = function() {
  return m('div.right.money-ind', ['+', m('span', {}, topBar.vm.valueCaught()), ' coins']);
};

topBar.view = function(ctrl) {
  return m('div.top-bar', [
    topBar.timeSW(ctrl), m('a.right[href=/caught]', {
      config: m.route
    }, 'Caught'), topBar.moneySW(ctrl)
  ]);
};

gameActions.actions = m.prop([
  {
    action: 'left',
    title: 'move left'
  }, {
    action: 'right',
    title: 'move right'
  }, {
    action: 'fish',
    title: 'fish here'
  }, {
    action: 'end',
    title: 'end game'
  }
]);

gameActions.view = function() {
  return [
    m('div#game-actions', [
      gameActions.actions().map(function(action) {
        return m('a[href="#"]', {
          onclick: game.vm.act(action.action)
        }, action.title);
      })
    ])
  ];
};

infoArea.view = function() {
  return m('div#info-area', 'infoArea');
};

gameMap.view = function() {
  return m('div#game-map', 'gameMap');
};

caught.controller = function() {};

caught.view = function() {
  return ['caught'];
};

shop.controller = function() {};

shop.view = function() {
  return ['shop'];
};

trophies.controller = function() {};

trophies.view = function() {
  return ['trophies'];
};

m.route.mode = 'hash';

m.route(document.getElementById('page'), '/game', {
  '/': home,
  '/game': game,
  '/caught': caught,
  '/shop': shop,
  '/trophies': trophies
});

//# sourceMappingURL=app.js.map
