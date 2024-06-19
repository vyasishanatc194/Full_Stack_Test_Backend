from django.db import models


class ActivityTracking(models.Model):
    """
    This Model will track the values when model has been created or modified 
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
