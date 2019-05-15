from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    start_date = models.DateField('Start date')
    competency = models.CharField(max_length=256)


class Project(models.Model):
    name = models.CharField(max_length=256)
    members = models.ManyToManyField(Staff)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class TaskStatus(Enum):
    CLOSED = "Closed"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    TERMINATED = "Terminated"


class Task(models.Model):
    name = models.CharField(max_length=256, default='')
    description = models.CharField(max_length=1024, default='')
    start_date = models.DateField('Start date')
    due_date = models.DateField('Due date')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    staff_pic = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_pic')
    deliverable = models.FileField('Deliverable', blank=True, null=True, upload_to='deliverable/')
    status = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in TaskStatus])
    history = HistoricalRecords()

    def get_status(self):
        if self.status == "TaskStatus.CLOSED":
            return "Closed"
        elif self.status == "TaskStatus.IN_PROGRESS":
            return "In Progress"
        elif self.status == "TaskStatus.COMPLETED":
            return "Completed"
        elif self.status == "TaskStatus.TERMINATED":
            return "Terminated"
        else:
            return ""

