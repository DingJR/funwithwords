from django.contrib import admin
from .models import BlogPost,Prefix,Suffix,Etyma,EtymaCategory,Word,WordCategory,Book,User,BlogPost,BlogComment
from .models import BookUser, WordUser

# Register your models here.
class Prefix_Admin(admin.ModelAdmin):
    list_display = ('affix', 'meaning', 'origin', 'words')
class Suffix_Admin(admin.ModelAdmin):
    list_display = ('affix', 'meaning', 'formtype','origin', 'words')
class Etyma_Admin(admin.ModelAdmin):
    list_display = ('root', 'meaning', 'category', 'origin', 'words')
class EtymaCategory_Admin(admin.ModelAdmin):
    list_display = ('e_meaning', 'c_meaning')
class WordCategory_Admin(admin.ModelAdmin):
    list_display = ('meaning','words','differ')
class Book_Admin(admin.ModelAdmin):
    list_display = ('title', 'body')
class Word_Admin(admin.ModelAdmin):
    list_display = ('word', 'e_meaning', 'c_meaning')
class User_Admin(admin.ModelAdmin):
    list_display = ('user','name', 'email', 'resume')
class BlogComment_Admin(admin.ModelAdmin):
    list_display = ('author', 'BlogPost', 'body')
class BlogPost_Admin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'pub_date', 'author', 'pub_date')
class BookUser_Admin(admin.ModelAdmin):
    list_display = ('book', 'user', 'finishDegree')
#admin.site.register(Prefix,Prefix_Admin)
#admin.site.register(Suffix,Suffix_Admin)
#admin.site.register(Etyma,Etyma_Admin)
admin.site.register(EtymaCategory,EtymaCategory_Admin)
#admin.site.register(WordCategory,WordCategory_Admin)
admin.site.register(Book,Book_Admin)
#admin.site.register(Word,Word_Admin)
admin.site.register(User,User_Admin)
#admin.site.register(BlogComment,BlogComment_Admin)
admin.site.register(BlogPost,BlogPost_Admin)
#admin.site.register(BookUser,BookUser_Admin)
