"""funwithwords URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from mainsite.views import homepage, index, login, register, logout, autoComplextion, searchword, showall,showone, showmypost,displaypost, thumbup
from mainsite.views import editpost, post,deletepost, modifypost, showEtyma, showEtymaCategory, showEtymaClass, showAffix, showAffixCategory, gotoModify, modify
from mainsite.views import getModifyWord,  getModifyWordInfo, todayWords, gotoBook
from mainsite.views import getBook, gotoTodayWords, wordInfo, reviewFinish, changeBook
from mainsite.views import personSetting, createNewComment
#from mainsite.views import showmypost, showallpost, editpost
blogpatterns = [
    re_path('mypost', showmypost),
    re_path('edit/post', post),
    re_path('edit',   editpost),
    re_path('delete/', deletepost),
    re_path('postComment', createNewComment),
    re_path('modify/post(?P<articleid>\w+)', modifypost),
    re_path('community/(?P<author>\w+)/(?P<slug>\w+)/thumbup', thumbup),
    re_path('community/(?P<author>\w+)/(?P<slug>\w+)', displaypost),
    re_path('community/(?P<author>\w+)/thumbup', thumbup),
    re_path('community/(?P<author>\w+)', showone),
    re_path('community', showall),
    path('', showall),
    #re_path('mypost/add', editpost),
    #re_path('mypost/modify', editpost),
    #re_path('community/(?P<slug>\w+)',showAllPost),
]
wordpatterns= [
    #re_path('(?P<word>\w+)/',wordInfo),
    path('', searchword),
]
affixpatterns= [
    re_path('(?P<affixType>\w+)/(?P<affixName>.+)', showAffix),
    re_path('(?P<affixType>\w+)', showAffixCategory),
]
mywordspatterns= [
    path('wordinfo', wordInfo),
    path('reviewFinish',reviewFinish),
    path('getwords', todayWords),
    path('review/', gotoTodayWords),
    re_path('change/(?P<bookname>.+)', changeBook),
    re_path('book/(?P<bookname>.+)', getBook),
    path('book/', gotoBook),
    #path('todaywords/', todayWords),
]
etymapatterns= [
    re_path('category/(?P<category>.+)', showEtymaClass),
    re_path('(?P<root>.+)', showEtyma),
    path('', showEtymaCategory),
]

urlpatterns = [
    path('admin/',  admin.site.urls),
    path('',  index),
    path('index/',  index),
    path('login/',  login),
    path('logout/', logout),
    path('register/',  register),
    path('settings/', personSetting),
    path('autoComplextion/', autoComplextion),
    path('blog/',   include(blogpatterns)),
    re_path('modify/(?P<subtype>\w+)', modify),
    path('modify/', gotoModify),
    path('getModifyWord/', getModifyWord),
    path('getModifyWordInfo/', getModifyWordInfo),
    path('word/',   include(wordpatterns)),
    path('affix/',  include(affixpatterns)),
    path('etyma/',  include(etymapatterns)),
    path('mywords/',include(mywordspatterns)),
    path('filer/',include('filer.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
