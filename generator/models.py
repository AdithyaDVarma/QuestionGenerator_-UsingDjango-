from django.db import models
from jsonfield import JSONField
class History(models.Model):
    username = models.CharField(max_length=150)  # Username of the user uploading the file
    filename = models.CharField(max_length=255)  # Name of the uploaded file
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically set to the current date and time on creation
    json_file = models.JSONField()  # Stores the JSON data

    def __str__(self):
        return f"{self.username} - {self.filename}"
