# coding=utf-8
from django.db.models import QuerySet
from jet.dashboard.modules import DashboardModule
from user.models import User


class RecentTickets(DashboardModule):
    title = 'Recent tickets'
    title_url = None
    template = 'admin/user/recent_user_add.html'
    limit = 10

    def init_with_context(self, context):
        self.children = User.objects.order_by('-date_joined')[:self.limit]
        for children in self.children:
            children.get_admin_url = '/admin/user/user/{}/change/'.format(children.id)


class UserAddPeerDay(DashboardModule):
    title = '用户增长'
    title_url = None
    template = 'admin/user/peer_user_statistics.html'
    limit = 10

    def init_with_context(self, context):
        self.children = User.objects.order_by('-date_joined')[:self.limit]
        for children in self.children:
            children.get_admin_url = '/admin/user/user/{}/change/'.format(children.id)

