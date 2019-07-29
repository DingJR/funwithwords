 # -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.forms.models import model_to_dict
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from datetime import datetime
from . import models
from .models import BlogPost,Word, ThumbRecord, ThumbCount
from mainsite import forms
from django.http import Http404, HttpResponseNotFound

import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request, pid = None ,del_pass= None):
    template = get_template('index.html')
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        message = "cookie supported"
    else :
        message = 'cookie not supported'
    user = None
    if request.session.get('is_login',None):
        user_id = request.session.get('user_id')
        user = models.User.objects.get(pk=user_id)
    request.session.set_test_cookie()
    html = template.render(locals())
    return HttpResponse(html)

@csrf_exempt
def register(request):
    template = get_template('index.html')
    user = None
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']
            passwordCheck = form.cleaned_data['passwordCheck']
            try:
                if(password != passwordCheck):
                    message = "两次密码不正确！"
                    registerFailMessage = True
                    html = template.render(locals())
                    return HttpResponse(html)
                else :
                    same_user  = models.User.objects.filter(name=username)
                    same_email = models.User.objects.filter(email=email)
                    if same_user:
                        message = "用户名已经存在！"
                    elif same_email:
                        message = "邮箱已经注册"
                    if same_email or same_user:
                        registerFailMessage = True
                        html = template.render(locals())
                        return HttpResponse(html)
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                new_user = models.User.objects.create(name=username, email=email, password = password, user=user)
                new_user.save()
                request.session['is_login'] = True
                request.session['user_name'] = new_user.name
                request.session['user_id'] = new_user.pk
                request.session['user_password'] = new_user.password
                request.session['user_email'] = new_user.email
                user = new_user
                return redirect('/index/')
            except:
                message = "未知错误！"
                registerFailMessage = False
    registerform = forms.RegisterForm(request.POST)
    html = template.render(locals())
    return HttpResponse(html)


@csrf_exempt
def login(request):
    if request.session.get('is_login',None):
        return redirect('/index')
    message = "Begin"
    loginFailMessage = 0
    user = None
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
    else :
        form = forms.LoginForm()
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            user = models.User.objects.get(name=username)
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_name'] = user.name
                request.session['user_id'] = user.pk
                request.session['user_password'] = user.password
                request.session['user_email'] = user.email
                group = Group.objects.get(name='teacher')
                try :
                    group.user_set.get(username=username)
                    request.session['is_teacher'] = True
                except:
                    pass
                return redirect('/index/')
            else:
                message = "密码不正确！"
                loginFailMessage = 1
        except:
            message = "用户不存在！"
            loginFailMessage = 1
    else :
        message = "用户信息获取失败"
        loginFailMessage = 1
    userform = forms.LoginForm(request.POST)
    template = get_template('index.html')
    html = template.render(locals())
    return HttpResponse(html)

@csrf_exempt
def personSetting(request):
    message = "Begin"
    loginFailMessage = 0
    user_id = request.session.get('user_id')
    username= request.session.get('username')
    form = None
    if request.method == 'POST':
        form = forms.SettingsForm(request.POST)
    else :
        form = forms.SettingsForm()
    if form.is_valid():
        try:
            newpassword = form.cleaned_data['password']
            newemail    = form.cleaned_data['email']
            user = models.User.objects.get(pk=user_id)
            group = Group.objects.get(name='teacher')
            user.password = newpassword
            user.email    = newemail
            user.save()
            request.session['user_password'] = newpassword
            request.session['user_email'] = newemail
            message = "修改成功！"
        except:
            message = "用户名已使用！"
            loginFailMessage = 1
    else :
        message = "用户信息获取失败"
        loginFailMessage = 1
    template = get_template('index.html')
    html = template.render(locals())
    return HttpResponse(html)


@csrf_exempt
def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')


'''
Blog District
'''


@csrf_exempt
def homepage(request):
    template = get_template('index.html')
    posts = BlogPost.objects.all()
    now = datetime.now()
    html = template.render(locals())
    return HttpResponse(html)


def showall(request):
    template = get_template('blog.html')
    try:
        posts = BlogPost.objects.all()
        if posts is not None:
            html = template.render(locals())
            return HttpResponse(html)
    except:
        return redirect('/')


def showone(request, author):
    template = get_template('blog.html')
    try:
        user = models.User.objects.filter(name=author)
        posts = None
        for i in user:
            posts = i.blogpost_set.all()
        if posts is not None:
            html = template.render(locals())
            return HttpResponse(html)
    except:
        return redirect('/')


@csrf_exempt
def showmypost(request):
    template = get_template('blog.html')
    is_login = request.session['is_login']
    username = request.session['user_name']
    password = request.session['user_password']
    author   = models.User.objects.filter(name=username)
    if not is_login:
        return redirect('/')
    try:
        user  = models.User.objects.filter(name = username)
        posts = None
        for i in user:
            posts = i.blogpost_set.all()
        if posts != None:
            html = template.render(locals())
            return HttpResponse(html)
    except :
        return redirect('/')

@csrf_exempt
def deletepost(request):
    try:
        deletepost_id = (request.POST)["localName"]
        d = models.BlogPost.objects.get(pk=deletepost_id).delete()
        from django.http import JsonResponse
        return JsonResponse('success', safe=False)
    except:
        return redirect('/blog/mypost')


@csrf_exempt
def displaypost(request,author,slug):
    template = get_template('displaypost.html')
    try:
        user_id = models.User.objects.get(name=author)
        article = BlogPost.objects.get(slug=slug, author_id=user_id)
        blogcomments = models.BlogComment.objects.filter(BlogPost=article)
        if article != None:
            html = template.render(locals())
            return HttpResponse(html)
    except :
        return redirect('/')

def message_response(status="SUCCESS",message="SUCCESS", AddData = None):
    data = {}
    data['status']   = status
    data['message']  = message
    data['thumbnum'] = AddData
    return JsonResponse(data)

@csrf_exempt
def createNewComment(request):
    if not request.session.get('is_login',None):
        return message_response(status="FAIL",message='评论需要先登录')
    article = (request.POST)["article"]
    author  = (request.POST)["author"]
    body    = (request.POST)["body"]
    user_id = (request.POST)["user_id"]
    slug    = (request.POST)["slug"]
    user    = models.User.objects.get(pk=user_id)
    author  = models.User.objects.get(pk=author)
    article = models.BlogPost.objects.get(title=article)
    comment = models.BlogComment.objects.create(author=user , BlogPost=article, body=body)
    comment.save()
    return displaypost(request, author=author.name, slug=slug)

def thumbup(request,author,slug):
    if not request.session.get('is_login',None):
        return message_response(status="FAIL",message='点赞需要先登录')
    user         = request.session.get("user_id")
    user         = models.User.objects.get(id=user)
    content_type = request.GET.get('content_type')
    content_type = models.ContentType.objects.get(model=content_type)
    object_id    = request.GET.get('object_id')
    is_thumb     = request.GET.get('is_thumb')
    if is_thumb == '0':
        thumb_record  = ThumbRecord.objects.filter(content_type=content_type, object_id=object_id, thumb_user=user)
        thumb_counts  = ThumbCount.objects.filter(content_type=content_type, object_id=object_id)
        thumb_count = None
        num = 0
        for i in thumb_counts:
            num = i.thumb_num
        if thumb_record :
            return message_response(status="nochange" ,message="1", AddData = num)
        else :
            return message_response(status="nochange" ,message="0", AddData = num)

    thumb_record,created = ThumbRecord.objects.get_or_create(content_type=content_type, object_id=object_id, thumb_user=user)
    thumb_count,createdCount  = ThumbCount.objects.get_or_create(content_type=content_type, object_id=object_id)
    message = ""
    if created:
        thumb_record.content_type = content_type
        thumb_record.object_id    = object_id
        thumb_record.thumb_user   = user
        thumb_record.save()
        thumb_count.thumb_num     += 1
        message                   = "1"
    else :
        thumb_record.delete()
        thumb_count.thumb_num      -= 1
        message                   = "-1"
    thumb_count.save()
    post = models.BlogPost.objects.get(id=object_id)
    post.thumb_num = thumb_count.thumb_num
    post.save()
    return message_response(message=message, AddData=thumb_count.thumb_num)


def modifypost(request, articleid):
    template = get_template("editblog.html")
    form = forms.EditForm()
    try:
        article = models.BlogPost.objects.get(id = articleid)
        data = {
                'title':article.title,
                'slug':article.slug,
                'body':article.body
                }
        form = forms.EditForm(data)
        html = template.render(context = locals())
        return HttpResponse(html)
    except:
        redirect('blog/mypost')

def editpost(request):
    template = get_template("editblog.html")
    form = forms.EditForm()
    html = template.render(context = locals())
    return HttpResponse(html)


@csrf_exempt
def post(request):
    if not request.session.get("is_login") :
        return HttpResponseNotFound("None")
    if request.method == 'POST':
        form       = forms.EditForm(request.POST)
        blogpostid = request.POST.get("blogpostid")
    else :
        form = forms.EditForm()
    if not form.is_valid():
        template = get_template("editblog.html")
        message = "信息不全"
        html = template.render(locals())
        return HttpResponse(html)
    author = request.session.get("user_id")
    if author:
        if blogpostid:
            post = models.BlogPost.objects.get(pk=blogpostid)
            post.body = form.cleaned_data['body']
            post.slug = form.cleaned_data['slug']
            post.title= form.cleaned_data['title']
            tempPost = models.BlogPost.objects.exclude(id=post.pk).filter(title=post.title,author_id=author)
            if tempPost:
                template = get_template("editblog.html")
                message = "文章名或介绍名重复"
                html = template.render(locals())
                return HttpResponse(html)
            else :
                post.save()
        else:
            post,create = models.BlogPost.objects.get_or_create(title=form.cleaned_data['title'],author_id=author)
            if not create:
                template = get_template("editblog.html")
                message = "文章名或介绍名重复"
                html = template.render(locals())
                return HttpResponse(html)
            post.body = form.cleaned_data['body']
            post.slug = form.cleaned_data['slug']
            post.title= form.cleaned_data['title']
            post.save()
            message = "成功存储"
    return redirect("/blog/mypost/")



@csrf_exempt
def autoComplextion(request):
    d = None
    try:
        prefixToFound = (request.POST)["localName"]
        from django.core.serializers import serialize
        d = models.Word.objects.filter().extra(where=["word like \'" + prefixToFound + "%%\'"])
        ans = []
        for i in d:
            ans.append({"localName":i.word + " " + i.c_meaning})
        from django.http import JsonResponse
        return JsonResponse(ans, safe=False)
    except:
        return HttpResponse(d)

def searchword(request):
    '''
    f = open('/home/dingjr/Web/spider/ECDICT/resemble.txt','r')
    state = 0
    words = ''
    meaning = ''
    differ = ''
    last_meaning = ''
    gre = {}
    import re
    for line in f.readlines():
        try:
            if state == 0:
                if line[0] == '%':
                    temp = line[1:].strip().split(', ')
                    last_meaning = temp[-1]
                    for i in temp:
                        words += i + ';'
                else :
                    continue
                state = 1
            elif state == 1:
                if not re.match('(-|-).*',line):
                    m = re.match('.*“(.*)”.*',line)
                    meaning = m.group(1)
                else :
                    meaning = last_meaning
                    differ += line
                state = 2
            elif state == 2:
                if line[0] != '-' and line[0] != '-':
                    state = 0
                    gre[meaning] = words.split(';')[0:-1]
                    meaning = ''
                    differ = ''
                    words = ''
                else:
                    differ += line
        except:
            continue
    allwords = models.Word.objects.filter()
    iii=0
    for w in allwords:
        for (k,v) in gre.items():
            if w.word in v:
                print(w.word,iii)
                iii += 1
                w.category.add(models.WordCategory.objects.get(meaning=k))
    '''

    word = None
    result = None
    template = get_template('word.html')
    if request.method == 'GET':
        word = request.GET.get('mainSearch')
        if not word :
            word = request.GET.get('searchHeader')
        try:
            result = Word.objects.get(word = word)
            cleanMeaning = []
            temp = ''
            noDigitMeaning = ''
            i = 0
            while i<len(result.e_meaning):
                if result.e_meaning[i].isdigit():
                    temp = ''
                    temp += result.e_meaning[i]
                    i += 1
                    while i<len(result.e_meaning) and not result.e_meaning[i].isdigit():
                        temp += result.e_meaning[i]
                        i += 1
                    cleanMeaning.append(temp)
                else:
                    noDigitMeaning += result.e_meaning[i]
                    i += 1
            if noDigitMeaning != '':
                cleanMeaning.append(noDigitMeaning)
            result.e_meaning = cleanMeaning
            result.c_meaning = result.c_meaning.split()
        except:
            redirect('/')
    classWord = []
    differ = ''
    try:
        for cat in result.category.all():
            newCat= models.WordCategory.objects.get(meaning=cat)
            temp = newCat.words.split(';')
            for i in temp:
                if i not in classWord:
                    classWord.append(i)
            differ += newCat.differ + '\n'
    except:
        pass
    wordEtymaList = []
    try:
        for ele in result.etyma.all():
            wordEtymaList.append({"root":ele.root,"meaning":ele.meaning})
    except:
        pass
    html = template.render(locals())
    return HttpResponse(html)


'''
affix and root function
'''

def showEtymaCategory(request):
    template = get_template('etyma.html')
    categorys = models.EtymaCategory.objects.all()
    categorywords = {}
    for ele in categorys:
        temp = ele.category_etymas.all()[0:5]
        words = []
        for etyma in temp:
            words.append(etyma)
        categorywords[ele.e_meaning] = words
    html = template.render(locals())
    return HttpResponse(html)

def showEtymaClass(request, category):
    template = get_template('etyma_category.html')
    etymas = None
    allwords= {}
    try:
        if category == 'ALL':
            etymas = models.Etyma.objects.all()
        else:
            category = models.EtymaCategory.objects.get(e_meaning=category)
            etymas = category.category_etymas.all()
        for ele in etymas:
            wordGroup = ele.words.replace('\'','').replace(']','').replace('[','').strip(' ').split(',')
            allwords[ele.root] = wordGroup
    except:
        return redirect('/etyma/')
    html = template.render(locals())
    return HttpResponse(html)


def showEtyma(request, root):
    template = get_template('etyma_show.html')
    #categorys = models.EtymaCategory.objects.all()
    etyma = None
    try:
        etyma = models.Etyma.objects.get(pk = root)
        temp = etyma.words.replace('\'','').replace(']','').replace('[','').replace(' ','').split(',')
        etyma.words = temp
        print(temp)
    except:
        return redirect('/etyma/')
    html = template.render(locals())
    return HttpResponse(html)

#showPrefixCategory, showSuffixCategory, showPrefix, showSuffix
def showAffix(request, affixType, affixName):
    template = get_template('affix_show.html')
    affix = None
    try:
        if affixType == 'suffix':
            affix = models.Suffix.objects.get(pk = affixName)
        elif affixType == 'prefix':
            affix = models.Prefix.objects.get(pk = affixName)
        temp = affix.words.replace('\'','').replace(']','').replace('[','').replace(' ','').split(',')
        affix.words = temp
    except:
        return redirect('/affix/'+affixType)
    html = template.render(locals())
    return HttpResponse(html)

def showAffixCategory(request, affixType):
    template = get_template('affix.html')
    affixes = None
    allwords= {}
    try:
        if affixType == 'prefix':
            affixes = models.Prefix.objects.all()
        else :
            affixes = models.Suffix.objects.all()
        temp = []
        for ele in affixes:
            wordGroup = ele.words.replace('\'','').replace(']','').replace('[','').strip(' ').split(',')
            allwords[ele.affix] = wordGroup[0:5]
    except:
        return redirect('/')
    html = template.render(locals())
    return HttpResponse(html)


'''

modify words

'''


def gotoModify(request):
    template = get_template('modify.html')
    formWord = forms.ModifyWordForm()
    formRoot = forms.ModifyEtymaForm()
    html     = template.render(locals())
    return HttpResponse(html)


@csrf_exempt
def getModifyWord(request):
    d = None
    try:
        prefixToFound = (request.POST)["localName"]
        searchType    = (request.POST)["searchType"]
        from django.core.serializers import serialize
        ans = []
        if searchType == 'root':
            d = models.Etyma.objects.filter().extra(where=["root like \'" + prefixToFound + "%%\'"])
            for i in d:
                ans.append({"localName":i.root})
        elif searchType == 'prefix':
            d = models.Prefix.objects.filter().extra(where=["affix like \'" + prefixToFound + "%%\'"])
            for i in d:
                ans.append({"localName":i.affix})
        elif searchType == 'suffix':
            d = models.Suffix.objects.filter().extra(where=["affix like \'" + prefixToFound + "%%\'"])
            for i in d:
                ans.append({"localName":i.affix})
        elif searchType == 'word':
            d = models.Word.objects.filter().extra(where=["word like \'" + prefixToFound + "%%\'"])
            for i in d:
                ans.append({"localName":i.word})
        from django.http import JsonResponse
        return JsonResponse(ans, safe=False)
    except:
        return HttpResponse(d)

@csrf_exempt
def getModifyWordInfo(request):
    d = {}
    try:
        toFind     = (request.POST)["localName"]
        searchType = (request.POST)["searchType"]
        temp = None
        if searchType == 'root':
            temp = models.Etyma.objects.get(root=toFind)
        elif searchType == 'prefix':
            temp = models.Prefix.objects.get(affix=toFind)
        elif searchType == 'suffix':
            temp = models.Suffix.objects.get(affix=toFind)
        elif searchType == 'word':
            temp = models.Word.objects.get(word=toFind)
            d['e_meaning'] = temp.e_meaning
            d['c_meaning'] = temp.c_meaning
            d['helper'] = temp.helper
            d['source'] = temp.source
        if searchType != 'word':
            d['meaning'] = temp.meaning
            d['function'] = temp.function
            d['words'] = temp.words
            d['origin'] = temp.origin
        from django.core.serializers import serialize
        from django.http import JsonResponse
        return JsonResponse(d, safe=False)
    except:
        return HttpResponse(d)

@csrf_exempt
def modify(request,subtype):
    if not request.session.get("is_teacher") :
        return HttpResponseNotFound("None")
    form = None
    modifyType = subtype
    if modifyType == 'word':
        form = forms.ModifyWordForm(request.POST)
    else :
        form = forms.ModifyEtymaForm(request.POST)
    if not form.is_valid():
        template = get_template('modify.html')
        formWord = forms.ModifyWordForm()
        formRoot = forms.ModifyEtymaForm()
        message = "信息不全"
        html     = template.render(locals())
        return HttpResponse(html)
    ele = None
    if modifyType == 'word':
        word = form.cleaned_data['word']
        e_meaning = form.cleaned_data['e_meaning']
        c_meaning = form.cleaned_data['c_meaning']
        source   = form.cleaned_data['source']
        helper   = form.cleaned_data['helper']
        ele ,created=  models.Word.objects.get_or_create(word=word)
        ele.e_meaning = e_meaning
        ele.c_meaning=c_meaning
        ele.source=source
        ele.helper=helper
    else:
        root     = form.cleaned_data['root']
        meaning  = form.cleaned_data['meaning']
        words    = form.cleaned_data['words']
        function = form.cleaned_data['function']
        origin   = form.cleaned_data['origin']
        if modifyType == 'etyma':
            ele,created = models.Prefix.objects.get_or_create(etyma=root)
        elif modifyType == 'suffix':
            ele,created = models.Suffix.objects.get_or_create(affix=root)
        elif modifyType == 'prefix':
            ele,created = models.Prefix.objects.get_or_create(affix=root)
        ele.meaning = meaning
        ele.words   = words
        ele.function= function
        ele.origin  = origin
    ele.save()
    return redirect('/modify')

def gotoBook(request):
    if not request.session.get("is_login") :
        return HttpResponseNotFound("None")
    template = get_template('book.html')
    user_id  = request.session['user_id']
    try:
        user     = models.User.objects.get(pk=user_id)
        curBook  = user.curBook
        currentBook = {}
        currentBook['title'] = curBook.title
        currentBook['wordnum'] = curBook.wordNum
        currentBook.update({'finishDegree':models.BookUser.objects.get(user=user_id, book=curBook.title).finishDegree})
        currentBook['url'] = curBook.image.url
    except:
        pass
    allbooks = [] 
    books = models.BookUser.objects.filter(user=user_id)
    for ele in books:
        ele_book = models.Book.objects.get(title=ele.book.title)
        book = {}
        try:
            if ele_book.wordNum == 0:
                ele_book.wordNum = len(ele_book.words.all())
            book['title'] = ele_book.title
            book['url'] = ele_book.image.url
            book['wordnum'] = ele_book.wordNum
            book['finishDegree'] = ele.finishDegree
        except:
            continue
        allbooks.append(book)
    categorybooks = []
    for ele in models.Book.objects.all():
        book = {}
        book['title'] = ele.title
        book['url'] = ele.image.url
        book['wordnum'] = len(ele.words.all())
        book['pub_date'] = ele.pub_date
        categorybooks.append(book)
    html     = template.render(locals())
    return HttpResponse(html)


def getBook(request,bookname):
    if not request.session.get("is_login") :
        return HttpResponseNotFound("None")
    user_id  = request.session['user_id']
    book  = None
    words = None
    isMyBook = None
    wordnum = None
    try:
        book = models.Book.objects.get(title=bookname)
        isMyBook = models.BookUser.objects.get(book_id=book, user_id=user_id)
        words = book.words.all()
    except:
        pass
    template = get_template('book_show.html')
    html     = template.render(locals())
    return HttpResponse(html)

def gotoTodayWords(request):
    if not request.session.get("is_login") :
        return HttpResponseNotFound("None")
    user_id  = request.session['user_id']
    user     = models.User.objects.get(pk=user_id)
    curBook  = user.curBook
    template = get_template('review.html')
    html     = template.render(locals())
    return HttpResponse(html)

@csrf_exempt
def todayWords(request):
    if not request.session.get("is_login") :
        return HttpResponseNotFound("None")
    user_id  = request.session['user_id']
    user     = models.User.objects.get(pk=user_id)
    curBook  = user.curBook
    allwords = curBook.words.all()
    reviewWords = []
    userwords = []             #the user's learned words
    queryUserWords = {}        #word-user info
    myword = models.WordUser.objects.filter(user_id=user_id)
    for ele in myword:
        userwords.append(ele.word_id)
        queryUserWords[ele.word_id] = ele
    userwords = set(list(userwords))
    for word in allwords:
        user_word_review_para  = 0
        user_word = None
        try:
            if word.word not in userwords:
                user_word = models.WordUser.objects.create(word_id=word, user_id = user_id)
                user_word.save()
            else:
                user_word_review_para = queryUserWords[word.word].reviewParameter
                user_word_review_times= queryUserWords[word.word].reviewTimes
            if  user_word_review_times< 6:   # learn once, review 5 times
                reviewWords.append((word.word,user_word_review_para))
        except:
            continue
    result = []
    itWordNum = 0
    itNewWordNum = 0
    newWordNum = user.newWordNum
    dayWordNum = user.dayWordNum
    for ele in reviewWords:         # new word
        if ele[1] == 0:
            itNewWordNum += 1
            itWordNum += 1
            result.append(ele[0])
        if itNewWordNum== newWordNum:
            break 
    for ele in reviewWords:
        if itWordNum == dayWordNum:
            break 
        if ele[1] in [1,2,3,5,7]:
            itWordNum += 1
            result.append(ele[0])
    for ele in reviewWords:
        if itWordNum == dayWordNum:
            break 
        if ele[1] not in [1,2,3,5,7] and ele[1]!=0:
            itWordNum += 1
            result.append(ele[0])
    from django.http import JsonResponse
    for i in range(len(result)):
        result[i] += ','
    result = "".join(result)
    d = {'words': result}
    return JsonResponse(d, safe=False)


@csrf_exempt
def wordInfo(request):
    try:
        word = (request.POST)["localName"]
        ans = {}
        d = models.Word.objects.get(word=word)
        ans['word'] = d.word
        ans['e_meaning'] = d.e_meaning
        ans['c_meaning'] = d.c_meaning
        ans['source'] = d.source
        ans['helper'] = d.helper
        from django.http import JsonResponse
        return JsonResponse(ans, safe=False)
    except:
        pass

@csrf_exempt
def reviewFinish(request):
    if not request.session.get("is_login") :
        return HttpResponseNotFound("None")
    user_id  = request.session['user_id']
    words = (request.POST)["words"]
    curBook = (request.POST)["curBook"]
    words = eval(words)    
    curBook      = models.Book.objects.get(title=curBook)
    bookUser     = models.BookUser.objects.get(book_id=curBook.title, user_id = user_id)
    userWordsObj = models.WordUser.objects.filter(user_id=user_id)
    userWords = {}
    allWords = curBook.words.all()
    for ele in userWordsObj:
        userWords[ele.word_id] = ele
    for word in allWords:
        wordObj = userWords[word.word]
        if wordObj.reviewParameter != 0:
            wordObj.reviewParameter += 1
            wordObj.save()
    for word in words:
        wordObj = userWords[word]
        wordObj.reviewTimes += 1
        if wordObj.reviewParameter == 0:
            wordObj.reviewParameter += 1
        wordObj.save()
    learnedWords = 0
    for word in allWords:
        wordObj = userWords[word.word]
        learnedWords += wordObj.reviewTimes
    bookUser.finishDegree = float(learnedWords)*6.0/float(curBook.wordNum)
    bookUser.save()
    return JsonResponse({"message":"success"}, safe=False)

def changeBook(request, bookname):
    if not request.session.get("is_login") :
        return HttpResponseNotFound("None")
    user_id  = request.session['user_id']
    user     = models.User.objects.get(pk=user_id)
    bookuser,create = models.BookUser.objects.get_or_create(user_id=user_id, book_id=bookname)
    if create:
        bookuser.save()
    curBook  = models.Book.objects.get(title=bookname)
    user.curBook = curBook
    user.save()
    return redirect('/mywords/book')
