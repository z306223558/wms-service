from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, mobile, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        if not mobile:
            raise ValueError('The given mobile must be set')
        user = self.model(
            mobile=mobile, is_staff=False, is_active=True,
            is_superuser=False,
            last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        u = self.create_user(mobile, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    mobile and password are required. Other fields are optional.
    """
    username = models.CharField(max_length=20, verbose_name="用户名", blank=True)
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号码")
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('是否有权限进入后台管理界面'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            '账号是否被激活'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    date_update = models.DateTimeField(_('更新时间'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'mobile'

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = '账号信息'
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'


class Profile(models.Model):
    """
    Dummy profile model used for testing
    """
    user = models.OneToOneField(User, related_name="profile",
                                on_delete=models.CASCADE)
    MALE, FEMALE = 'M', 'F'
    choices = (
        (MALE, '男'),
        (FEMALE, '女'))
    gender = models.CharField(max_length=1, choices=choices,
                              verbose_name='性别')
    name = models.CharField(max_length=100, verbose_name="用户姓名")
    age = models.PositiveIntegerField(verbose_name='年龄', blank=True)
    avatar = models.ImageField(verbose_name="头像", upload_to="avatar", default="avatar/user.6102e21.jpg")
    tel_info = models.CharField(verbose_name="联系方式", max_length=20)
    birthday = models.CharField(verbose_name="出生年月日", max_length=100)

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Profile'
