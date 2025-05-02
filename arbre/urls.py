from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, FamilyRelationViewSet
from django.conf.urls.static import static
from django.conf import settings
from .views import run_algorithm

router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'relations', FamilyRelationViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/run-algorithm/', run_algorithm, name='run_algorithm'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)