from django import forms
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import SetPasswordForm
from user.models import Profile

from rest_framework import serializers, exceptions


UserModel = get_user_model()


class RegisterSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    mobile = serializers.CharField(
        max_length=11,
        min_length=11,
        required=True
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    @staticmethod
    def validate_password1(password):
        min_length = 6
        if min_length and len(password) < min_length:
            raise forms.ValidationError("密码不能少于{0}位".format(min_length))
        validate_password(password)
        return password

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("两次密码不匹配")
        return data

    def get_cleaned_data(self):
        return {
            'mobile': self.validated_data.get('mobile', ''),
            'password1': self.validated_data.get('password1', ''),
        }

    def save(self, request, commit=True):
        user = get_user_model()()
        self.cleaned_data = self.get_cleaned_data()
        user.mobile = self.cleaned_data['mobile']
        if 'password1' in self.cleaned_data:
            user.set_password(self.cleaned_data["password1"])
        else:
            user.set_unusable_password()
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user


class LoginSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    mobile = serializers.CharField(
        max_length=11,
        min_length=11,
        required=True,
        label='手机号码'
    )
    password = serializers.CharField(style={'input_type': 'password'}, label='密码')

    @staticmethod
    def _validate_mobile(mobile, password):
        user = None

        if mobile and password:
            user = authenticate(mobile=mobile, password=password)
        else:
            msg = '必须包含"mobile"和"password"'
            raise exceptions.ValidationError(msg)
        return user

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        password = attrs.get('password')

        user = None
        user = self._validate_mobile(mobile, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = '用户处于非激活状态'
                raise exceptions.ValidationError(msg)
        else:
            msg = '密码与该手机号不匹配'
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = UserModel
        fields = ('id', 'mobile', 'email', 'first_name', 'last_name', 'username')
        read_only_fields = ('mobile', )


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        user_data = UserDetailsSerializer(obj['user'], context=self.context).data
        return user_data


class PasswordChangeSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', True
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
