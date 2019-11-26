# coding=utf-8
from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


api_description = """
### 管理员账号
手机号：`13166315160`
密码：`z12369874`

### 后台管理
* [localhost测试](http://127.0.0.1:8000/admin)
* [服务器](http://175.102.18.112:8000/admin)

### 名词释义

"""


schema_view = get_schema_view(
    openapi.Info(
        title="WMS平台API文档",
        default_version='v1',
        description=api_description,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', RedirectView.as_view(url='docs/')),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('user/', include('user.urls')),
    path('docs/',
         schema_view.with_ui('swagger', cache_timeout=None),
         name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework'))
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
