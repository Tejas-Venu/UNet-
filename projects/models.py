from django.db import models


class Project(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Planned', 'Planned'),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')

    def __str__(self):
        return self.title
