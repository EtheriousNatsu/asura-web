from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from asura.users import urls as users_urls
from asura.services import urls as services_urls
from asura.steps import urls as steps_urls
from asura.schedules import urls as schedules_urls
from asura.hooks import urls as hooks_urls
from asura.assertions import views as assertions_views
from asura.environments import views as environments_views
from asura.hooks import views as hooks_views
from asura.results import views as results_views
from asura.schedules import views as schedules_views
from asura.services import views as services_views
from asura.steps import views as steps_views
from asura.testcases import views as tests_views
from asura.testsuites import views as testsuites_view

router = DefaultRouter(trailing_slash=False)

router.register(
    'environments',
    environments_views.EnvironmentViewSet,
    base_name='environments',
)
router.register(
    'services',
    services_views.ServiceViewSet,
    base_name='services'
)
router.register(
    'tests',
    tests_views.TestCaseViewSet,
    base_name='tests'
)
router.register(
    'assertions',
    assertions_views.AssertionsViewSet,
    base_name='assertions'
)
router.register(
    'setups',
    steps_views.SetupViewSet,
    base_name='setups'
)
router.register(
    'teardowns',
    steps_views.TeardownViewSet,
    base_name='teardowns'
)
router.register(
    'results',
    results_views.ResultViewSet,
    base_name='results'
)
router.register(
    'testsuites',
    testsuites_view.TestSuiteViewSet,
    base_name='testsuites'
)
router.register(
    'schedules',
    schedules_views.ScheduleViewSet,
    base_name='schedules'
)
router.register(
    'hooks',
    hooks_views.HookViewSet,
    base_name='hooks'
)
urlpatterns = [
    path('', include(users_urls)),
    path('', include(router.urls)),
    path('', include(services_urls)),
    path('', include(steps_urls)),
    path('', include(schedules_urls)),
    path('', include(hooks_urls)),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
