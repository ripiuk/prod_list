from django.conf.urls import url
from . import views

app_name = 'product'

urlpatterns = [
    #/products/
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login_user/$', views.LoginView.as_view(), name='login_user'),
    url(r'^logout_user/$', views.LogoutView.as_view(), name='logout_user'),
    #/products/24_only/
    url(r'^24_only/$', views.Only_TF.as_view(), name='24-only'),
    #/products/<category_slug>/
    url(r'^(?P<category_slug>[\w-]+)/$', views.ProductView.as_view(), name='products'),
    #/products/<category_slug>/<product_slug>/
    url(r'^(?P<category_slug>[\w-]+)/(?P<product_slug>[\w-]+)$', views.OneProductView.as_view(), name='one-product'),

]