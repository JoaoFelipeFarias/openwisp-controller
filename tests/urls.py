from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from openwisp_utils.admin_theme.admin import admin, openwisp_admin

from portal import views as portal_views

openwisp_admin()

redirect_view = RedirectView.as_view(url=reverse_lazy('admin:index'))

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('openwisp_controller.urls')),
    url(r'^$', redirect_view, name='index'),
    url(r'^portal/sign_up/', portal_views.PortalSignup.as_view()),
    url(r'^portal/login/', portal_views.PortalLogin.as_view()),
    url(r'^portal/logout/', portal_views.PortalLogout.as_view()),
    url(r'^portal/radius_return/', portal_views.PortalLogout.as_view()),
    url(r'^tmp/', portal_views.RegisterTmp.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
