from distutils import text_file
from operator import mod
from pyexpat import model
from tkinter import CASCADE
from django.db import models
import uuid

from django.forms import CharField

class Publish(models.Model):
    name = models.TextField(default="")
    author = models.TextField(default="")
    Edition = models.IntegerField(default=1)
    id = models.CharField(default="", primary_key=True, max_length=20)
    quantity = models.IntegerField(default=1)
    book_genre = models.ForeignKey("collection",on_delete=models.CASCADE, blank=True)
    borrowers = models.ManyToManyField("Student", blank=True, related_name="no_of_borrowers")
    TYPES = (
        ('Book', 'Book'),
        ('Article', 'Article'),
        ('Magazine', 'Magazine'),
        ('Project_files', 'Project Files'),
    )
    publish_type = models.CharField(default="Book",max_length=15, choices=TYPES)
    def __str__(self):
        return str(self.name)

class Student(models.Model):
    name = models.TextField(default="")
    roll_no = models.CharField(default="", max_length=50)
    mobile_no = models.CharField(default="", max_length=12)
    def __str__(self):
        return str(self.name)

class collection(models.Model):
    genre = models.TextField(default="")
    def __str__(self):
        return str(self.genre)