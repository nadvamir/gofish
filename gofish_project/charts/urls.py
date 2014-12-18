from django.conf.urls import patterns, url
from charts import views

urlpatterns = patterns('',
        # index page, to show the options
        url(r'^$', views.index, name='index'),
        # consumes log and creates database entries from it
        url(r'^parse_log/$', views.parseLog, name='parseLog'),
        # visualiser of individual user data
        url(r'^data_by_user/$', views.dataByUser,
            name='dataByUser'),
        # visualiser of aggregated data
        url(r'^data_aggregated/$', views.dataAggregated,
            name='dataAggregated'),
        # api call to get specific data
        url(r'^api/get_data/$', views.getData,
            name='getData'),
        # api call for bar chart data
        url(r'^api/get_bar_data/$', views.getBarData,
            name='getData'),
        # api call for box plot data
        url(r'^api/get_box_data/$', views.getBoxData,
            name='getData'),
)
