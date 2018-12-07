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
from django.conf.urls import url, include
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

    # 宣讲会相关
    url(r'^Teachin_list/$', views.Teachin_list),
    url(r'^teachin_stop/$', views.teachin_stop),
    url(r'^teachin_start/$', views.teachin_start),
    url(r'^teachin_del/$', views.teachin_del),
    url(r'^teachin_edit/(\d+)/', views.teachin_edit),


    #孟浩
    url(r'^$', views.m_index),
    url(r'^m_login/$',views.m_login),
    url(r'^m_register/$', views.m_register),
    url(r'^success/$', views.success),
    url(r'^company/', include('companyadmin.urls')),
    url(r'^m_student_link/$',views.m_student_link),
    url(r'^m_danwei_link/$',views.m_danwei_link),
    url(r'^m_teacher_link/$',views.m_teacher_link),
    url(r'^m_news_cyzd/$',views.m_news_cyzd),
    url(r'^m_news_gywm/$',views.m_news_gywm),

    url(r'^m_enroliment/$', views.m_enroliment),
    url(r'^m_enroliment_content/$', views.m_enroliment_content),
    url(r'^m_quality/$', views.m_quality),
    url(r'^m_quality_content/$', views.m_quality_content),
    url(r'^m_intership/$', views.m_intership),
    url(r'^m_intership_content/$', views.m_intership_content),
    url(r'^m_survey/$', views.m_survey),
    url(r'^m_survey_content/$', views.m_survey_content),
    url(r'^m_alumnus/$', views.m_alumnus),
    url(r'^m_alumnus_content/$', views.m_alumnus_content),
    url(r'^m_incubation/$', views.m_incubation),
    url(r'^m_incubation_content/$', views.m_incubation_content),

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

    url(r'^m_guide/$', views.m_guide),
    url(r'^m_guide_content/$',views.m_guide_content),
    url(r'^m_education/$',views.m_education),
    url(r'^m_education_content/$',views.m_education_content),
    url(r'^m_practice/$',views.m_practice),
    url(r'^m_practice_content/$',views.m_practice_content),
    url(r'^m_elegant/$',views.m_elegant),
    url(r'^m_elegant_content/$',views.m_elegant_content),
    url(r'^m_float/$',views.m_float),
    url(r'^m_logout/$',views.m_logout),
    url(r'^m_download/$', views.m_download),
    url(r'^m_download_content/$', views.m_download_content),

    url(r'^ariticle_upload/', views.ariticle_upload),
    url(r'^float_upload/', views.float_upload),
    url(r'^invite_upload/', views.invite_upload),
    url(r'^invite_upload/', views.invite_upload),
    url(r'^teachin_upload/', views.teachin_upload),

    # 友情链接
    url(r'^blogroll_list/$', views.blogroll_list),
    url(r'^blogroll_add/$', views.blogroll_add),
    url(r'^upload_img/$', views.upload_img),
    url(r'^del_blogroll/$', views.del_blogroll),

    # 图片新闻
    url(r'^news_list/$', views.news_list),
    url(r'^news_add/$', views.news_add),
    url(r'^upload_news_img/$', views.upload_news_img),
    url(r'^del_news/$', views.del_news),
    url(r'^news_start/$', views.news_start),
    url(r'^news_stop/$', views.news_stop),
    url(r'^news_upload/$', views.news_upload),
    url(r'^news_edit/$', views.news_edit),
    url(r'^edit_news_img/$', views.edit_news_img),
    url(r'^news_detail/$', views.news_detail),


    # media 相关的路由设置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

    # 验证码
    url(r'^Login/$', views.Login),
    url(r'^checkcode/$', views.CheckCode),

]
