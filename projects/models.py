from enum import unique
from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import *


class Project(models.Model):
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
        ordering = ['-total_votes', '-scores_votes']

    @property
    def get_reviewers(self):
        reviewers = self.review_set.all().values_list('owner__id', flat=True)
        return reviewers

    @property
    def get_vote_total(self):
        reviews = self.review_set.all()
        like_vote = reviews.filter(value='like').count()
        total_votes = reviews.count()

        ratio = (like_vote / total_votes) * 100
        self.total_votes = total_votes
        self.scores_votes = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=500, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

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


class Transaction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['project', 'buyer']]

    def __str__(self):
        return self.project.title
