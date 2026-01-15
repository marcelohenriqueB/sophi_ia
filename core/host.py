from django_hosts import patterns, host

urlpatterns = patterns('',
    host(r'www', 'project.urls', name='www'),
    host(r'app', 'app.urls', name='app'),
    host(r'api', 'api.urls', name='api'),
)