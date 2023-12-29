from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, MerchantViewSet, KeywordViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'merchants', MerchantViewSet)
router.register(r'keywords', KeywordViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
