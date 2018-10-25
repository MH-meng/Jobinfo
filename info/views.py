from django.shortcuts import render,HttpResponse,redirect,render_to_response
from django.http import JsonResponse
from django.contrib import auth
from info import models
from info.form.login import StudentForm
from info.form.register import StudentRegisterForm
from django.db.models import Count
import json

# Create your views here.

#登陆


#登陆
def login(request):
    if request.method == "POST":

        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("account")
        pwd = request.POST.get("password")
        user = auth.authenticate(username=username, password=pwd)
        if user:
            # 用户名密码正确
            # 给用户做登录
            ret["status"] = 1
            auth.login(request, user)
            ret["msg"] = "/index/"
        else:
            # 用户名密码错误
            ret["status"] = 0
            ret["msg"] = "用户名或密码错误,请重新输入！"

        return JsonResponse(ret)
    return render(request, "login.html")


#空白页面
def welcome(request):
    return render(request, 'welcome.html')

#退出登录
def logout(request):
    auth.logout(request)
    return redirect('/login/')


#首页
def index(request):
    # print(request.user.is_authenticated())
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return redirect('/login/')


#文章列表
def article_list(request):
    article_list = models.Article.objects.all().order_by("-create_time")
    count = models.Article.objects.all().count()
    # print(count)
    # print(article_list.tags__set("title"), type(article_list))
    # article_list = []
    # for a in article_obj:
    #     print(a.tags.all())
    # #     tags = models.Tag.objects.filter(nid=article_list).values_list("title")
    # #     article_list.append(a)
    # # print(article_list)
    return render(request, 'article-list.html', locals())


#添加文章 保存并提交
def add_article(request):
    tags_list = models.Tag.objects.all()
    if request.method == "POST":
        # print(request.POST)
        # print("-" * 120)
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        tags = request.POST.get("tags")
        article_content = request.POST.get("article_content")
        user = request.user
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, 'html.parser')
        # print(bs,type(bs))
        # print("-" * 120)

        # desc = bs[0:150]

        for tag in bs.find_all():
            if tag.name in["script"]:
                tag.decompose()
        tag_obj = models.Tag.objects.filter(title=tags).first()
        article_obj = models.Article.objects.create(title=title, desc=desc, status=1, content=str(bs), tags_id=tag_obj.nid)
        # models.ArticleDetail.objects.create(content=str(bs), article=article_obj)
        ret = {}
        ret["msg"] = "提交成功，已发布！！"
        ret["link"] = "/article_list/"
        return JsonResponse(ret)
        # import time
        # time.sleep(5)
        # return redirect('/index/')

    return render(request, 'article-add.html', locals())


#删除文章
def del_article(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Article.objects.filter(nid=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


#文章下架(停用)
def article_stop(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Article.objects.filter(nid=id).update(status=0)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)



#文章悬浮下架(停用)
def float_stop(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Float.objects.filter(nid=id).update(status=0)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


#文章悬浮
def picture_start(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Float.objects.filter(nid=id).update(status=1)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)

#悬浮删除
def picture_del(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Float.objects.filter(nid=id).delete()
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


#文章发布
def article_start(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Article.objects.filter(nid=id).update(status=1)
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)


#文章编辑
def article_edit(request, id):
    if request.method == "POST":
        # print(id)
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        tags = request.POST.get("tags")
        article_content = request.POST.get("article_content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, 'html.parser')

        for tag in bs.find_all():
            if tag.name in ["script"]:
                tag.decompose()
        tag_obj = models.Tag.objects.filter(title=tags).first()
        article_obj = models.Article.objects.filter(nid=id).update(title=title, desc=desc, status=1, content=str(bs),
                                                    tags_id=tag_obj.nid)
        ret = {}
        ret["msg"] = "提交成功，已发布！！"
        ret["link"] = "/article_list/"
        return JsonResponse(ret)

    else:
        article_obj = models.Article.objects.filter(nid=id).first()
        tags_list=models.Tag.objects.all()
        # print(article_obj.tags)
        tags_obj = []
        for tags in tags_list:
            # print(tags)
            if article_obj.tags == tags:
                tags_obj.insert(0, article_obj.tags)
            else:
                tags_obj.append(tags)

        # print(len(tags_obj), len(tags_list))
        # print(tags_obj)


    return render(request, 'article_edit.html', locals())


#分类列表
def article_class(request):
    tags_list = models.Tag.objects.all()
    count = models.Tag.objects.all().count()

    return render(request, 'article-class.html', locals())

#分类列表
def article_class_add(request):
    if request.method == "POST":
        tags_title = request.POST.get("article_tags")
        is_exist = models.Tag.objects.filter(title=tags_title).first()
        ret = {}
        if is_exist:
            ret["status"] = 0
            ret["msg"] = "此分类已存在！"
        else:
            tags_obj =  models.Tag.objects.create(title=tags_title)
            tags_count = models.Tag.objects.all().count()
            ret["status"] = 1
            ret["tags_ccount"] = models.Tag.objects.all().count()
            ret["nid"] = tags_obj.pk
            ret["tags_title"] = tags_obj.title

        return JsonResponse(ret)


#浮动窗口内容列表
def float_list(request):
    float_obj = models.Float.objects.all().order_by("-create_time")
    count = models.Float.objects.all().count()
    return render(request, 'picture-list.html', locals())



#浮动窗口内容列表
def float_edit(request,id):
    # print(id)
    if request.method == "POST":
        # print(id)
        article_title = request.POST.get("article_title")
        article_desc = request.POST.get("article_desc")
        float_title = request.POST.get("float_title")
        float_desc = request.POST.get("float_desc")
        article_content = request.POST.get("article_content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, 'html.parser')
        for tag in bs.find_all():
            if tag.name in ["script"]:
                tag.decompose()
        models.Float.objects.filter(nid=id).update(a_title=article_title, a_desc=article_desc, status=1, content=str(bs),
                                                    f_title=float_title, f_desc=float_desc)


        ret = {}
        ret["msg"] = "提交成功，已发布！！"
        ret["link"] = "/picture_list/"
        return JsonResponse(ret)

    else:
        float_obj = models.Float.objects.filter(nid=id).first()
    return render(request, 'picture-edit.html', locals())


#添加浮动窗口内容
def float_add(request):
    if request.method == "POST":
        article_title = request.POST.get("article_title")
        article_desc = request.POST.get("article_desc")
        float_title = request.POST.get("float_title")
        float_desc = request.POST.get("float_desc")
        article_content = request.POST.get("article_content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content, 'html.parser')
        for tag in bs.find_all():
            if tag.name in ["script"]:
                tag.decompose()
        models.Float.objects.create(a_title=article_title, a_desc=article_desc, status=1, content=str(bs),
                                                    f_title=float_title, f_desc=float_desc)
        ret = {}
        ret["msg"] = "提交成功，已发布！！"
        ret["link"] = "/picture_list/"
        return JsonResponse(ret)

    return render(request, 'picture-add.html')



#招聘会列表
def invite_list(request):
    invite_list = models.Invite.objects.all()
    count = models.Invite.objects.all().count()
    return render(request, "invite-list.html", locals())


#招聘会添加
def add_invite(request):
    # print("hahahahahhahahhaha")
    ret = {}
    if request.method == "POST":
        # print("jejejej")
        name = request.POST.get("name")
        city = request.POST.get("city")
        i_type = request.POST.get("type")
        i_data = request.POST.get("data")
        sponsor = request.POST.get("sponsor")
        content = request.POST.get("content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(content, 'html.parser')
        models.Invite.objects.create(i_name=name, i_data=i_data, i_city=city, i_sponsor=sponsor, i_type=i_type, i_content=str(bs))
        # print(name, city, i_type, i_data, sponsor, content)
        ret["msg"] = "添加成功！"
        ret["link"] = "/invite_list/"
        return JsonResponse(ret)

    return render(request, "invite-add.html", locals())


#招聘会删除
def del_invite(request):
    if request.method == "POST":
        id = request.POST.get("pk")
        models.Invite.objects.filter(id=id).delete()
        ret = {}
        ret["id"] = id
        return JsonResponse(ret)



#招聘会编辑
def invite_edit(request, id):
    ret = {}
    if request.method == "POST":
        name = request.POST.get("name")
        city = request.POST.get("city")
        i_type = request.POST.get("type")
        i_data = request.POST.get("data")
        sponsor = request.POST.get("sponsor")
        content = request.POST.get("content")
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(content, 'html.parser')
        models.Invite.objects.filter(id=id).update(i_name=name, i_data=i_data, i_city=city, i_sponsor=sponsor, i_type=i_type,
                                     i_content=str(bs))
        # print(name, city, i_type, i_data, sponsor, content)
        ret["msg"] = "修改成功，已发布！"
        ret["link"] = "/invite_list/"
        return JsonResponse(ret)


    else:
        invite_obj = models.Invite.objects.filter(id=id).first()

    return render(request, 'invite-edit.html', locals())




#孟浩




# 首页
def m_index(request):
    infor = {'status':True}
    if request.session.get('is_login1', None):
        infor['status'] = True
        number = request.session.get('number', None)
        name = models.Conpanys.objects.filter(c_number=number).values()
        preach = models.Invite.objects.filter().all().order_by('-id')[:10]
        company = models.Conpanys.objects.filter().all().order_by('-id')[:10]
        teachin = models.Teachin.objects.filter().all().order_by('-id')[:10]
        zhaopin = models.Zhaopin.objects.filter().all().order_by('-id')[:10]
        article = models.Article.objects.filter().all().order_by('-nid')[:8]
        float = models.Float.objects.all().order_by('-create_time')[:2]
        return render(request, 'm_index.html', {
            'number': number,
            'name': name,
            'infor': infor,
            'company': company,
            'preach_infor': preach,
            'teachin': teachin,
            'zhaopin': zhaopin,
            'article': article,
            'float': float,
        })
    else:
        infor['status'] = False
        preach = models.Invite.objects.filter().all().order_by('-id')[:10]
        company = models.Conpanys.objects.filter().all().order_by('-id')[:10]
        teachin = models.Teachin.objects.filter().all().order_by('-id')[:10]
        zhaopin = models.Zhaopin.objects.filter().all().order_by('-id')[:10]
        article = models.Article.objects.filter().all().order_by('-nid')[:8]
        float = models.Float.objects.all().order_by('-create_time')[:2]
        # print(float)
        return render(request, 'm_index.html', {
            'infor':infor,
            'company':company,
            'preach_infor':preach,
            'teachin':teachin,
            'zhaopin':zhaopin,
            'article':article,
            'float':float,
        })

    # return render(request,'m_index.html')


#登录
def m_login(request):
    if request.method == "GET":
        # 创建一个HTML
        obj_form = StudentForm()
        return render(request, 'm_login.html', locals())
    else:
        infor = {'status':True}
        obj_form = StudentForm(request.POST)
        # 是否全部验证成功
        if obj_form.is_valid():
            # 用户提交的数据
            c_number = obj_form.cleaned_data['number']
            c_pwd = obj_form.cleaned_data['pwd']
            c_ret = models.Conpanys.objects.filter(c_number=c_number,c_pwd=c_pwd).count()
            # print('c_ret',c_ret)
            if c_ret:
                infor['status'] = True
                request.session['is_login1'] = True
                request.session['number'] = c_number
                return redirect('/')
            else:
                infor['status'] = False
                obj_form.error_class = "用户账号或密码错误，请重新输入。。。。"
                return render(request, 'm_login.html', {'obj_form': obj_form})
        else:
            return render(request, 'm_login.html', {'obj_form': obj_form})
# 注册
import time
def register(request):
    if request.method == "GET":
        # 创建一个HTML
        obj_form = StudentRegisterForm()
        return render(request, 'register.html', {'obj_form':obj_form})
    else:
        obj_form = StudentRegisterForm(request.POST)
        # 是否全部验证成功
        if obj_form.is_valid():
            # 用户提交的数据
            c_name = obj_form.cleaned_data['name']
            c_number = obj_form.cleaned_data['number']
            c_pwd = obj_form.cleaned_data['pwd']
            times = time.localtime()
            c_create_time = time.strftime('%Y-%m-%d',times)

            models.Conpanys.objects.create(
                c_name=c_name,
                c_number=c_number,
                c_pwd=c_pwd,
                c_create_time = c_create_time
            )
            return redirect('/success/')
        else:
            return render(request, 'register.html', {'obj_form': obj_form})
def success(request):
    return render(request,'succes.html')

import json
def user_center(request):
    if request.method == "GET":
        cid = request.GET.get('cid')
        company = models.Conpanys.objects.filter(id=cid).values()
        teachin = models.Teachin.objects.filter(x_company_id=cid).values()
        return render(request,'user_center.html',{
            'company':company,
            'teachin':teachin,
            'cid':cid
        })
    else:
        show_inf = {'status': True, 'inf': None}
        id = request.POST.get('id')
        c_nature = request.POST.get('c_nature')
        c_industry = request.POST.get('c_industry')
        c_scale = request.POST.get('c_scale')
        c_city = request.POST.get('c_city')
        c_linkman = request.POST.get('c_linkman')
        c_phone = request.POST.get('c_phone')
        c_brief = request.POST.get('c_brief')
        models.Conpanys.objects.filter(id=id).update(
            c_nature=c_nature,
            c_industry=c_industry,
            c_scale=c_scale,
            c_phone=c_phone,
            c_brief=c_brief,
            c_city=c_city,
            c_linkman=c_linkman,
        )
        show_inf['inf']='完善信息成功'
        res = json.dumps(show_inf)
        return HttpResponse(res)

def user_center_preach(request):
    if request.method == "POST":
        show_inf = {'status': True, 'inf': None}

        # 宣讲会
        x_company_id = request.POST.get('x_company_id')
        x_title = request.POST.get('x_title')
        x_time = request.POST.get('x_time')
        x_city = request.POST.get('x_city')
        x_school = request.POST.get('x_school')
        x_detail = request.POST.get('x_detail')
        models.Teachin.objects.filter().create(
            x_title=x_title,
            x_time=x_time,
            x_city=x_city,
            x_school=x_school,
            x_detail=x_detail,
            x_company_id=x_company_id,
        )

        show_inf['inf'] = '发布宣讲会信息成功'
        res = json.dumps(show_inf)
        return HttpResponse(res)

def user_center_zhaopin(request):
    if request.method == "POST":
        show_inf = {'status': True, 'inf': None}

        # 招聘会
        z_company_id = request.POST.get('z_company_id')
        z_position = request.POST.get('z_position')
        z_number = request.POST.get('z_number')
        z_salary = request.POST.get('z_salary')
        z_education = request.POST.get('z_education')
        z_experience = request.POST.get('z_experience')
        z_nature = request.POST.get('z_nature')
        z_data = request.POST.get('z_data')
        z_city = request.POST.get('z_city')
        z_email = request.POST.get('z_email')
        z_detail = request.POST.get('z_detail')
        models.Zhaopin.objects.filter().create(
            z_position=z_position,
            z_number=z_number,
            z_education=z_education,
            z_experience=z_experience,
            z_nature=z_nature,
            z_data=z_data,
            z_email=z_email,
            z_city=z_city,
            z_detail=z_detail,
            z_salary=z_salary,
            z_company_id=z_company_id,
        )

        show_inf['inf'] = '发布招聘信息成功'
        res = json.dumps(show_inf)
        return HttpResponse(res)


# 学生
def m_student_link(request):
    return render(request,'m_student_link.html')
# 单位
def m_danwei_link(request):
    return render(request,'m_danwei_link.html')
# 教师
def m_teacher_link(request):
    return render(request,'m_teacher_link.html')
# 创业指导
def m_news_cyzd(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_news_cyzd.html',locals())
# 关于我们
def m_news_gywm(request):
    return render(request,'m_news_gywm.html')

# 通知公告
def m_news_tzgg(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_news_tzgg.html',{'article':article})
# 通知公告文章
def m_news_tzgg_article(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        # for i in article_infor:
        #     print(i)
        return render(request,'m_news_tzgg_article.html',{'article_infor':article_infor})
# 新闻快递
def m_news_xwkd(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_news_xwkd.html',{'article':article})
# 新闻快递文章
def m_news_xwkd_article(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        # for i in article_infor:
        #     print(i)
        return render(request,'m_news_xwkd_article.html',{'article_infor':article_infor})
# 校园公示
def m_news_xygs(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_news_xygs.html',{'article':article})
# 校园公示文章
def m_news_xygs_article(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_news_xygs_article.html',{'article_infor':article_infor})

# 宣讲会
def m_teachin(request):
    company_teachin = models.Conpanys.objects.filter().all()
    teachin_teachin = models.Teachin.objects.filter().all()
    return render(request,'m_teachin.html',locals())
# 宣讲会-内容
def m_teachin_content(request):
    if request.method == "GET":
        pid = request.GET.get('pid')
        teachin_infor = models.Teachin.objects.filter(id=pid).values()
        teachins = []
        for teachin in teachin_infor:
            te={}
            x_time = teachin['x_time']
            x_city = teachin['x_city']
            x_school = teachin['x_school']
            x_detail = teachin['x_detail']
            x_company_id = teachin['x_company_id']
            te['x_time']=x_time
            te['x_city']=x_city
            te['x_school']=x_school
            te['x_detail']=x_detail
            company_infor = models.Conpanys.objects.filter(id=x_company_id).values()
            for company in company_infor:
                c_name = company['c_name']
                c_nature = company['c_nature']
                c_industry = company['c_industry']
                c_scale = company['c_scale']
                c_brief = company['c_brief']
                c_phone = company['c_phone']
                te['c_name'] = c_name
                te['c_nature'] = c_nature
                te['c_industry'] = c_industry
                te['c_scale'] = c_scale
                te['c_brief'] = c_brief
                te['c_phone'] = c_phone
            teachins.append(te)
        return render(request, 'm_teachin_content.html', {'teachins':teachins})
# 招聘公告
def m_campus(request):
    company_teachin = models.Conpanys.objects.filter().all()
    zhaopin_teachin = models.Zhaopin.objects.filter().all()
    return render(request,'m_campus.html',
                  {'company_teachin':company_teachin,'zhaopin_teachin':zhaopin_teachin})
# 招聘公告-内容
def m_campus_content(request):
    if request.method == "GET":
        pid = request.GET.get('pid')
        company_infor = models.Conpanys.objects.filter(id=pid).values()
        companys=[]
        for company in company_infor:
            cop = {}
            c_id = company['id']
            c_name = company['c_name']
            c_nature = company['c_nature']
            c_industry = company['c_industry']
            c_scale = company['c_scale']
            c_brief = company['c_brief']
            c_city = company['c_city']
            cop['c_name'] = c_name
            cop['c_nature'] = c_nature
            cop['c_industry'] = c_industry
            cop['c_scale'] = c_scale
            cop['c_brief'] = c_brief
            cop['c_city'] = c_city
            zhaopin_infor = models.Zhaopin.objects.filter(z_company_id=c_id).values()
            for zhaopin in zhaopin_infor:
                z_position = zhaopin['z_position']
                z_number = zhaopin['z_number']
                z_salary = zhaopin['z_salary']
                z_data = zhaopin['z_data']
                z_city = zhaopin['z_city']
                z_email = zhaopin['z_email']
                z_detail = zhaopin['z_detail']
                cop['z_position'] = z_position
                cop['z_number'] = z_number
                cop['z_salary'] = z_salary
                cop['z_city'] = z_city
                cop['z_data'] = z_data
                cop['z_email'] = z_email
                cop['z_detail'] = z_detail
            companys.append(cop)

        return render(request,'m_campus_content.html',{'companys':companys})
# 招聘会
def m_jobfair(request):
    preach_infor = models.Invite.objects.filter().all()
    return render(request,'m_jobfair.html',{'preach_infor':preach_infor})
# 招聘会-内容
def m_jobfair_content(request):
    if request.method == "GET":
        zid = request.GET.get('zid')
        invite_infor = models.Invite.objects.filter(id=zid).values()
        company_invite = models.Conpanys.objects.filter().all()
        zhaopin_invite = models.Zhaopin.objects.filter().values()
        # print(zhaopin_invite)
        return render(request,'m_jobfair_content.html',{
            'invite_infor':invite_infor,
            'company_invite':company_invite,
            'zhaopin_invite':zhaopin_invite,
        })
# 岗位
def m_station(request):
    company_station = models.Conpanys.objects.filter().all()
    zhaopin_station = models.Zhaopin.objects.filter().all()
    return render(request,'m_station.html',{
        'company_station':company_station,
        'zhaopin_station':zhaopin_station
    })
# 岗位-内容
def m_station_content(request):
    if request.method == "GET":
        pid = request.GET.get('pid')
        company_infor = models.Conpanys.objects.filter(id=pid).values()
        return render(request,'m_station_content.html',{'company_infor':company_infor})
# 招考公告
def m_invite(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_invite.html',locals())
# 招考公告-内容
def m_invite_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_invite_content.html',locals())

# 政策法规
def m_policy(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_policy.html',locals())
# 政策法规-内容
def m_policy_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_policy_content.html',locals())
# 就业指导
def m_obtain(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_obtain.html',locals())
# 就业指导-内容
def m_obtain_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_obtain_content.html',locals())
# # 创业指导
# def m_guide(request):
#     article = models.Article.objects.filter().values()
#     return render(request,'m_guide.html',locals())
# 创业指导-内容
def m_guide_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_guide_content.html',locals())
# 创业教育
def m_education(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_education.html',locals())
# 创业教育-内容
def m_education_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_education_content.html',locals())
# 创业实践
def m_practice(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_practice.html',locals())
# 创业实践-内容
def m_practice_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_practice_content.html',locals())
# 创业风采
def m_elegant(request):
    article = models.Article.objects.filter().values()
    return render(request,'m_elegant.html',locals())
# 创业风采-内容
def m_elegant_content(request):
    if request.method == 'GET':
        nid = request.GET.get('news_id')
        article_infor = models.Article.objects.filter(nid=nid).values()
        return render(request,'m_elegant_content.html',locals())

# 浮动框
def m_float(request):
    nid = request.GET.get('news')
    float_infor = models.Float.objects.filter(nid=nid).values()

    return render(request,'m_float.html',locals())

#退出登录
def m_logout(request):
    del request.session["is_login1"]
    return redirect('/')






#文件上传
import os
from jobinfo import settings
def upload(request):
    # print(request.FILES)
    obj = request.FILES.get("upload_img")
    path = os.path.join(settings.MEDIA_ROOT, 'add_article_img', obj.name)

    with open(path,"wb") as f:
        for line in obj:
            f.write(line)

    res ={
        "error":0,
        "url":"/media/add_article_img/"+obj.name
    }
    return HttpResponse(json.dumps(res))