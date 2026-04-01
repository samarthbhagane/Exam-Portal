from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    mcq_score = models.IntegerField(default=0)
    result = models.CharField(max_length=100, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)  # optional but useful

    def __str__(self):
        return f"{self.name} ({self.email})"
