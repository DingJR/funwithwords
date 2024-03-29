# Generated by Django 2.2.1 on 2019-06-04 04:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('title', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('body', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
        migrations.CreateModel(
            name='BookUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finishDegree', models.PositiveIntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.Book')),
            ],
            options={
                'ordering': ('book', 'user'),
            },
        ),
        migrations.CreateModel(
            name='Etyma',
            fields=[
                ('root', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('meaning', models.CharField(max_length=100)),
                ('words', models.CharField(max_length=1000)),
                ('origin', models.CharField(blank=True, max_length=100, null=True)),
                ('function', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['root'],
            },
        ),
        migrations.CreateModel(
            name='EtymaCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_meaning', models.CharField(max_length=150, unique=True)),
                ('c_meaning', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['e_meaning'],
            },
        ),
        migrations.CreateModel(
            name='Prefix',
            fields=[
                ('affix', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('meaning', models.CharField(blank=True, max_length=100, null=True)),
                ('words', models.CharField(blank=True, max_length=1000, null=True)),
                ('origin', models.CharField(blank=True, max_length=100, null=True)),
                ('function', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['word'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Suffix',
            fields=[
                ('affix', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('meaning', models.CharField(blank=True, max_length=100, null=True)),
                ('words', models.CharField(blank=True, max_length=1000, null=True)),
                ('origin', models.CharField(blank=True, max_length=100, null=True)),
                ('function', models.CharField(blank=True, max_length=200, null=True)),
                ('formtype', models.CharField(max_length=20, null=True)),
            ],
            options={
                'ordering': ['word'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(default=None, max_length=200, null=True)),
                ('joinTime', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('resume', models.CharField(blank=True, max_length=200, null=True)),
                ('WordList', models.CharField(blank=True, max_length=1000, null=True)),
                ('curBook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainsite.Book')),
                ('learnedBook', models.ManyToManyField(related_name='book_learners', through='mainsite.BookUser', to='mainsite.Book')),
            ],
            options={
                'ordering': ('joinTime',),
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('word', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('e_meaning', models.CharField(max_length=100, null=True)),
                ('c_meaning', models.CharField(max_length=100, null=True)),
                ('source', models.TextField(null=True)),
                ('helper', models.CharField(max_length=100, null=True)),
                ('Suffix', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainsite.Suffix')),
            ],
            options={
                'ordering': ['word'],
            },
        ),
        migrations.CreateModel(
            name='WordUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewTimes', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.User')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.Word')),
            ],
            options={
                'ordering': ('word', 'user'),
            },
        ),
        migrations.CreateModel(
            name='WordCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meaning', models.CharField(max_length=100, unique=True)),
                ('words', models.CharField(max_length=1000)),
                ('differ', models.CharField(blank=True, max_length=2000, null=True)),
                ('antonym', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainsite.WordCategory')),
            ],
            options={
                'ordering': ['meaning'],
            },
        ),
        migrations.AddField(
            model_name='word',
            name='category',
            field=models.ManyToManyField(related_name='wordcategory_words', to='mainsite.WordCategory'),
        ),
        migrations.AddField(
            model_name='word',
            name='etyma',
            field=models.ManyToManyField(related_name='etyma_word', to='mainsite.Etyma'),
        ),
        migrations.AddField(
            model_name='word',
            name='prefix',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainsite.Prefix'),
        ),
        migrations.AddField(
            model_name='user',
            name='learnedWord',
            field=models.ManyToManyField(related_name='word_learners', through='mainsite.WordUser', to='mainsite.Word'),
        ),
        migrations.AddField(
            model_name='user',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ThumbRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('thumb_time', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
                ('thumb_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainsite.User')),
            ],
        ),
        migrations.CreateModel(
            name='ThumbCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('thumb_num', models.IntegerField(default=0)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
            ],
        ),
        migrations.AddField(
            model_name='etyma',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_etymas', to='mainsite.EtymaCategory'),
        ),
        migrations.AddField(
            model_name='bookuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.User'),
        ),
        migrations.AddField(
            model_name='book',
            name='words',
            field=models.ManyToManyField(related_name='word_class', to='mainsite.Word'),
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('thumb_num', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.User')),
            ],
            options={
                'ordering': ('-pub_date',),
                'unique_together': {('title', 'author')},
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('BlogPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.BlogPost')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.User')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
    ]
