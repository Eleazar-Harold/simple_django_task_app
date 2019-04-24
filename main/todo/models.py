from django.db import models
from django.shortcuts import reverse
from datetime import datetime, date

# Create your models here.
class Todo(models.Model):
    
    description = models.CharField(max_length=200)
    taskdate = models.DateTimeField(auto_now=False, auto_now_add=False)
    complete = models.BooleanField(default=False)
    expire = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ('taskdate',)
        verbose_name_plural = "Todo"

    def __str__(self):
        return self.description + ' | ' + str(self.complete)

    def get_absolute_url(self):
        return reverse("Todo_detail", kwargs={"pk": self.pk})
