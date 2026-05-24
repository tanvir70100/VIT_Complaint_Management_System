from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from complaints.views import custom_login


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', custom_login, name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', include('complaints.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
