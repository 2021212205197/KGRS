from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from authentication.views import index

urlpatterns = [
    # 其他路由配置
]

urlpatterns += i18n_patterns(
    path('api/', include('authentication.urls')),
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # 添加根路径的路由
    prefix_default_language=True
)