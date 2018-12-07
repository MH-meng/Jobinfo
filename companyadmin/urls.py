from django.conf.urls import url
from companyadmin import views

urlpatterns = [
    url(r'^c_index/$', views.c_index),
    url(r'^c_welcome/$', views.c_welcome),

    url(r'^c_teachin/$', views.c_teachin),
    url(r'^c_teachin_add/$', views.c_teachin_add),
    url(r'^c_teachin_edit/$', views.c_teachin_edit),
    url(r'^c_teachin_add_confirm/$', views.c_teachin_add_confirm),
    url(r'^c_teachin_del/$', views.c_teachin_del),

    url(r'^c_zhaopin/$', views.c_zhaopin),
    url(r'^c_zhaopin_del/$', views.c_zhaopin_del),
    url(r'^c_zhaopin_add_confirm/$', views.c_zhaopin_add_confirm),
    url(r'^c_zhaopin_add/$', views.c_zhaopin_add),
    url(r'^c_zhaopin_edit/$', views.c_zhaopin_edit),

    url(r'^c_perfect/$', views.c_perfect),
    url(r'^confirm_center/$', views.confirm_center),
    url(r'^c_password/$', views.c_password),
    url(r'^upload/$', views.upload),
]
