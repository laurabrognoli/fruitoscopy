from django.conf.urls import url, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
# from .views import SampleViewSet, ML_ModelViewSet, SP_ModelViewSet, SampleListView, ImageListView
from frutopy import views

'''
router = routers.DefaultRouter()
router.register(r'samples', SampleViewSet)
router.register(r'ml_models', ML_ModelViewSet)
router.register(r'sp_models', SP_ModelViewSet)
'''


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), # login URLs for browsable API
    url(r'^upload/$', 'frutopy.views.upload_file', name='upload_file'),
    url(r'^about/$', 'frutopy.views.about', name='about'),
    url(r'^success/$', 'frutopy.views.success', name='success'),
    url(r'^$', 'frutopy.views.home', name='home'),
    url(r'^samples_list/$', views.SampleListView.as_view(), name='samples_list'),
    url(r'^images_list/$', views.ImageListView.as_view(), name='samples_list'),
    # url(r'^', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)