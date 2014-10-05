from django.conf.urls import patterns, url
from gofish import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^levelselect/', views.levelselect, name='levelselect'),
        url(r'^shop/', views.shop, name='shop'),
        # TODO: update in order to select a specific level
        url(r'^level/', views.level, name='level'),
        url(r'^results/', views.results, name='results'),
        # start a new game round
        url(r'^api/start/(?P<level>\w+)/$', views.start, name='start'),
        # end the current game round preemptively
        url(r'^api/end/$', views.end, name='end'),
        # execute action
        url(r'^api/action/(?P<action>\w+)/(?P<par>[\w,]+)/$', views.action, name='action'),
        # update something (buy it)
        url(r'^api/update/(?P<target>\w+)/$', views.update, name='update'),
        # switch modifier
        url(r'^api/choose/(?P<modifier>\w+)/$', views.choose, name='choose'),
        # buy modifier
        url(r'^api/buy/(?P<modifier>\w+)/$', views.buy, name='buy'),
        # get game info (available levels, etc)
        url(r'^api/getgame/$', views.getgame, name='getgame'),
        )
