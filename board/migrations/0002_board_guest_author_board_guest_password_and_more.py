# Generated by Django 4.2.14 on 2024-08-21 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='guest_author',
            field=models.CharField(help_text='작성자(비회원)', max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='guest_password',
            field=models.CharField(help_text='비회원 작성자 암호', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='board',
            name='author',
            field=models.ForeignKey(help_text='작성자(유저)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='boards', to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
        ),
        migrations.AlterField(
            model_name='board',
            name='category',
            field=models.CharField(choices=[('notice', '공지사항'), ('general', '일반 게시판'), ('qna', '질문 게시판')], help_text='카테고리', max_length=10, verbose_name='카테고리'),
        ),
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.CharField(help_text='게시글 제목', max_length=100, verbose_name='제목'),
        ),
    ]
