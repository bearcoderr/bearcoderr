from django.core.exceptions import ValidationError
from django.db.models import ImageField
from django.utils.translation import gettext_lazy as _

class SVGImageField(ImageField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value:
            file_extension = value.name.split('.')[-1]
            if file_extension.lower() != 'svg':
                raise ValidationError(_('Only SVG images are allowed.'))

    def formfield(self, **kwargs):
        from django.forms import FileField
        defaults = {'form_class': FileField}
        defaults.update(kwargs)
        return super().formfield(**defaults)