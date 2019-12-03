#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from rest_framework import exceptions


User = get_user_model()


if hasattr(User, 'REQUIRED_FIELDS'):
    if not (User.USERNAME_FIELD == 'mobile' or 'mobile' in User.REQUIRED_FIELDS):
        raise ImproperlyConfigured(
            "MobileAuthBackend: Your User model must have an mobile"
            " field with blank=False")


class UsernameAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        if username is None:
            if 'username' not in kwargs or kwargs['username'] is None:
                return None
            clean_mobile = kwargs['username']
        else:
            clean_mobile = username

        matching_users = User.objects.filter(username__iexact=clean_mobile)
        if len(matching_users) == 0:
            raise exceptions.ValidationError('用户名不存在')
        authenticated_users = [
            user for user in matching_users if user.check_password(password)]
        if len(authenticated_users) == 1:
            # Happy path
            return authenticated_users[0]
        elif len(authenticated_users) > 1:
            # This is the problem scenario where we have multiple users with
            # the same email address AND password. We can't safely authenticate
            # either.
            raise User.MultipleObjectsReturned(
                "There are multiple users with the given mobile and "
                "password")
        raise exceptions.ValidationError('密码不正确')


class MobileAuthBackend(ModelBackend):
    def authenticate(self, request, mobile=None, password=None, **kwargs):
        if mobile is None:
            if 'username' not in kwargs or kwargs['username'] is None:
                return None
            clean_mobile = kwargs['username']
        else:
            clean_mobile = mobile

        # Check if we're dealing with an mobile
        if len(clean_mobile) != 11:
            return None

        # Since Django doesn't enforce emails to be unique, we look for all
        # matching users and try to authenticate them all. Note that we
        # intentionally allow multiple users with the same email address
        # (has been a requirement in larger system deployments),
        # we just enforce that they don't share the same password.
        # We make a case-insensitive match when looking for emails.
        matching_users = User.objects.filter(mobile__iexact=clean_mobile)
        if len(matching_users) == 0:
            raise exceptions.ValidationError('手机号未注册')
        authenticated_users = [
            user for user in matching_users if user.check_password(password)]
        if len(authenticated_users) == 1:
            # Happy path
            return authenticated_users[0]
        elif len(authenticated_users) > 1:
            # This is the problem scenario where we have multiple users with
            # the same email address AND password. We can't safely authenticate
            # either.
            raise User.MultipleObjectsReturned(
                "There are multiple users with the given mobile and "
                "password")
        raise exceptions.ValidationError('密码不正确')
