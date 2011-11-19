from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^user/$', 'version1.views.index'),
    url(r'^user/validatepin/$', 'version1.views.validatepin'),
    url(r'^user/options/$', 'version1.views.options'),    
    url(r'^user/balanceenquiry/$', 'version1.views.balanceenquiry'),
    url(r'^user/cashwithdrawal/$', 'version1.views.cashwithdrawal'),
    url(r'^user/mcashwithdrawal/$', 'version1.views.mcashwithdrawal'),
    url(r'^user/cashtransfer/$', 'version1.views.cashtransfer'),
    url(r'^user/mcashtransfer/$', 'version1.views.mcashtransfer'),
    url(r'^user/pinchange/$', 'version1.views.pinchange'),
    #url(r'^user/phonechange/$', 'version1.views.phonechange'),
    url(r'^user/changepin/$', 'version1.views.changepin'),
    #url(r'^user/changephone/$', 'version1.views.changephone'),
    url(r'^user/fastcash/$', 'version1.views.fastcash'),
    url(r'^user/mfastcash/$', 'version1.views.mfastcash'),
    url(r'^user/exit/$', 'version1.views.exit'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
