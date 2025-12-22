from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403, handler404, handler500
import users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', users.views.register, name='registration'),
    path('profile/edit/', users.views.edit_profile, name='edit_profile'),
]

handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
