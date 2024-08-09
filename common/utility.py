from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_story_link(value):
    if not value.startswith("https://"):
        raise ValidationError(_('Invalid URL: %(value)s. The link must start with "https://".'))

    domain_site = "instagram.com"
    pattern = r"https:\/\/(?:www\.)?" + re.escape(domain_site) + r"\/.*"
    if not re.match(pattern, value):
        raise ValidationError(_('Invalid URL: %(value)s. The link must be an Instagram story link.'))
