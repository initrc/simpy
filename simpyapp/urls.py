from django.conf.urls import patterns, url

urlpatterns = patterns(
    'simpyapp.views',
    url(r'^$', 'index'),
    url(r'^compare/$', 'compare'),
)
