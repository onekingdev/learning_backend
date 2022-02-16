from django.db import models
from django.utils.text import slugify
from app.models import RandomSlugModel, TimestampModel, IsActiveModel


class Order(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'order_'

    guardian = models.ForeignKey('guardians.Guardian', on_delete=models.CASCADE)
    sub_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount_code = models.CharField(max_length=255, blank=True)
    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=255, choices=(("Card", "Card"), ("PayPal", "PayPal"), ("ApplePay", "ApplePay")), default="Card")
    is_paid = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)


class OrderDetail(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'order_detail_'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    guardian_student_plan = models.ForeignKey('plans.GuardianStudentPlan', on_delete=models.CASCADE, blank=True, null=True)
    plan = models.ForeignKey('plans.Plan', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    period = models.CharField(
        max_length=100,
        choices=(("Monthly", "Monthly"), ("Yearly", "Yearly")),
        default="Monthly"
    )
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)


class PaypalTransaction(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'paypal_transaction_'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    token_id = models.CharField(max_length=255)
    approve_link = models.TextField()
    capture_link = models.TextField()
    is_captured = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)


class CardTransaction(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'card_transaction_'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)
    approve_link = models.TextField()
    is_captured = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)


class PaymentMethod(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'payment_method_'

    guardian = models.ForeignKey('guardians.Guardian', on_delete=models.CASCADE)
    method = models.CharField(max_length=255, choices=(("Card", "Card"), ("PayPal", "PayPal"), ("ApplePay", "ApplePay")), default="Card")
    is_default = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        return super().save(*args, **kwargs)
