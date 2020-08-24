import os
from environ import Env

env = Env()
env.read_env(env.str("ENV_PATH", default=".env"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", False)
ALLOWED_HOSTS = []

ROOT_URLCONF = "server.urls"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "widget_tweaks",
    "channels",
    "live_chat"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "live_chat/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"
ASGI_APPLICATION = "server.routing.application"

# CACHES = {"default": env.cache_url()}
layers_hosts = []
for addr in env.list("CHANNEL_LAYERS_URLS"):
    host, port = addr.split(":")
    layers_hosts.append((host, int(port)))
del addr, host, port

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             # "hosts": [("127.0.0.1", 6379)],
#             "hosts": layers_hosts,
#         },
#     },
# }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

DATABASES = {"default": env.db_url()}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = env.str("STATIC_URL", "/static/")
LOGIN_URL = "/auth/login"
LOGOUT_URL = "/auth/logout"
LOGIN_REDIRECT_URL = "/"
