from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.utility import validate_story_link


# Create your models here.
class Media(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", _("Image")
        VIDEO = "video", _("Video")
        FILE = "file", _("File")
    file = models.FileField(_("File"), upload_to="files/")
    type = models.CharField(_("Type"), max_length=10, choices=MediaType.choices)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Media")


class Setting(models.Model):
    home_image = models.ForeignKey(Media, verbose_name=_("Home Image"), on_delete=models.SET_NULL, null=True, blank=True)
    home_title = models.CharField(_("Home Title"), max_length=120)
    home_subtitle = models.CharField(_("Home Subtitle"), max_length=120)

    def __str__(self):
        return self.home_title

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")


class Country(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    code = models.CharField(_("Code"), max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Region(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="regions")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class OurInstagramStory(models.Model):
    image = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="instagram_stories")
    story_link = models.URLField(_("Story Link"), validators=[validate_story_link])

    def __str__(self):
        return f"Id: {self.id} | Link: {self.story_link}"

    class Meta:
        verbose_name = _("Our Instagram Story")
        verbose_name_plural = _("Our Instagram Stories")


class CustomerFeedback(models.Model):
    description = models.TextField(_("Description"))
    rank = models.IntegerField(_("Rank"), validators=[MinValueValidator(1), MaxValueValidator(5)])
    customer_name = models.CharField(_("Customer Name"), max_length=120)
    customer_position = models.CharField(_("Customer Position"), max_length=120)
    customer_image = models.ForeignKey(Media, on_delete=models.SET_NULL, related_name="feedbacks", null=True, blank=True)

    def __str__(self):
        return self.customer_name

    class Meta:
        verbose_name = _("Customer Feedback")
        verbose_name_plural = _("Customer Feedbacks")
