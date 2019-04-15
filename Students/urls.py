from django.conf.urls import url
from Students import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^register/$', views.register),
    url(r'^success/$', views.success),
    url(r'^logout/$', views.logout),
    url(r'^index/$', views.index),
    url(r'^index/$', views.index),
    url(r'^welcome/$', views.welcome),

    # 修改信息
    url(r'^supdateinfo/$', views.supdateinfo),

    # 工作经验
    url(r'^workexperiencelist/$', views.workexperiencelist),
    url(r'^workexperienceadd/$', views.workexperienceadd),
    url(r'^workexperiencedel/$', views.workexperiencedel),
    url(r'^workexperienceupd/$', views.workexperienceupd),

    # 教育经历
    url(r'^educationexperiencelist/$', views.educationexperiencelist),
    url(r'^educationexperienceadd/$', views.educationexperienceadd),
    url(r'^educationexperiencedel/$', views.educationexperiencedel),
    url(r'^educationexperienceupd/$', views.educationexperienceupd),

    # 求职意见
    url(r'^jobintensionlist/$', views.jobintensionlist),
    url(r'^jobintensionadd/$', views.jobintensionadd),
    url(r'^jobintensiondel/$', views.jobintensiondel),
    url(r'^jobintensionupd/$', views.jobintensionupd),

    # 项目经验
    url(r'^projectexperiencelist/$', views.projectexperiencelist),
    url(r'^projectexperienceadd/$', views.projectexperienceadd),
    url(r'^projectexperiencedel/$', views.projectexperiencedel),
    url(r'^projectexperienceupd/$', views.projectexperienceupd),
]
