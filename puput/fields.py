from django.db import models

from puput.widgets import ColorPickerWidget


class ColorField(models.CharField):
    """
    A CharField which uses the HTML5 color picker widget.
    """

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = ColorPickerWidget
        return super().formfield(**kwargs)
