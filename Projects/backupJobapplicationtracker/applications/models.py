from django.db import models

class JobApplication(models.Model):
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Applied', 'Applied'),
            ('Interview Scheduled', 'Interview Scheduled'),
            ('Rejected', 'Rejected'),
            ('Selected', 'Selected'),
        ]
    )
    applied_date = models.DateField()

    def __str__(self):
        return f"{self.company} - {self.role}"
