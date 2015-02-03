var game, gameActions, gameMap, infoArea, ingame, nav, shop, topBar, trophies,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

nav = {};

game = {};

ingame = {};

topBar = {};

gameActions = {};

infoArea = {};

gameMap = {};

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
      this.game = new game.Game();
      return this.state = m.prop('ingame');
    }
  };
})();

game.controller = (function() {
  function controller() {
    game.vm.init();
  }

  controller.prototype.showCaught = function() {
    return console.log('caught asked');
  };

  controller.prototype.act = function(action) {
    console.log('send a request to server');
    return console.log(action);
  };

  return controller;

})();

game.subviews = {
  ingame: ingame
};

game.view = function(ctrl) {
  var subview;
  subview = game.subviews[game.vm.state()];
  return [subview.view(new subview.controller(ctrl))];
};

ingame.controller = (function() {
  function controller(pctrl) {
    this.topBar = new topBar.controller(pctrl);
    this.gameActions = new gameActions.controller(pctrl);
    this.infoArea = new infoArea.controller(pctrl);
    this.gameMap = new gameMap.controller(pctrl);
  }

  return controller;

})();

ingame.view = function(ctrl) {
  return [topBar.view(ctrl.topBar), gameActions.view(ctrl.gameActions), infoArea.view(ctrl.infoArea), gameMap.view(ctrl.gameMap)];
};

topBar.controller = (function() {
  var BAR_W;

  BAR_W = 400;

  function controller(pctrl) {
    this.timeFullW = __bind(this.timeFullW, this);
    this.showCaught = pctrl.showCaught;
  }

  controller.prototype.timeLeftW = function() {
    var g;
    g = game.vm.game;
    return g.timeLeft() / g.totalTime() * BAR_W;
  };

  controller.prototype.timeFullW = function() {
    return BAR_W - this.timeLeftW();
  };

  controller.prototype.valueCaught = function() {
    return game.vm.game.valCaught();
  };

  return controller;

})();

topBar.timeSW = function(ctrl) {
  return [
    m('i.fa.fa-clock-o'), m('span.time-indicator.time-left', {
      style: {
        width: ctrl.timeLeftW() + 'px'
      }
    }, m.trust('&nbsp;')), m('span.time-indicator.time-full', {
      style: {
        width: ctrl.timeFullW() + 'px'
      }
    }, m.trust('&nbsp;'))
  ];
};

topBar.moneySW = function(ctrl) {
  return m('div.right.money-ind', ['+', m('span', {}, ctrl.valueCaught()), ' coins']);
};

topBar.view = function(ctrl) {
  return m('div.top-bar', [
    topBar.timeSW(ctrl), m('a.right[href=#]', {
      onclick: ctrl.showCaught
    }, 'Caught'), topBar.moneySW(ctrl)
  ]);
};

gameActions.Actions = function() {
  return m.prop([
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
};

gameActions.controller = function(pctrl) {
  return {
    actions: gameActions.Actions(),
    act: function(action) {
      return function() {
        return pctrl.act(action);
      };
    }
  };
};

gameActions.view = function(ctrl) {
  return [
    m('div#game-actions', [
      ctrl.actions().map(function(action) {
        return m('a[href="#"]', {
          onclick: ctrl.act(action.action)
        }, action.title);
      })
    ])
  ];
};

infoArea.controller = function() {};

infoArea.view = function(ctrl) {
  return m('div#info-area', 'infoArea');
};

gameMap.controller = function() {};

gameMap.view = function(ctrl) {
  return m('div#game-map', 'gameMap');
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

m.route(document.getElementById('page'), '/', {
  '/': game,
  '/shop': shop,
  '/trophies': trophies
});

//# sourceMappingURL=app.js.map
