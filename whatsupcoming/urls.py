from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("eventsearch.views",
		       url(r'^upcoming', 'upcoming'),
                       url(r'^upcoming/(?P<latitude>&<longitude>\d+)/$', 'upcoming'),
                       url(r'^event/(?P<event_id>\d+)/$', 'detail')
)
urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'sup.views.home', name='home'),
    # url(r'^sup/', include('sup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin 
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),

)
