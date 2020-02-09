from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    createdDate = models.DateTimeField()
    content = models.TextField()


class DocumentHistory(models.Model):
    title = models.ForeignKey(Document, on_delete=models.CASCADE)
    createdDate = models.DateTimeField()
    content = models.TextField()