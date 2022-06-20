from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import *

# Create your models here.


class Project(models.Model):
    # Blank - whenever you change some in form to UPDATE record you can't submit empty field
    owner = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=5000, null=True, blank=True)
    source_link = models.CharField(max_length=5000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    total_votes = models.IntegerField(default=0, null=False, blank=False)
    scores_votes = models.IntegerField(default=0, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(
        default=0, null=False, blank=False, validators=[MinValueValidator(10), MaxValueValidator(10000)])
    id = models.UUIDField(default=uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.price = round(self.price, 2)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        # Set ordering from oldest to newest in QuerySet
        ordering = ['created']


class Review(models.Model):
    VOTE_TYPE = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )

    # Param on_delete working like if we delete some project, every review about it will be delete
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=500, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    docs_link = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
