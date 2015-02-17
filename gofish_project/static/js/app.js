var caught, game, gameActions, gameMap, get, home, infoArea, link, list, nav, shop, topBar, trophies, url;

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

list = {};

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

home.Level = (function() {
  function Level(lvl) {
    this.id = m.prop(lvl.id);
    this.name = m.prop(lvl.name);
    this.unlocked = m.prop(lvl.unlocked);
    this.active = m.prop(lvl.active);
    this.cost = m.prop(lvl.cost);
    this.stars = m.prop(lvl.stars);
  }

  return Level;

})();

home.Levels = Array;

home.vm = (function() {
  return {
    init: function() {
      return get('/v2/home').then((function(_this) {
        return function(r) {
          var level, _i, _len, _ref, _results;
          _this.levels = new home.Levels();
          _ref = r.levels;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            level = _ref[_i];
            _results.push(_this.levels.push(new home.Level(level)));
          }
          return _results;
        };
      })(this));
    },
    chooseLevel: function() {
      console.log(this.id());
      return m.route('/game');
    },
    getItemView: function() {
      var star;
      if (this.unlocked()) {
        return [
          m('a[href=#]', {
            onclick: link(home.vm.chooseLevel.bind(this))
          }, this.name()), ', unlocked. ', [
            (function() {
              var _i, _ref, _results;
              _results = [];
              for (star = _i = 0, _ref = this.stars(); 0 <= _ref ? _i < _ref : _i > _ref; star = 0 <= _ref ? ++_i : --_i) {
                _results.push('*');
              }
              return _results;
            }).call(this)
          ]
        ];
      } else if (this.active() && this.cost() <= game.vm.player.money()) {
        return [
          m('a[href=#]', {
            onclick: link(home.vm.chooseLevel.bind(this))
          }, this.name()), ', cost ', m('strong', this.cost())
        ];
      } else if (this.active()) {
        return [this.name(), ', cost ', m('strong', this.cost())];
      } else {
        return this.name();
      }
    }
  };
})();

home.controller = function() {
  home.vm.init();
  return game.vm.init().then(function() {
    if (game.vm.inGame()) {
      return m.route('/game');
    }
  });
};

home.topBar = function() {
  return m('div.top-bar', ['Choose a location:', m('div.right.money-ind', [m('span', {}, game.vm.player.money()), ' coins'])]);
};

home.view = function() {
  return [home.topBar(), list.view(home.vm.levels, home.vm.getItemView)];
};

game.Fish = (function() {
  function Fish(f) {
    this.id = m.prop(new Date().getTime());
    this.name = m.prop(f.name);
    this.value = m.prop(f.value);
    this.weight = m.prop(f.weight);
  }

  return Fish;

})();

game.Player = (function() {
  function Player(p) {
    this.money = m.prop(p.money);
    this.boat = m.prop(p.boat);
    this.line = m.prop(p.line);
    this.cue = m.prop(p.cue);
  }

  return Player;

})();

game.Game = (function() {
  function Game(g) {
    var f, _i, _len, _ref;
    this.totalTime = m.prop(g.totalTime);
    this.timeLeft = m.prop(g.timeLeft);
    this.valCaught = m.prop(g.valCaught);
    this.showDepth = m.prop(g.showDepth);
    this.map = m.prop(g.map);
    this.position = m.prop(g.position);
    this.cues = m.prop(g.cues);
    this.caught = m.prop([]);
    _ref = g.caught;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      f = _ref[_i];
      this.caught().push(new game.Fish(f));
    }
  }

  return Game;

})();

game.vm = (function() {
  return {
    init: function() {
      get('/v2/player').then((function(_this) {
        return function(r) {
          return _this.player = new game.Player(r.player);
        };
      })(this));
      this.game = null;
      return get('/v2/game').then((function(_this) {
        return function(r) {
          return _this.game = new game.Game(r.game);
        };
      })(this));
    },
    act: function(action) {
      console.log('send a request to server');
      return console.log(action);
    },
    inGame: function() {
      return this.game !== null;
    },
    getWaterClass: function(i, j) {
      if (i < this.game.map()[0][j]) {
        if (j !== this.game.position() || this.game.cues()[i][0] + 1 < 0.001) {
          return 'dark-water';
        } else {
          return 'light-water.fish-' + Math.round(this.game.cues()[i][0]);
        }
      } else {
        return 'ground';
      }
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

topBar.view = function(caught) {
  return m('div.top-bar', [
    topBar.timeSW(), caught && m('a.right[href=/game]', {
      config: m.route
    }, 'Back') || m('a.right[href=/caught]', {
      config: m.route
    }, 'Caught'), topBar.moneySW()
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
          onclick: link(game.vm.act.bind(this, action.action))
        }, action.title);
      })
    ])
  ];
};

infoArea.view = function() {
  return m('div#info-area', 'infoArea');
};

gameMap.TILE_W = 40;

gameMap.boatSW = function() {
  return m('p', [
    m('span.boat-' + game.vm.player.boat(), {
      style: {
        marginLeft: gameMap.TILE_W * game.vm.game.position() + 'px'
      }
    })
  ]);
};

gameMap.waterSW = function() {
  var i, j;
  if (game.vm.game.showDepth()) {
    return [
      (function() {
        var _i, _results;
        _results = [];
        for (i = _i = 0; _i < 10; i = ++_i) {
          _results.push(m('p', [
            (function() {
              var _j, _results1;
              _results1 = [];
              for (j = _j = 0; _j < 20; j = ++_j) {
                _results1.push(m('span.' + game.vm.getWaterClass(i, j)));
              }
              return _results1;
            })()
          ]));
        }
        return _results;
      })()
    ];
  } else {
    return [
      (function() {
        var _i, _results;
        _results = [];
        for (i = _i = 0; _i < 20; i = ++_i) {
          _results.push(m('span.dark-water'));
        }
        return _results;
      })()
    ];
  }
};

gameMap.view = function() {
  return m('div#game-map', [gameMap.boatSW(), gameMap.waterSW()]);
};

caught.controller = function() {
  home.vm.init();
  return game.vm.init();
};

caught.vm = (function() {
  return {
    getItemView: function() {
      return [this.name(), ', weight ', this.weight(), ' kg, value ', m('strong', this.value())];
    }
  };
})();

caught.topBarGame = function() {
  return m('div.top-bar', ['Choose a location:', m('div.right.money-ind', [m('span', {}, game.vm.player.money()), ' coins'])]);
};

caught.topBar = function() {
  return m('div.top-bar', ['Results of this fishing trip:', m('div.right.money-ind', ['+', m('span', {}, topBar.vm.valueCaught()), ' coins. Total: ', m('span', {}, game.vm.player.money())])]);
};

caught.view = function() {
  return [game.vm.inGame() && topBar.view(true) || caught.topBar(), list.view(game.vm.game.caught(), caught.vm.getItemView)];
};

shop.view = function() {
  return ['shop'];
};

trophies.controller = function() {};

trophies.view = function() {
  return ['trophies'];
};

list.view = function(items, view) {
  return m('ul.list', [
    items.map(function(item) {
      return m('li', {
        key: item.id()
      }, [view.apply(item)]);
    })
  ]);
};

link = function(f) {
  return function(e) {
    e.preventDefault();
    return f();
  };
};

url = function(specifics) {
  return '/gofish/api' + specifics;
};

get = function(q) {
  return m.request({
    method: 'GET',
    url: url(q)
  });
};

m.route.mode = 'hash';

m.route(document.getElementById('page'), '/', {
  '/': home,
  '/game': game,
  '/caught': caught,
  '/shop': shop,
  '/trophies': trophies
});

//# sourceMappingURL=app.js.map
