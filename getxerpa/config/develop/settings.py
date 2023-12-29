# pylint: disable=wildcard-import,unused-wildcard-import
from getxerpa.config.settings import *  # noqa: F403


DEBUG = config('DEBUG', cast=bool, default=True)  # noqa: F405


INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'getxerpa.config.develop.urls'

INSTALLED_APPS += [  # noqa: F405
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE += [  # noqa: F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

AUTH_PASSWORD_VALIDATORS = []
