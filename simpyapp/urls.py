from django.conf.urls import patterns, include, url

urlpatterns = patterns('simpyapp.views',
    # Examples:
    url(r'^$', 'index'),
    url(r'^compare/$', 'compare'),
)
