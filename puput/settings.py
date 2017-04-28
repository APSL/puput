from django.conf import settings


def get_use_body():
    """
    Returns the value from the Django Project's settings, or the default.
    """
    return getattr(settings, "PUPUT_USE_BODY", True)


def get_use_stream_body():
    """
    Returns the value from the Django Project's settings, or the default.
    """
    return getattr(settings, "PUPUT_USE_STREAM_BODY", True)
