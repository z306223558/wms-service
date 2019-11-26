from jet.dashboard.dashboard import Dashboard

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from jet.dashboard import modules
from django.utils.translation import ugettext_lazy as _
from jet.utils import get_admin_site_name
from user.dashboard_modules.dashboard_modules import RecentTickets, UserAddPeerDay

try:
    from django.template.context_processors import csrf
except ImportError:
    from django.core.context_processors import csrf


class DefaultIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.available_children.append(modules.Feed)

        site_name = get_admin_site_name(context)
        # self.children.append(modules.LinkList(
        #     _('快捷操作'),
        #     layout='inline',
        #     draggable=False,
        #     deletable=False,
        #     collapsible=False,
        #     children=[
        #         [_('用户管理'), '/admin/user'],
        #     ],
        #     column=0,
        #     order=0
        # ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('auth.*',),
            column=1,
            order=0
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('历史操作'),
            10,
            column=0,
            order=1
        ))

        # append another link list module for "support".
        self.children.append(RecentTickets(
            _('最新用户'),
            column=2,
            order=1
        ))

        # append another link list module for "support".
        self.children.append(UserAddPeerDay(
            _('用户'),
            column=2,
            order=1
        ))
