from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'apps.views.dashboard', name='dashboard'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'people.views.logout', name='logout'),
    url(r'^workflow/', include('workflow.urls')),
    url(r'^activation/', include('activation.urls')),
    url(r'^shout/', include('shout.urls')),
    url(r'^people/', include('people.urls')),
    url(r'^vote/', include('vote.urls')),
    url(r'^event/', include('event.urls')),
    url(r'^planning/', include('planning.urls')),
    url(r'^activity-ajax/$', 'apps.views.activity_ajax', name='activity-ajax'),
)

urlpatterns += patterns("",
    (r'^robots\.txt$', direct_to_template,
         {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^humans\.txt$', direct_to_template,
         {'template': 'humans.txt', 'mimetype': 'text/plain'}),
    (r'^hacker\.txt$', direct_to_template,
         {'template': 'hacker.txt', 'mimetype': 'text/plain'}),
    (r'^license\.txt$', direct_to_template,
         {'template': 'license.txt', 'mimetype': 'text/plain'}),
    (r'^python\.txt$', direct_to_template,
         {'template': 'python.txt', 'mimetype': 'text/plain'}),
    )


if settings.LOCAL_DEVELOPMENT:
    urlpatterns += staticfiles_urlpatterns()

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )
