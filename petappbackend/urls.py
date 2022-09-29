"""petappbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from acountinfo.controllers import auth_controller
from ecommerce.controllers.cart import cart_controller
from ecommerce.controllers.order import order_controller
from ecommerce.controllers.others import category_controller, product_image_controller, item_controller, article_controller
from ecommerce.controllers.product import product_controller

api = NinjaAPI()
api.add_router('/auth', auth_controller)
api.add_router('/products', product_controller)
api.add_router('/carts', cart_controller)
api.add_router('/orders', order_controller)
api.add_router('/categories', category_controller)
api.add_router('/product-images', product_image_controller)
api.add_router('/items', item_controller)
api.add_router('/articles', article_controller)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
