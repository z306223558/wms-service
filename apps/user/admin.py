from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from utils.export_excel import export_excel

from apps.user.models import User, Profile


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'subject', 'location', 'date_sent', 'is_read')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('mobile', 'username', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.ser
    """
    password = ReadOnlyPasswordHashField(label='密码')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    verbose_name = '个人信息'
    verbose_name_plural = verbose_name


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [ProfileInline]

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    def get_queryset(self, request):
        """
        用户列表展示中只展示该用户类型能够看到的用户
        :param request:
        :return:
        """
        qs = super().get_queryset(request)
        # if request.user.is_superuser:
        #     return qs.filter(is_teacher=False, is_superuser=False, date_joined__gte='2019-06-26')
        # if request.user.is_teacher:
        #     return qs.filter(date_joined__gte='2019-06-26')
        # return qs.filter(is_teacher=False, is_superuser=False, date_joined__gte='2019-06-26')
        return qs

    def get_user_name(self, obj):
        return obj.profile.name

    get_user_name.short_description = '用户名称'

    def get_user_sex(self, obj):
        if obj.profile.gender == 'F':
            return '女'
        else:
            return '男'

    get_user_sex.short_description = '性别'

    list_display = ('mobile', 'get_user_name', 'get_user_sex', 'date_joined', )
    list_filter = ('mobile', )
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        ('基本信息', {'fields': ('username', 'email', 'last_name', 'first_name')}),
        ('权限控制', {'fields': ('is_superuser', 'groups', 'user_permissions', 'is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2')}
         ),
    )
    search_fields = ('mobile', 'profile__name', )
    ordering = ('date_joined',)
    filter_horizontal = ()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    用户信息管理
    """
    list_display = ('get_user_mobile', 'name', 'age', 'get_user_sign_date',)
    list_related_fields = ('user', )
    search_fields = ('user__mobile', 'name', )
    actions = ["save_excel", ]

    def get_user_sign_date(self, obj):
        return obj.user.date_joined
    get_user_sign_date.short_description = '注册时间'

    def save_excel(self, request, queryset):
        response = export_excel(request, queryset, 'user', Profile)
        return response

    save_excel.short_description = '导出所有数据到excel(请先任意勾选一行数据)'

    def get_user_mobile(self, obj):
        return obj.user.mobile

    get_user_mobile.short_description = '手机号'


admin.site.register(User, UserAdmin)
admin.site.unregister(Site)

# 全局的设定
admin.site.site_title = "WMS管理平台管理"
admin.site.site_header = "WMS管理平台管理"
admin.site.index_title = "WMS管理平台管理"