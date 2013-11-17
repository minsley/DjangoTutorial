from django.db import models

# Create your models here.
class Word(models.Model):
	spelling = models.CharField(max_length=30)
	definition = models.CharField(max_length=1000)

class DomainName(models.Model):
	word = models.ForeignKey(Word)
	variation = models.CharField(max_length=40)
	tld = models.CharField(max_length=10)