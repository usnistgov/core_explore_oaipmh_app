""" Test settings
"""

SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # Extra apps
    "defender",
    "menu",
    "django_celery_beat",
    # Local apps
    "core_main_app",
    "core_explore_common_app",
    "core_explore_oaipmh_app",
    "core_oaipmh_common_app",
    "core_oaipmh_harvester_app",
    "core_linked_records_app",
    "tests",
]

# SERVER URI
SERVER_URI = "http://example.com"

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Needed by any curator app
                "core_main_app.utils.custom_context_processors.domain_context_processor",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

STATIC_URL = "/static/"
ROOT_URLCONF = "tests.test_urls"

DATA_SORTING_FIELDS = ["+title"]

CUSTOM_NAME = "Curator"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

AUTO_SET_PID = False

MONGODB_INDEXING = False
MONGODB_ASYNC_SAVE = False
ENABLE_SAML2_SSO_AUTH = False
