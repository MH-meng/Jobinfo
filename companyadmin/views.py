from django.shortcuts import render, HttpResponse
from info import models
import json


# 主页框架
def c_index(request):
    cid = request.GET.get('cid')
    company_name = models.Conpanys.objects.filter(id=cid).values()
    return render(request, 'company/c_index.html', {'company_name': company_name, 'cid': cid})


# 首页
def c_welcome(request):
    cid = request.GET.get('cid')
    company_name = models.Conpanys.objects.filter(id=cid).values()
    return render(request, 'company/welcome.html', {'company_name': company_name})


# 宣讲会
def c_teachin(request):
    cid = request.GET.get('cid')
    teachin_list = models.Teachin.objects.filter(x_company_id=cid).values().order_by('-id')
    teachin_count = models.Teachin.objects.filter(x_company_id=cid).count()
    return render(request, 'company/article-list.html',
                  {
                      'teachin_list': teachin_list,
                      'cid': cid,
                      'teachin_count': teachin_count,

                  })


# 添加宣讲会
def c_teachin_add(request):
    cid = request.GET.get('cid')
    return render(request, 'company/article-add.html', locals())


# 宣讲会添加
def c_teachin_add_confirm(request):
    if request.method == "POST":
        show_inf = {'status': True, 'inf': None}

        # 宣讲会
        x_company_id = request.POST.get('x_company_id')
        x_title = request.POST.get('x_title')
        x_time = request.POST.get('x_time')
        x_city = request.POST.get('x_city')
        x_school = request.POST.get('x_school')
        x_detail = request.POST.get('x_detail')
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(x_detail, 'html.parser')
        if x_title and x_city and x_school and x_detail:
            models.Teachin.objects.filter().create(
                x_title=x_title,
                x_time=x_time,
                x_city=x_city,
                x_school=x_school,
                x_detail=str(bs),
                x_company_id=x_company_id,
            )

            show_inf['inf'] = '发布宣讲会信息成功'
            show_inf['link'] = '/company/c_teachin?cid=' + x_company_id

        else:
            show_inf['status'] = False
            show_inf['inf'] = '请把信息填写完整，谢谢！'
        res = json.dumps(show_inf)
        return HttpResponse(res)


# 删除宣讲会
from django.http import JsonResponse


def c_teachin_del(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        models.Teachin.objects.filter(id=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


# 编辑宣讲会
def c_teachin_edit(request):
    if request.method == "GET":
        id = request.GET.get('id')
        teach_list = models.Teachin.objects.filter(id=id).values()
        return render(request, 'company/article_edit.html', locals())
    else:
        show_inf = {'status': True, 'inf': None}
        # 宣讲会
        x_company_id = request.POST.get('x_company_id')
        x_title = request.POST.get('x_title')
        x_id = request.POST.get('x_id')
        x_time = request.POST.get('x_time')
        x_city = request.POST.get('x_city')
        x_school = request.POST.get('x_school')
        x_detail = request.POST.get('x_detail')
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(x_detail, 'html.parser')
        if x_title and x_city and x_school and x_detail:
            models.Teachin.objects.filter(id=x_id).update(
                x_title=x_title,
                x_time=x_time,
                x_city=x_city,
                x_school=x_school,
                x_detail=str(bs),
                x_company_id=x_company_id,
            )

            show_inf['inf'] = '修改宣讲会信息成功'
            show_inf['link'] = '/company/c_teachin?cid=' + x_company_id

        else:
            show_inf['status'] = False
            show_inf['inf'] = '请把信息填写完整，谢谢！'
        res = json.dumps(show_inf)
        return HttpResponse(res)


# 招聘会
def c_zhaopin(request):
    cid = request.GET.get('cid')
    zhaopin_list = models.Zhaopin.objects.filter(z_company_id=cid).values().order_by('-id')
    zhaopin_count = models.Zhaopin.objects.filter(z_company_id=cid).count()
    return render(request, 'company/zhaopin-list.html',
                  {
                      'cid': cid,
                      'zhaopin_list': zhaopin_list,
                      'zhaopin_count': zhaopin_count,
                  })


# 删除招聘信息
def c_zhaopin_del(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        models.Zhaopin.objects.filter(id=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


# 添加招聘会
def c_zhaopin_add(request):
    cid = request.GET.get('cid')
    return render(request, 'company/zhaopin-add.html', locals())


# 添加招聘会提交
def c_zhaopin_add_confirm(request):
    if request.method == "POST":
        show_inf = {'status': True, 'inf': None}

        # 招聘信息
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
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(z_detail, 'html.parser')
        if z_position and z_salary:
            models.Zhaopin.objects.filter().create(
                z_position=z_position,
                z_number=z_number,
                z_salary=z_salary,
                z_education=z_education,
                z_experience=z_experience,
                z_nature=z_nature,
                z_data=z_data,
                z_city=z_city,
                z_email=z_email,
                z_detail=str(bs),
                z_company_id=z_company_id,
            )
            show_inf['inf'] = '发布招聘信息成功'
            show_inf['link'] = '/company/c_zhaopin?cid=' + z_company_id

        else:
            show_inf['status'] = False
            show_inf['inf'] = '请把信息填写完整，谢谢！'
        res = json.dumps(show_inf)
        return HttpResponse(res)


# 编辑招聘信息
def c_zhaopin_edit(request):
    if request.method == "GET":
        id = request.GET.get('id')
        zhaopin_list = models.Zhaopin.objects.filter(id=id).values()
        return render(request, 'company/zhaopin_edit.html', locals())
    else:
        show_inf = {'status': True, 'inf': None}
        # 招聘信息
        z_company_id = request.POST.get('z_company_id')
        z_id = request.POST.get('z_id')
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
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(z_detail, 'html.parser')
        if z_position and z_salary:
            models.Zhaopin.objects.filter(id=z_id).update(
                z_position=z_position,
                z_number=z_number,
                z_salary=z_salary,
                z_education=z_education,
                z_experience=z_experience,
                z_nature=z_nature,
                z_data=z_data,
                z_city=z_city,
                z_email=z_email,
                z_detail=str(bs),
                z_company_id=z_company_id,
            )
            show_inf['inf'] = '修改招聘信息成功'
            show_inf['link'] = '/company/c_zhaopin?cid=' + z_company_id

        else:
            show_inf['status'] = False
            show_inf['inf'] = '请把信息填写完整，谢谢！'
        res = json.dumps(show_inf)
        return HttpResponse(res)


# 完善信息
def c_perfect(request):
    if request.method == 'GET':
        cid = request.GET.get('cid')
        company_list = models.Conpanys.objects.filter(id=cid).values()
        return render(request, 'company/picture-add.html', locals())

    else:
        info = {'status': True, 'mession': None}
        c_id = request.POST.get('id')
        c_name = request.POST.get('c_name')
        c_nature = request.POST.get('c_nature')
        c_city = request.POST.get('c_city')
        c_industry = request.POST.get('c_industry')
        c_scale = request.POST.get('c_scale')
        c_phone = request.POST.get('c_phone')
        c_linkman = request.POST.get('c_linkman')
        c_type = request.POST.get('c_type')
        c_site = request.POST.get('c_site')
        c_time = request.POST.get('c_time')
        c_capital = request.POST.get('c_capital')
        c_manage = request.POST.get('c_manage')
        c_brief = request.POST.get('c_brief')

        from bs4 import BeautifulSoup
        bs = BeautifulSoup(c_brief, 'html.parser')
        if c_time and c_capital and c_linkman:
            models.Conpanys.objects.filter(id=c_id).update(
                c_nature=c_nature,
                c_city=c_city,
                c_industry=c_industry,
                c_scale=c_scale,
                c_phone=c_phone,
                c_linkman=c_linkman,
                c_type=c_type,
                c_site=c_site,
                c_time=c_time,
                c_capital=c_capital,
                c_manage=c_manage,
                c_brief=str(bs),
            )

            info['mession'] = '修改企业信息成功！'
            info['link'] = '/company/c_welcome?cid=' + c_id

        else:
            info['status'] = False
            info['mession'] = '请把信息填写完整，谢谢！'

        res = json.dumps(info)
        return HttpResponse(res)


import os


def create_uuid():
    import uuid
    s_uuid = str(uuid.uuid1())
    l_uuid = s_uuid.split('-')
    uid = ''.join(l_uuid)
    return uid


from jobinfo import settings


def confirm_center(request):
    if request.method == "POST":
        ret = {}
        id = request.POST.get("id")
        avatar_img = request.FILES.get("avatar")
        if avatar_img:
            avatar_uid = create_uuid()
            avatar_img_name = avatar_uid + "." + avatar_img.name.split(".")[1]

            # file_path = os.path.join('static/images/', avatar_img_name)
            # f = open(file_path, 'wb')
            # for line in avatar_img.chunks():
            #     f.write(line)
            # f.close()
            #
            # avatar_url = "http://" + request.get_host() + "/static/images/" + avatar_img_name

            path = os.path.join(settings.MEDIA_ROOT, 'avatars', avatar_img_name)
            with open(path, "wb") as f:
                for line in avatar_img:
                    f.write(line)

            avatar_url = "http://" + request.get_host() + "/media/avatars/" + avatar_img_name

            # print(avatar_url)

            models.Conpanys.objects.filter(id=id).update(
                c_business=avatar_url
            )
            ret["status"] = True
            ret["msg"] = "上传成功！"
        else:
            ret["status"] = False
            ret["msg"] = "上传失败！"

        return JsonResponse(ret)


# 修改密码
def c_password(request):
    if request.method == "GET":
        cid = request.GET.get('cid')
        return render(request, 'company/password-edit.html', locals())
    else:

        info = {'status': '0', 'mession': None}
        id = request.POST.get('id')
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        newpassword2 = request.POST.get('newpassword2')
        c_pwd_int = models.Conpanys.objects.filter(id=id).values()[0]['c_pwd']
        c_pwd = str(c_pwd_int)

        if oldpassword == '' or newpassword == '' or newpassword2 == '':
            info['status'] = '3'
            info['mession'] = '没有做任何修改'
        else:
            if oldpassword == c_pwd:
                if newpassword == newpassword2:
                    models.Conpanys.objects.filter(id=id).update(c_pwd=newpassword)
                    info['mession'] = '修改密码成功！'
                    info['link'] = '/company/c_welcome?cid=' + id
                else:
                    info['status'] = '1'
                    info['mession'] = '两次密码输入不相同'
            else:
                info['status'] = '2'
                info['mession'] = '原密码输入错误'

        res = json.dumps(info)
        return HttpResponse(res)


def upload(request):
    obj = request.FILES.get("upload_img")
    avatar_uid = create_uuid()
    avatar_img_name = avatar_uid + "." + obj.name.split(".")[1]
    flag = ".doc" in obj.name
    if flag:
        path = os.path.join(settings.MEDIA_ROOT, 'add_company_file', avatar_img_name)
    else:
        path = os.path.join(settings.MEDIA_ROOT, 'add_company_img', avatar_img_name)

    print('path', path)

    with open(path, "wb") as f:
        for line in obj:
            f.write(line)

    res = {
        "error": 0,
        "url": "/" + path.split("\\")[4] + "/" + path.split("\\")[5] + "/" + avatar_img_name
    }
    print('res', res)
    return HttpResponse(json.dumps(res))
