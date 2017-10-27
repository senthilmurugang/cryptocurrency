from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

test = patterns('',
    url(r'^static_content', 'cryptocurrency.views.static_content', name='static_content'),
    url(r'^json_response', 'cryptocurrency.views.json_response', name='json_response'),
)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cryptocurrency.views.home', name='home'),
    url(r'^test/', include(test)),
    # url(r'^cryptocurrency/', include('cryptocurrency.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
