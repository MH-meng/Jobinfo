from django.shortcuts import render, redirect, HttpResponse
from info.form.login import StudentForm
from info.form.register import RegisterForm
import json
from info import models
import hashlib
from django.http import JsonResponse


def login(request):
    if request.method == 'GET':
        obj_form = StudentForm()
        return render(request, 'students/login.html', {'obj_form': obj_form})
    else:
        obj_form = StudentForm(request.POST)
        # 是否全部验证成功
        if obj_form.is_valid():
            # 用户提交的数据
            snumber = obj_form.cleaned_data['number']
            spwds = str(obj_form.cleaned_data['pwd'])
            spwd = hashlib.md5(spwds.encode(encoding='UTF-8')).hexdigest()
            sret = models.StudentInfo.objects.filter(snumber=snumber, spwd=spwd).count()
            check_code = request.POST.get('checkcode')
            # 从session中获取验证码
            session_code = request.session["CheckCode"]

            if sret == 0:
                obj_form.error_class = "用户账号或密码错误，请重新输入。。。。"
                return render(request, 'students/login.html', {'obj_form': obj_form})
            elif check_code.strip().lower() != session_code.lower():
                error_ver = "验证码错误，请重新输入。。。。"
                return render(request, 'students/login.html', {'obj_form': obj_form, 'error_ver': error_ver})
            else:
                request.session['is_login1'] = True
                request.session['snumber'] = snumber
                request.session['status'] = "students"
                return redirect('/')
        else:
            return render(request, 'students/login.html', {'obj_form': obj_form})


def register(request):
    if request.method == 'GET':
        obj_form = RegisterForm()
        return render(request, 'students/register.html', {'obj_form': obj_form})
    else:
        obj_form = RegisterForm(request.POST)
        info = {'status': None}
        # 是否全部验证成功
        if obj_form.is_valid():
            # 用户提交的数据
            sname = obj_form.cleaned_data['name']
            snumber = obj_form.cleaned_data['number']
            spwds = str(obj_form.cleaned_data['pwd'])

            from hashlib import md5
            md5 = md5()
            md5.update(spwds.encode('utf8'))
            spwd = md5.hexdigest()

            count = models.StudentInfo.objects.filter(snumber=snumber).count()
            if count == 0:
                models.StudentInfo.objects.create(
                    sname=sname,
                    snumber=snumber,
                    spwd=spwd,
                )
                return redirect('/students/success/')
            else:
                info['status'] = '账号已存在，无需重新注册，请返回登录界面！'
                return render(request, 'students/register.html', {'obj_form': obj_form, 'info': info})
        else:
            return render(request, 'students/register.html', {'obj_form': obj_form})


def success(request):
    return render(request, 'students/succes.html')


def logout(request):
    del request.session["is_login1"]
    return redirect('/')


def index(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        student = models.StudentInfo.objects.filter(id=sid).values()
        return render(request, 'students/index.html', {"student": student, 'sid': sid})


def welcome(request):
    sid = request.GET.get('sid')
    students = models.StudentInfo.objects.filter(id=sid).values()
    return render(request, 'students/welcome.html', {"students": students})


# 修改信息
def supdateinfo(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        students = models.StudentInfo.objects.filter(id=sid).values()
        return render(request, 'students/updateInfo.html', {'students': students})
    else:
        info = {'status': True, 'mession': None}
        sid = request.POST.get('id')
        sgender = request.POST.get('sgender')
        sborthday = request.POST.get('sborthday')
        sphone = request.POST.get('sphone')
        sarea = request.POST.get('sarea')
        startwork = request.POST.get('startwork')
        semail = request.POST.get('semail')
        sstatus = request.POST.get('sstatus')
        if sgender and sborthday and sphone and sarea and semail and sstatus:
            models.StudentInfo.objects.filter(id=sid).update(
                sgender=sgender,
                sborthday=sborthday,
                sphone=sphone,
                sarea=sarea,
                startwork=startwork,
                semail=semail,
                sstatus=sstatus,
            )

            info['mession'] = '修改学生信息成功！'
            info['link'] = '/students/welcome?sid=' + sid
        else:
            info['status'] = False
            info['mession'] = '修改失败，请填写完整信息！'
        res = json.dumps(info)
        return HttpResponse(res)


# 工作经验
def workexperiencelist(request):
    sid = request.GET.get('sid')
    work = models.WorkExperience.objects.filter(wstudentid=sid).values().order_by('-id')
    coutnt = work.count()
    return render(request, 'students/workexperiencelist.html', {'work': work, 'coutnt': coutnt, 'sid': sid})


def workexperienceadd(request):
    if request.method == "GET":
        sid = request.GET.get('sid')
        return render(request, 'students/workexperienceadd.html', {"sid": sid})
    else:
        info = {'status': True, 'mession': None}
        sid = request.POST.get('sid')
        wcompanyname = request.POST.get('wcompanyname')
        wstartwork = request.POST.get('wstartwork')
        wendwork = request.POST.get('wendwork')
        wpost = request.POST.get('wpost')
        wbranch = request.POST.get('wbranch')
        windustry = request.POST.get('windustry')
        wcompanyscale = request.POST.get('wcompanyscale')
        wcompanyquality = request.POST.get('wcompanyquality')
        wjobdesc = request.POST.get('wjobdesc')
        if wcompanyname and wpost and wbranch and windustry and wcompanyscale and wcompanyquality and wjobdesc:
            models.WorkExperience.objects.filter().create(
                wcompanyname=wcompanyname,
                wstartwork=wstartwork,
                wendwork=wendwork,
                wpost=wpost,
                wbranch=wbranch,
                windustry=windustry,
                wcompanyscale=wcompanyscale,
                wcompanyquality=wcompanyquality,
                wjobdesc=wjobdesc,
                wstudentid_id=sid,
            )
            info['mession'] = '添加成功！'
            info['link'] = '/students/workexperiencelist?sid=' + sid
        else:
            info['status'] = False
            info['mession'] = '添加失败，请填写完整信息！'
        res = json.dumps(info)
        return HttpResponse(res)


def workexperiencedel(request):
    if request.method == "POST":
        id = request.POST.get('id')
        models.WorkExperience.objects.filter(id=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


def workexperienceupd(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        student = models.WorkExperience.objects.filter(id=id).values()
        return render(request, 'students/workexperienceupd.html', {'student': student, 'id': id})
    else:
        info = {'status': True, 'mession': None}
        id = request.POST.get('id')
        wstudentid_id = request.POST.get('wstudentid_id')
        wcompanyname = request.POST.get('wcompanyname')
        wstartwork = request.POST.get('wstartwork')
        wendwork = request.POST.get('wendwork')
        wpost = request.POST.get('wpost')
        wbranch = request.POST.get('wbranch')
        windustry = request.POST.get('windustry')
        wcompanyscale = request.POST.get('wcompanyscale')
        wcompanyquality = request.POST.get('wcompanyquality')
        wjobdesc = request.POST.get('wjobdesc')
        if wcompanyname and wpost and wbranch and windustry and wcompanyscale and wcompanyquality and wjobdesc:
            models.WorkExperience.objects.filter(id=id).update(
                wcompanyname=wcompanyname,
                wstartwork=wstartwork,
                wendwork=wendwork,
                wpost=wpost,
                wbranch=wbranch,
                windustry=windustry,
                wcompanyscale=wcompanyscale,
                wcompanyquality=wcompanyquality,
                wjobdesc=wjobdesc,
                wstudentid_id=wstudentid_id,
            )
            info['mession'] = '修改成功！'
            info['link'] = '/students/workexperiencelist?sid=' + wstudentid_id
        else:
            info['status'] = False
            info['mession'] = '修改失败，请填写完整信息！'
        res = json.dumps(info)
        return HttpResponse(res)


# 教育经历
def educationexperiencelist(request):
    sid = request.GET.get('sid')
    education = models.EducationExperience.objects.filter(estudentid=sid).values().order_by('-id')
    coutnt = education.count()
    return render(request, 'students/educationexperiencelist.html', locals())


def educationexperienceadd(request):
    if request.method == "GET":
        sid = request.GET.get('sid')
        return render(request, 'students/educationexperienceadd.html', {"sid": sid})
    else:
        info = {'status': True, 'mession': None}
        sid = request.POST.get('sid')
        estarttime = request.POST.get('estarttime')
        eendtime = request.POST.get('eendtime')
        eschool = request.POST.get('eschool')
        ebackground = request.POST.get('ebackground')
        emajor = request.POST.get('emajor')
        if estarttime and eendtime and eschool and ebackground:
            models.EducationExperience.objects.filter().create(
                estarttime=estarttime,
                eendtime=eendtime,
                eschool=eschool,
                ebackground=ebackground,
                emajor=emajor,
                estudentid_id=sid,
            )
            info['mession'] = '添加成功！'
            info['link'] = '/students/educationexperiencelist?sid=' + sid
        else:
            info['status'] = False
            info['mession'] = '添加失败，请填写完整信息！'
        res = json.dumps(info)
        return HttpResponse(res)


def educationexperiencedel(request):
    if request.method == "POST":
        id = request.POST.get('id')
        models.EducationExperience.objects.filter(id=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


def educationexperienceupd(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        education = models.EducationExperience.objects.filter(id=id).values()
        return render(request, 'students/educationexperienceupd.html', {'education': education, 'id': id})
    else:
        info = {'status': True, 'mession': None}
        id = request.POST.get('id')
        estudentid = request.POST.get('estudentid_id')
        estarttime = request.POST.get('estarttime')
        eendtime = request.POST.get('eendtime')
        eschool = request.POST.get('eschool')
        ebackground = request.POST.get('ebackground')
        emajor = request.POST.get('emajor')
        if estarttime and eendtime and eschool and ebackground:
            models.EducationExperience.objects.filter(id=id).update(
                estarttime=estarttime,
                eendtime=eendtime,
                eschool=eschool,
                ebackground=ebackground,
                emajor=emajor,
                estudentid_id=estudentid,
            )
            info['mession'] = '修改成功！'
            info['link'] = '/students/educationexperiencelist?sid=' + estudentid
        else:
            info['status'] = False
            info['mession'] = '修改失败，请填写完整信息！'
        res = json.dumps(info)
        return HttpResponse(res)


# 求职意见
def jobintensionlist(request):
    sid = request.GET.get('sid')
    job = models.JobIntension.objects.filter(jstudentid=sid).values().order_by('-id')
    coutnt = job.count()
    return render(request, 'students/jobintensionlist.html', locals())


def jobintensionadd(request):
    if request.method == "GET":
        sid = request.GET.get('sid')
        return render(request, 'students/jobintensionadd.html', {"sid": sid})
    else:
        info = {'status': True, 'mession': None}
        sid = request.POST.get('sid')
        jarea = request.POST.get('jarea')
        jpost = request.POST.get('jpost')
        jjobtype = request.POST.get('jjobtype')
        jsalary = request.POST.get('jsalary')
        if jarea and jpost and jjobtype and jsalary:
            models.JobIntension.objects.filter().create(
                jarea=jarea,
                jpost=jpost,
                jjobtype=jjobtype,
                jsalary=jsalary,
                jstudentid_id=sid,
            )
            info['mession'] = '添加成功！'
            info['link'] = '/students/jobintensionlist?sid=' + sid
        else:
            info['status'] = False
            info['mession'] = '添加失败，请填写完整信息！'
        res = json.dumps(info)
        return HttpResponse(res)


def jobintensiondel(request):
    if request.method == "POST":
        id = request.POST.get('id')
        models.JobIntension.objects.filter(id=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


def jobintensionupd(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        job = models.JobIntension.objects.filter(id=id).values()
        return render(request, 'students/jobintensionupd.html', {'job': job, 'id': id})
    else:
        info = {'status': True, 'mession': None}
        id = request.POST.get('id')
        jstudentid_id = request.POST.get('jstudentid_id')
        jarea = request.POST.get('jarea')
        jpost = request.POST.get('jpost')
        jjobtype = request.POST.get('jjobtype')
        jsalary = request.POST.get('jsalary')
        if jarea and jpost and jjobtype and jsalary:
            models.JobIntension.objects.filter(id=id).update(
                jarea=jarea,
                jpost=jpost,
                jjobtype=jjobtype,
                jsalary=jsalary,
                jstudentid_id=jstudentid_id,
            )
            info['mession'] = '添加成功！'
            info['link'] = '/students/jobintensionlist?sid=' + jstudentid_id
        else:
            info['status'] = False
            info['mession'] = '修改失败，请填写完整信息！'
        res = json.dumps(info)
        return HttpResponse(res)


# 工作经验
def projectexperiencelist(request):
    sid = request.GET.get('sid')
    project = models.ProjectExperience.objects.filter(pstudentid=sid).values().order_by('-id')
    coutnt = project.count()
    return render(request, 'students/projectexperiencelist.html', locals())


def projectexperienceadd(request):
    if request.method == "GET":
        sid = request.GET.get('sid')
        return render(request, 'students/projectexperienceadd.html', {"sid": sid})
    else:
        info = {'status': True, 'mession': None}
        sid = request.POST.get('sid')
        pstarttime = request.POST.get('pstarttime')
        pendtime = request.POST.get('pendtime')
        pprojectname = request.POST.get('pprojectname')
        pprojectdesc = request.POST.get('pprojectdesc')
        if pstarttime and pendtime and pprojectname and pprojectdesc:
            models.ProjectExperience.objects.filter().create(
                pstarttime=pstarttime,
                pendtime=pendtime,
                pprojectname=pprojectname,
                pprojectdesc=pprojectdesc,
                pstudentid_id=sid,
            )
            info['mession'] = '添加成功！'
            info['link'] = '/students/projectexperiencelist?sid=' + sid
        else:
            info['status'] = False
            info['mession'] = '添加失败，请填写完整信息！'

        res = json.dumps(info)
        return HttpResponse(res)


def projectexperiencedel(request):
    if request.method == "POST":
        id = request.POST.get('id')
        models.ProjectExperience.objects.filter(id=id).delete()
        ret = {}
        ret["status"] = 1
        return JsonResponse(ret)


def projectexperienceupd(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        project = models.ProjectExperience.objects.filter(id=id).values()
        return render(request, 'students/projectexperienceupd.html', {'project': project, 'id': id})
    else:
        info = {'status': True, 'mession': None}
        id = request.POST.get('id')
        pstudentid_id = request.POST.get('pstudentid_id')
        pstarttime = request.POST.get('pstarttime')
        pendtime = request.POST.get('pendtime')
        pprojectname = request.POST.get('pprojectname')
        pprojectdesc = request.POST.get('pprojectdesc')
        if pstarttime and pendtime and pprojectname and pprojectdesc:
            models.ProjectExperience.objects.filter(id=id).update(
                pstarttime=pstarttime,
                pendtime=pendtime,
                pprojectname=pprojectname,
                pprojectdesc=pprojectdesc,
                pstudentid_id=pstudentid_id,
            )
            info['mession'] = '修改成功！'
            info['link'] = '/students/projectexperiencelist?sid=' + pstudentid_id
        else:
            info['status'] = False
            info['mession'] = '修改失败，请填写完整信息！'

        res = json.dumps(info)
        return HttpResponse(res)
