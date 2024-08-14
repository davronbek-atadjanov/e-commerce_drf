from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models import Media


# Create your models here.


class Category(MPTTModel):
    name = models.CharField(_("name"), max_length=255)
    image = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    class MPTTMeta:
        order_insertion_by = ['name']


class Product(models.Model):
    name = models.CharField(_("name"), max_length=255)
    price = models.FloatField(_("price"))
    short_description = models.CharField(_("short description"), max_length=255)
    description = models.TextField(_("description"))
    quantity = models.IntegerField(_("quantity"))
    instructions = RichTextField(_("instructions"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    in_stock = models.BooleanField(_("in stock"), default=True)
    brand = models.CharField(_("brand"))
    discount = models.IntegerField(_("discount"))
    thumbnail = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    image = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Product: {self.product.id} | Image: {self.image.id}"

    class Meta:
        verbose_name = _("product color")
        verbose_name_plural = _("product colors")


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return f"Product: {self.product.id} | Image: {self.image.id}"

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    value = models.CharField(_("value"), max_length=255)

    def __str__(self):
        return f"Product: {self.product.id} | Size: {self.value}"

    class Meta:
        verbose_name = _("product size")
        verbose_name_plural = _("product sizes")


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=255)
    review = models.TextField(_("review"))
    rank = models.IntegerField(_("rank"), validators=[MinValueValidator(1), MaxValueValidator(5)])
    email = models.EmailField(_("email"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return f"User id:{self.user.id} | rank {self.rank}"

    class Meta:
        verbose_name = _("product review")
        verbose_name_plural = _("product reviews")


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlists")
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"Product: {self.product.id} | User: {self.user.id}"

    class Meta:
        verbose_name = _("wishlist")
        verbose_name_plural = _("wishlists")