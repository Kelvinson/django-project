from django.conf.urls import url
from . import views


urlpatterns = [
        url(r'^$',views.post_list,name = 'post_list'),
        url(r'^post/(?P<pk>[0-9]+)/$',views.post_detail,name='post_detail'),
        url(r'^post/new/$',views.post_new,name = 'post_new'),
        url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
        url(r'^chart/$',views.piechart,name='pie_chart'),
        url(r'^barchart/$',views.multibarchart,name='multibarchart'),
        url(r'^scatterchart/$',views.scatterchart,name ='scatterchart'),
        url(r'^table/$',views.people,name = 'tables'),
        url(r'^lineplusbarchart/$',views.lineplusbarchart,name = 'linepluschart'),
        url(r'^result_detail_date/date/(?P<date>[0-9]+)/$',views.result_detail_date,name = 'result_detail_date'),
        url(r'^search/$',views.search_result,name = 'search_result'),
        url(r'^trend/rules/(?P<rules>[^/]+)/$',views.trend_plot,name = 'trend_plot'),
        url(r'^trend/items/(?P<items>[^/]+)/$',views.trend_plot_items,name = 'trend_plot_items')
        ]
