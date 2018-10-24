"""jobinfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from info import views
from django.views.static import serve
from django.conf import  settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^index/$', views.index),
    url(r'^welcome/$', views.welcome),
    url(r'^article_list/$', views.article_list),
    url(r'^article_add/$', views.add_article),
    url(r'^del_article/$', views.del_article),
    url(r'^article_stop/$', views.article_stop),
    url(r'^article_edit/(\d+)/', views.article_edit),
    url(r'^article_start/$', views.article_start),
    url(r'^article_class/$', views.article_class),
    url(r'^article_class_add/$', views.article_class_add),
    url(r'^float_stop/$', views.float_stop),
    url(r'^picture_start/$', views.picture_start),
    url(r'^picture_del/$', views.picture_del),
    url(r'^picture_list/$', views.float_list),
    url(r'^picture_edit/(\d+)/', views.float_edit),
    url(r'^picture_add/$', views.float_add),


    #招娉会相关
    url(r'^invite_list/$', views.invite_list),
    url(r'^add_invite/$', views.add_invite),
    url(r'^del_invite/$', views.del_invite),
    url(r'^invite_edit/(\d+)/', views.invite_edit),


    #孟浩
url(r'^$',views.m_index),
    url(r'^m_login/$',views.m_login),
    url(r'^register/$',views.register),
    url(r'^success/$', views.success),
    url(r'^user_center/$', views.user_center),
    url(r'^user_center_preach/$', views.user_center_preach),
    url(r'^user_center_zhaopin/$', views.user_center_zhaopin),

    url(r'^m_student_link/$',views.m_student_link),
    url(r'^m_danwei_link/$',views.m_danwei_link),
    url(r'^m_teacher_link/$',views.m_teacher_link),
    url(r'^m_news_cyzd/$',views.m_news_cyzd),
    url(r'^m_news_gywm/$',views.m_news_gywm),

    url(r'^m_news_tzgg/$',views.m_news_tzgg),
    url(r'^m_news_tzgg_article/$',views.m_news_tzgg_article),
    url(r'^m_news_xwkd/$',views.m_news_xwkd),
    url(r'^m_news_xwkd_article/$',views.m_news_xwkd_article),
    url(r'^m_news_xygs/$',views.m_news_xygs),
    url(r'^m_news_xygs_article/$',views.m_news_xygs_article),

    url(r'^m_teachin/$',views.m_teachin),
    url(r'^m_teachin_content/$',views.m_teachin_content),
    url(r'^m_campus/$',views.m_campus),
    url(r'^m_campus_content/$',views.m_campus_content),
    url(r'^m_jobfair/$',views.m_jobfair),
    url(r'^m_jobfair_content/$',views.m_jobfair_content),
    url(r'^m_station/$',views.m_station),
    url(r'^m_station_content/$',views.m_station_content),
    url(r'^m_invite/$',views.m_invite),
    url(r'^m_invite_content/$',views.m_invite_content),

    url(r'^m_policy/$',views.m_policy),
    url(r'^m_policy_content/$',views.m_policy_content),
    url(r'^m_obtain/$',views.m_obtain),
    url(r'^m_obtain_content/$',views.m_obtain_content),

    # url(r'^m_guide/$',views.m_guide),
    url(r'^m_guide_content/$',views.m_guide_content),
    url(r'^m_education/$',views.m_education),
    url(r'^m_education_content/$',views.m_education_content),
    url(r'^m_practice/$',views.m_practice),
    url(r'^m_practice_content/$',views.m_practice_content),
    url(r'^m_elegant/$',views.m_elegant),
    url(r'^m_elegant_content/$',views.m_elegant_content),
    url(r'^m_float/$',views.m_float),
    url(r'^m_logout/$',views.m_logout),







    url(r'^upload/', views.upload),

    # media 相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    #
]
