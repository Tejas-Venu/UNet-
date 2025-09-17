from django.db import models
from django.utils.timezone import now
from ngos.models import NGO
from users.models import User


class Donation(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    ngo_id = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name='donations')
    date = models.DateTimeField(default=now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

