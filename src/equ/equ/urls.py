from django.conf.urls import patterns, include, url
from equ_common.views import Home, Busqueda
from userena import views as userena_views
from django.conf import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^$', Home, name='home'),
                       url(r'^', include('equ_common.urls')),
                       url(r'', include('social_auth.urls')),
                       url(r'^accounts/', userena_views.signup, name='accounts'),
                       url(r'^activate/(?P<activation_key>\w+)/$', userena_views.activate, name='userena_activate'),
                       url(r'^search/', Busqueda, name='search'),
                       #url(r'^search/',include('haystack.urls')),
                       url(r'^your_uploads/', include('multiuploader.urls')),
                       #url(r'^accounts/',include('userena.urls')),
                       #url(r'^register/$', RegisterUser, name="register")
                       # url(r'^equ/', include('equ.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       )
"""
urlpatterns = patterns('haystack.views',
    url(r'^search/',SearchView(
        template = 'equ_common/templates/search/search.html',
        form_class = 'Busqueda',
        ), name='haystack_search'),
)
"""


#urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
                            url(r'^static/(?P<path>.*)$', 'serve'),
                            )
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
