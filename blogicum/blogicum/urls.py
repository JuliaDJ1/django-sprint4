from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('blog.urls')),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('rules/', TemplateView.as_view(template_name='pages/rules.html'), name='rules'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = TemplateView.as_view(template_name='pages/403csrf.html')
handler404 = TemplateView.as_view(template_name='pages/404.html')
handler500 = TemplateView.as_view(template_name='pages/500.html')