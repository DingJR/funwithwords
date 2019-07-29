from django.db import models
from django.utils import timezone
from filer.fields.image import FilerImageField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
# Users

class AffixInfo(models.Model):
    affix     = models.CharField(max_length = 30, primary_key = True) #word
    meaning   = models.CharField(max_length = 100, null=True, blank=True)
    words     = models.CharField(max_length = 1000, blank = True, null=True)#examples
    origin    = models.CharField(max_length = 100, blank = True, null=True)#origins
    function  = models.CharField(max_length = 200, blank = True, null=True)#origins

    class Meta:
        abstract = True
        ordering = ['word']

    def __str__(self):
        return self.affix

class Prefix(AffixInfo):
    pass

class Suffix(AffixInfo):
    formtype = models.CharField(max_length = 20, null=True)
    pass

class EtymaCategory(models.Model):
    e_meaning = models.CharField(max_length = 150, unique = True) #English meaning 
    c_meaning = models.CharField(max_length = 100) #Chinese meaning
    class Meta:
        ordering = ['e_meaning']
    def __str__(self):
        return self.e_meaning

class Etyma(models.Model):
    root      = models.CharField(max_length = 30, primary_key= True)  #word
    meaning   = models.CharField(max_length = 100) #English meaning 
    words     = models.CharField(max_length = 1000) #examples
    origin    = models.CharField(max_length = 100, blank = True, null=True) #origins
    function  = models.CharField(max_length = 200, blank = True, null=True) #origins
    category  = models.ForeignKey(EtymaCategory,null=True, related_name='category_etymas', on_delete = models.SET_NULL)#categories of etyma
    class Meta:
        ordering = ['root']
    def __str__(self):
        return self.root

class WordCategory(models.Model):
    meaning   = models.CharField(max_length = 100, unique=True) #English meaning 
    antonym   = models.ForeignKey('WordCategory', null = True, on_delete = models.SET_NULL)
    words     = models.CharField(max_length = 1000) 
    differ    = models.CharField(null=True,blank=True,max_length = 2000) 
    class Meta:
        ordering = ['meaning']
    def __str__(self):
        return self.meaning

class Word(models.Model):
    word      = models.CharField(max_length = 30, primary_key= True)  #word
    e_meaning = models.CharField(max_length = 100, null=True) #English meaning 
    c_meaning = models.CharField(max_length = 100, null=True) #Chinese meaning
    Suffix    = models.ForeignKey(Suffix,null=True, on_delete = models.SET_NULL)#word's suffix
    prefix    = models.ForeignKey(Prefix,null=True, on_delete = models.SET_NULL)          
    etyma     = models.ManyToManyField(Etyma, related_name = "etyma_word") #word's etyma
    source    = models.TextField(null=True)
    helper    = models.CharField(max_length = 100,null=True) #strategy to remember
    category  = models.ManyToManyField(WordCategory, related_name = "wordcategory_words")
    class Meta:
        ordering = ['word']
    def __str__(self):
        return self.word

class Book(models.Model):
    title       = models.CharField(max_length = 200, primary_key = True)
    words       = models.ManyToManyField(Word, related_name='word_class')
    author      = models.CharField(max_length = 200)
    wordNum     = models.PositiveIntegerField(default=0)
    pub_date    = models.DateTimeField(auto_now=True)
    body        = models.TextField(null = True, blank=True)
    image       = FilerImageField(related_name='book_image',null=True,on_delete=models.SET_NULL)
    class Meta:
        ordering = ['pub_date']
    def __unicode__(self):
        return self.title

class WordUser(models.Model):
    user           = models.ForeignKey('User', on_delete=models.CASCADE)
    word           = models.ForeignKey(Word, on_delete=models.CASCADE)
    reviewTimes    = models.PositiveIntegerField(default=0)
    reviewParameter= models.PositiveIntegerField(default=0)
    class Meta :
        ordering = ('word','user')

class BookUser(models.Model):
    user         = models.ForeignKey('User', on_delete=models.CASCADE)
    book         = models.ForeignKey(Book, on_delete=models.CASCADE)
    finishDegree = models.DecimalField(max_digits = 5, decimal_places = 2,default=0.0)
    class Meta :
        ordering = ('book','user')

class User(models.Model):
    name        = models.CharField(max_length = 200, unique = True)
    password    = models.CharField(max_length = 200, null=True, default=None)
    from django.contrib import auth
    user        = models.OneToOneField(auth.models.User, null=True, on_delete=models.CASCADE, related_name='profile')
    joinTime    = models.DateTimeField(auto_now = True)
    email       = models.EmailField(max_length = 40, unique = True)
    resume      = models.CharField(max_length = 200, null=True, blank = True)
    learnedBook = models.ManyToManyField(Book,related_name = "book_learners",through='BookUser')
    learnedWord = models.ManyToManyField(Word,related_name = "word_learners",through='WordUser')
    curBook     = models.ForeignKey(Book, null=True, blank=True, on_delete=models.SET_NULL)
    dayWordNum  = models.PositiveIntegerField(default=100)
    newWordNum  = models.PositiveIntegerField(default=20)
    WordList    = models.CharField(max_length = 1000, null=True,blank = True)
    class Meta :
        ordering = ('joinTime',)
    def __unicode__(self):
        return self.name


class BlogPost(models.Model):
    title    = models.CharField(max_length = 200)
    author   = models.ForeignKey(User,on_delete = models.CASCADE)
    slug     = models.CharField(max_length = 200)
    body     = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    thumb_num= models.PositiveIntegerField(default=0)
    class Meta :
        unique_together=("title", "author")
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.title

class BlogComment(models.Model):
    author   = models.ForeignKey(User, on_delete = models.CASCADE)
    BlogPost = models.ForeignKey(BlogPost, on_delete = models.CASCADE)
    body     = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    class Meta :
        ordering = ('-pub_date',)
    def __unicode__(self):
        return self.author

class ThumbCount(models.Model):
    content_type   = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    thumb_num      = models.IntegerField(default=0)
 
class ThumbRecord(models.Model):
    content_type   = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id      = models.PositiveIntegerField()
    thumb_user     = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    thumb_time     = models.DateTimeField(auto_now = True)


