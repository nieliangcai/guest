from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import render,get_object_or_404
# Create your views here.
def index(request):
    #return HttpResponse('Hello Django!')
    return render(request,'index.html')
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        # if username=='admin' and password == 'admin123':
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)    #调用数据库登录
            # return HttpResponse('Luck! login Success!')
            # return HttpResponseRedirect('/event_manage/')
            response = HttpResponseRedirect('/event_manage/')   #返回页面
            # response.set_cookie('user',username,3600)       #添加浏览器Cookie
            request.session['user'] = username              #记录session
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user','')     #读取浏览器cookie
    username = request.session.get('user','')       #读取服务器session
    event_list = Event.objects.all()
    return render(request,'event_manage.html',{'user':username,
                                               'events':event_list})
@login_required
def search_name(request):           #搜索功能,现在是发布页面和嘉宾页面公用一个search_name，所以这里要修改
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name) #从数据库取得匹配的结果
    # search_realname = request.GET.get('realname','')
    # guest_list = Guest.objects.filter(realname__contains=search_realname)
    return render(request,'event_manage.html',{'user':username,
                                               'events':event_list})
@login_required
def guest_manage(request):
    username = request.session.get('user','')
    # search_name = request.GET.get('name','')
    guest_list = Guest.objects.all()    #获取Guest表中的所有对象
    paginator = Paginator(guest_list,10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,
                                               'guests':contacts})
@login_required
def search_realname(request):
    username = request.session.get('user','')
    search_realname = request.GET.get('realname','')
    guest_list = Guest.objects.filter(realname__contains=search_realname)
    paginator = Paginator(guest_list,10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,
                                               'guests':contacts})

@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)     #同Event.objects.all()，如果对象不存在返回404，比Event.objects.all()高级
    return render(request,'sign_index.html',{'event':event})

@login_required
def sign_index_action(request,eid):
    username = request.session.get('user','')
    event = get_object_or_404(Event,id=eid)
    phone = request.POST.get('phone','')
    sign = request.POST.get('sign','')
    #print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'user':username,
                                                 'event':event,
                                                 'hint':'phone.error'})
    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,'sign_index.html',{'user':username,
                                                 'event':event,
                                                 'hint':'event id or phone'})

    result = Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,
                                                 'hint':'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request,'sign_index.html',{'user':username,
                                                 'event':event,
                                                 'hint':'sign in success!!!',
                                                 'guest':result})
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response