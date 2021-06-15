from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
import pgcrypto


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = pgcrypto.EncryptedDateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = pgcrypto.EncryptedCharField(key="datekey", validators=[phone_regex], max_length=17, verbose_name='Телефон')
    address = pgcrypto.EncryptedCharField(key="datekey", blank=True, null=True)
    postal_code = pgcrypto.EncryptedCharField(key="datekey", blank=True, null=True)
    city = pgcrypto.EncryptedCharField(key="datekey", blank=True, null=True)
    region = pgcrypto.EncryptedCharField(key="datekey", blank=True, null=True)

    def __str__(self):
        return (self.user.username)


class TemporaryBanIp(models.Model):
    class Meta:
        db_table = "TemporaryBanIp"

    ip_address = models.GenericIPAddressField("IP адрес")
    attempts = models.IntegerField("Неудачных попыток", default=0)
    time_unblock = models.DateTimeField("Время разблокировки", blank=True)
    status = models.BooleanField("Статус блокировки", default=False)

    def __str__(self):
        return self.ip_address