from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

test = patterns('',
    url(r'^static-content', 'cryptocurrency.views.static_content', name='static_content'),
    url(r'^json-response', 'cryptocurrency.views.json_response', name='json_response'),
    url(r'^collections', 'cryptocurrency.views.collections', name='collections'),
    url(r'^post-request', 'cryptocurrency.views.post_request', name='post-request')
)
update = patterns('',
    url(r'^rates', 'cryptocurrency.views.rates', name='rates')
)

rate_patterns = patterns('',
    url(r'^history', 'cryptocurrency.views.history', name='history')
)

view = patterns('',
    url(r'^bitcoin/', include(rate_patterns))
)

auth = patterns('',
    url(r'^callback', 'cryptocurrency.views.auth_callback', name='auth_callback'),
    url(r'^authorize', 'cryptocurrency.views.authorize', name='authorize'),
    url(r'^refresh-token', 'cryptocurrency.views.refresh_token', name='refresh_token')
)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cryptocurrency.views.home', name='home'),
    url(r'^test/', include(test)),
    url(r'^update/', include(update)),
    url(r'^view/', include(view)),
    url(r'^auth/', include(auth))
    # url(r'^cryptocurrency/', include('cryptocurrency.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
