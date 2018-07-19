from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^process_login', views.process_login),
    url(r'^success$', views.success),
    url(r'^products/(?P<product_id>\d+)/buy/', views.buy_product),
    url(r'^checkout/', views.checkout)
]
