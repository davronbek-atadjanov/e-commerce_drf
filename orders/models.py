from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class CartItem(models.Model):
    user = models.ForeignKey("accounts.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("products.Product", verbose_name=_("Product"), on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(_("Quantity"))
    subtotal = models.FloatField(_("Subtotal"))

    def __str__(self):
        return f"{self.user.id} - {self.product.name}"

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")


class Card(models.Model):
    user = models.ForeignKey("accounts.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="cards")
    card_name = models.CharField(_("Card Name"), max_length=120)
    card_number = models.CharField(_("Card Number"), max_length=16)
    expiry_date = models.DateField(_("Expiry Date"))
    cvv = models.CharField(_("CVV"), max_length=3)

    def __str__(self):
        return f"{self.user.id} - {self.card_number}"

    class Meta:
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")


class Discount(models.Model):
    code = models.CharField(_("Code"), max_length=60)
    max_limit_price = models.FloatField(_("Max Limit Price"))
    percentage = models.FloatField(_("Percentage"))
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")


class Branch(models.Model):
    name = models.CharField(_("Name"), max_length=120)
    region = models.ForeignKey("common.Region", on_delete=models.CASCADE, related_name="branches")
    zip_code = models.CharField(_("Zip Code"), max_length=10)
    street = models.CharField(_("Street"), max_length=120)
    address = models.TextField(_("Address"))
    longitude = models.FloatField(_("Longitude"))
    latitude = models.FloatField(_("Latitude"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")


class DeliveryTariff(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="delivery_tariffs")
    high = models.FloatField(_("High"))
    width = models.FloatField(_("Width"))
    weight = models.FloatField(_("Weight"))
    price = models.FloatField(_("Price"))
    regions = models.ManyToManyField("common.Region", related_name="delivery_tariffs")
    delivery_time = models.TimeField(_("Delivery Time"))

    def __str__(self):
        return f"{self.branch.name} - {self.price}"

    class Meta:
        verbose_name = _("Delivery Tariff")
        verbose_name_plural = _("Delivery Tariffs")


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CREATED = "created", _("Created")
        IN_PROGRESS = "in_progress", _("In progress")
        DELIVERED = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")
        FINISHED = "finished", _("Finished")

    class PaymentStatus(models.TextChoices):
        CREATED = "created", _("Created")
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        CANCELLED = "cancelled", _("Cancelled")

    class PaymentMethod(models.TextChoices):
        CASH = "cash", _("Cash")
        CLICK = "click", _("Click")
        PAYME = "payme", _("Payme")

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(_("Status"), max_length=20, choices=OrderStatus.choices)
    items = models.ManyToManyField(CartItem, related_name="orders")
    total_price = models.FloatField(_("Total Price"))
    address = models.ForeignKey("accounts.UserAddress", on_delete=models.CASCADE, related_name="orders")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, related_name="orders", null=True, blank=True)
    payment_status = models.CharField(_("Payment Status"), max_length=20, choices=PaymentStatus.choices)
    payment_method = models.CharField(_("Payment Method"), max_length=20, choices=PaymentMethod.choices)
    delivery_tariff = models.ForeignKey(DeliveryTariff, on_delete=models.SET_NULL, related_name="orders", null=True, blank=True)
