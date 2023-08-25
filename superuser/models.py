from django.db import models

class AdminMessages(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=250)
