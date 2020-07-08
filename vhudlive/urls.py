import djoser
from djoser.urls import authtoken

from django.urls import path
from django.conf.urls import include, url, re_path
from django.contrib import admin
from rest_framework_nested import routers

from .views import *

### Router Implemenation ###

router = routers.SimpleRouter()
router.register(r'storages', StorageListView)
router.register(r'data', DataListView, basename='data')
router.register(r'users', UsersView, basename='users')
router.register(r'groups', GroupsView, basename='groups')

storages_router = routers.NestedSimpleRouter(router, r'storages', lookup='storage')
storages_router.register(r'data', StorageDataView, basename='storage-data')


### URL Output regex ###

urlpatterns = (
    path('', PageView.home_page, name='home'),
    path('register', PageView.register_page, name='register_page'),
    path('login', PageView.login_page, name='login_page'),
    path('logout', PageView.logout_page, name='logout_page'),
    path('cart', PageView.cart_page, name='cart_page'),
    path('menu', PageView.menu_page, name='menu_page'),
    #path("add/<str:item_type>/<int:item_id>/<str:item_bigger>", add_to_cart, name="add_to_cart"),
    path('finalize', PageView.make_order, name='make_order'),
    path('all_orders', PageView.all_orders_page, name='all_orders_page'),
    path('order/<int:order_id>/done', PageView.mark_order_as_done, name='mark_order_as_done'),
    path('my_orders', PageView.user_orders_page, name='user_orders_view'),
    #path('clear_cart', PageView.clear_cart, name='clear_cart'),

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(storages_router.urls)),
    url(r'^api/v1/auth/', include(djoser.urls.authtoken)),
    url(r'^admin/', admin.site.urls),
)

'''
urlpatterns = [
    url(r'^api/v1/storages/$', StorageListView.as_view()),
    url(r'^api/v1/storages/(?P<id>[\w.@+-]+)/$', StorageView.as_view()),
    url(r'^api/v1/data/$', DataListView.as_view()),
    url(r'^api/v1/data/(?P<id>[\w.@+-]+)/$', DataView.as_view()),
]
'''
