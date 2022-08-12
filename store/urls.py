from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter
from pprint import pprint

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

#urlConf
urlpatterns = [
    path('', include(router.urls)),
]