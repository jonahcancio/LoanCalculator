# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework import routers
from backend_api import views
from django.contrib import admin

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    # path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', TemplateView.as_view(template_name='index.html')),         
    path('calculator/', views.CalculateView.as_view()),
    path('admin/', admin.site.urls),
]

