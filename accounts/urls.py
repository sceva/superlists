from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^login$', 'accounts.views.persona_login', name='persona_login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^favicon.ico%', 'django.views.static.serve', ))