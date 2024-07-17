from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from uuid import uuid4

class UserManager(BaseUserManager):
    '''
        View에서 user_data를 전달 받으면
        받은것으로 DB로 create함
    '''
    def create_user(self, **user_data):
        email = user_data.get('email')
        password = user_data.get('password')
        if not email:
            raise ValueError('이메일 주소를 입력해야합니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **user_data)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    last_login = None
    USERNAME_FIELD = 'internal_uuid'
    REQUIRED_FIELDS = []

    user_role_choices = (
        ('normal', '일반'),
        ('admin', '관리자'),
        ('sub_admin', '부 관리자'),
    )

    gender_choice = (
        ("F", "여자"),
        ("M", "남자")
    )

    # 내부 식별 uuid
    # 내부에서 핸들링할 개인 식별키
    internal_uuid = models.UUIDField(
        default=uuid4,
        unique=True,
        editable=False,
    )

    # 외부 식별 uuid
    # 외부에 노출될 개인 식별키
    # 외부에 노출되어도 영향이 가지않음.
    external_uuid = models.UUIDField(
        default=uuid4,
        unique=True,
    )

    # 이메일 주소
    email = models.EmailField(
        unique=True,
        help_text='이메일 주소'
    )

    password = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=11,
        verbose_name="휴대 번호",
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=30,
        blank=True,
        help_text='성명'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='활성화 여부'
    )

    is_staff = models.BooleanField(
        default=False
    )

    role = models.CharField(
        max_length=10,
        choices=user_role_choices,
        default='user',
        help_text='유저 권한'
    )

    birthday = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name="생년월일",
        default=None
    )

    gender = models.CharField(
        max_length=1,
        choices=gender_choice,
        blank=True,
        null=True,
        verbose_name="성별",
        default=None
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    objects = UserManager()
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set', blank=True)

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = '유저'

    def __str__(self):
        return f"{self.email} {self.name} {self.role}"
