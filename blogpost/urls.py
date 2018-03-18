from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^blog/(?P<slug>[^\.]+).html', views.view_post, name='view_blog_post')
]
