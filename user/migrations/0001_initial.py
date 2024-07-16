# Generated by Django 3.2 on 2024-07-16 14:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('internal_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('external_uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('email', models.EmailField(help_text='이메일 주소', max_length=254, unique=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='휴대 번호')),
                ('name', models.CharField(blank=True, help_text='성명', max_length=30)),
                ('is_active', models.BooleanField(default=True, help_text='활성화 여부')),
                ('is_staff', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('normal', '일반'), ('admin', '관리자'), ('sub_admin', '부 관리자')], default='user', help_text='유저 권한', max_length=10)),
                ('birthday', models.CharField(blank=True, default=None, max_length=8, null=True, verbose_name='생년월일')),
                ('gender', models.CharField(blank=True, choices=[('F', '여자'), ('M', '남자')], default=None, max_length=1, null=True, verbose_name='성별')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일시')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_set', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_permissions_set', to='auth.Permission')),
            ],
            options={
                'verbose_name': '유저',
                'verbose_name_plural': '유저',
            },
        ),
    ]
