var caught, end, gTopBar, game, gameActions, gameMap, get, home, infoArea, link, list, nav, shop, topBar, trophies, url;

nav = {};

home = {};

game = {};

gTopBar = {};

gameActions = {};

infoArea = {};

gameMap = {};

caught = {};

end = {};

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
    this.highS = m.prop(lvl.highS);
    this.maxHighS = m.prop(lvl.maxHighS);
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
      return get('/start/' + this.id()).then(function(r) {
        if (r.error) {
          return console.log(r);
        } else {
          return m.route('/game');
        }
      });
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
          ], m('.right', [m('strong', this.highS()), ' / ', m('strong', this.maxHighS())])
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

home.view = function() {
  return [topBar('Choose a location:', game.vm.player.money()), list.view(home.vm.levels, home.vm.getItemView)];
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
    this.day = m.prop(g.day);
    this.name = m.prop(g.name);
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
      this.info = m.prop('');
      return get('/v2/game').then((function(_this) {
        return function(r) {
          return _this.game = new game.Game(r.game);
        };
      })(this));
    },
    act: function(action) {
      var actions, common, fish, move, urls;
      urls = {
        fish: '/action/catchall/1',
        left: '/action/move/left',
        right: '/action/move/right'
      };
      common = function(r) {
        var g;
        if (r.error) {
          return m.route('/end');
        }
        g = game.vm.game;
        g.timeLeft(g.totalTime() - parseInt(r.time, 10));
        return g.cues(r.cues);
      };
      move = function(r) {
        common(r);
        game.vm.game.position(r.position);
        return game.vm.info('');
      };
      fish = function(r) {
        var f, g;
        if (0 === r.fishList.length) {
          return m.route('/end');
        }
        common(r);
        fish = r.fishList[0];
        if (null !== fish) {
          g = game.vm.game;
          g.valCaught(g.valCaught() + fish.value);
          f = new game.Fish(fish);
          game.vm.info(['You\'ve got ', caught.vm.getItemView.apply(f)]);
          return g.caught().push(f);
        } else {
          return game.vm.info('Nothing was caught');
        }
      };
      actions = {
        fish: fish,
        left: move,
        right: move
      };
      return get(urls[action]).then(actions[action], function() {
        return m.route('/end');
      });
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
  return [gTopBar.view(), gameActions.view(), infoArea.view(), gameMap.view()];
};

gTopBar.vm = (function() {
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

gTopBar.daySW = function() {
  return m('.day-ind', ['Day ', m('span', game.vm.game.day()), '. ', m('span', game.vm.game.name())]);
};

gTopBar.timeSW = function() {
  return [
    m('i.fa.fa-clock-o'), m('span.time-indicator.time-left', {
      style: {
        width: gTopBar.vm.timeLeftW() + 'px'
      }
    }, m.trust('&nbsp;')), m('span.time-indicator.time-full', {
      style: {
        width: gTopBar.vm.timeFullW() + 'px'
      }
    }, m.trust('&nbsp;'))
  ];
};

gTopBar.moneySW = function() {
  return m('div.right.money-ind', ['+', m('span', {}, gTopBar.vm.valueCaught()), ' coins']);
};

gTopBar.view = function(caught) {
  return m('div.top-bar', [
    gTopBar.timeSW(), gTopBar.daySW(), caught && m('a.right[href=/game]', {
      config: m.route
    }, 'Back') || m('a.right[href=/caught]', {
      config: m.route
    }, "Caught " + (game.vm.game.caught().length) + " fish"), gTopBar.moneySW()
  ]);
};

gameActions.actions = m.prop([
  {
    action: 'left',
    title: 'move left'
  }, {
    action: 'fish',
    title: 'fish here'
  }, {
    action: 'right',
    title: 'move right'
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
  return m('div#info-area', game.vm.info());
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
    },
    compare: function(a, b) {
      return b.value() - a.value();
    }
  };
})();

caught.topBarGame = function() {
  return m('div.top-bar', ['Choose a location:', m('div.right.money-ind', [m('span', {}, game.vm.player.money()), ' coins'])]);
};

caught.topBar = function() {
  return m('div.top-bar', ['Results of this fishing trip:', m('div.right.money-ind', ['+', m('span', {}, gTopBar.vm.valueCaught()), ' coins. Total: ', m('span', {}, game.vm.player.money())])]);
};

caught.view = function() {
  return [game.vm.inGame() && gTopBar.view(true) || caught.topBar(), list.view(game.vm.game.caught().sort(caught.vm.compare), caught.vm.getItemView)];
};

end.controller = (function() {
  function controller() {
    get('/end').then((function(_this) {
      return function(r) {
        _this.earned = m.prop(r.earned);
        _this.money = m.prop(r.money);
        return _this.stars = m.prop(r.stars);
      };
    })(this));
  }

  return controller;

})();

end.view = function(c) {
  return [m('div.top-bar', ['This day is over!']), m('ul.list', [m('li', ['Earned ', m('strong', c.earned())]), m('li', ['Now you have ', m('strong', c.money()), ' coins']), c.stars() > 0 && (m('li', ['Achieved ', m('strong', c.stars()), ' stars'])) || ''])];
};

shop.Update = (function() {
  function Update(b, type) {
    this.name = m.prop(b.name);
    this.cost = m.prop(b.cost);
    this.perk = m.prop(b.perk);
    this.type = m.prop(type);
  }

  return Update;

})();

shop.Updates = Array;

shop.vm = (function() {
  return {
    init: function() {
      get('/v2/player').then((function(_this) {
        return function(r) {
          return _this.player = new game.Player(r.player);
        };
      })(this));
      this.boats = new shop.Updates();
      this.lines = new shop.Updates();
      this.cues = new shop.Updates();
      return get('/v2/shop').then((function(_this) {
        return function(r) {
          var u, _i, _j, _k, _len, _len1, _len2, _ref, _ref1, _ref2, _results;
          _ref = r.boats;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            u = _ref[_i];
            _this.boats.push(new shop.Update(u, 'boats'));
          }
          _ref1 = r.lines;
          for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
            u = _ref1[_j];
            _this.lines.push(new shop.Update(u, 'lines'));
          }
          _ref2 = r.cues;
          _results = [];
          for (_k = 0, _len2 = _ref2.length; _k < _len2; _k++) {
            u = _ref2[_k];
            _results.push(_this.cues.push(new shop.Update(u, 'cues')));
          }
          return _results;
        };
      })(this));
    },
    currentBoat: function() {
      return shop.vm.boats[shop.vm.player.boat() + 1];
    },
    updateBoat: function() {
      return shop.vm.boats[shop.vm.player.boat() + 2];
    },
    currentLine: function() {
      return shop.vm.lines[shop.vm.player.line() + 1];
    },
    updateLine: function() {
      return shop.vm.lines[shop.vm.player.line() + 2];
    },
    currentCue: function() {
      return shop.vm.cues[shop.vm.player.cue() + 1];
    },
    updateCue: function() {
      return shop.vm.cues[shop.vm.player.cue() + 2];
    },
    update: function() {
      return get('/update/' + this.type()).then(function() {
        return m.route('/shop');
      });
    }
  };
})();

shop.controller = function() {
  return shop.vm.init();
};

shop.currentView = function(u) {
  return m('div.shop-item', ['You have a ', m('span', u.name()), ': ', u.perk()]);
};

shop.updateView = function(u) {
  if (!u) {
    return m('div.shop-item', 'Nothing is better!');
  } else if (shop.vm.player.money() < u.cost()) {
    return m('div.shop-item', ['Update to ', m('span', u.name()), ' for ', m('strong', u.cost()), ': ', u.perk()]);
  } else {
    return m('div.shop-item', [
      'Upgrade to ', m('a[href=#]', {
        onclick: link(shop.vm.update.bind(u))
      }, u.name()), ' for ', m('strong', u.cost()), ' coins: ', u.perk()
    ]);
  }
};

shop.view = function() {
  return [topBar('Shop:', shop.vm.player.money()), m('h2', 'Boats'), shop.currentView(shop.vm.currentBoat()), shop.updateView(shop.vm.updateBoat()), m('h2', 'Lines'), shop.currentView(shop.vm.currentLine()), shop.updateView(shop.vm.updateLine()), m('h2', 'Cues'), shop.currentView(shop.vm.currentCue()), shop.updateView(shop.vm.updateCue())];
};

trophies.vm = (function() {
  return {
    init: function() {
      return get('/v2/player').then((function(_this) {
        return function(r) {
          return _this.player = new game.Player(r.player);
        };
      })(this));
    }
  };
})();

trophies.controller = function() {
  return trophies.vm.init();
};

trophies.view = function() {
  return [topBar('Trophies and records:', trophies.vm.player.money())];
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

topBar = function(text, money) {
  return m('div.top-bar', [m('span.large', text), m('div.right.money-ind', [m('span', money), ' coins'])]);
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
  '/end': end,
  '/shop': shop,
  '/trophies': trophies
});

//# sourceMappingURL=app.js.map
