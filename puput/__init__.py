__author__ = "Marc Tudurí"
__email__ = "marctc@gmail.com"
__version__ = "2.0.0"

PUPUT_APPS = (
    # Wagtail apps
    "wagtail.contrib.legacy.richtext",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.snippets",
    "wagtail.users",
    "wagtail.images",
    "wagtail.embeds",
    "wagtail.search",
    "wagtail.sites",
    "wagtail.contrib.redirects",
    "wagtail.contrib.forms",
    "wagtail.contrib.sitemaps",
    "wagtail.contrib.routable_page",
    "wagtail",
    # Third-party apps
    "taggit",
    "modelcluster",
    "django_social_share",
    # Puput apps
    "puput",
    "wagtailmarkdown",
)

default_app_config = "puput.apps.PuputAppConfig"
