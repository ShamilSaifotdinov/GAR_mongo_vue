from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.IntegerField()