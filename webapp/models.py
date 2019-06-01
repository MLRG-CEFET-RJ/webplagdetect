# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Document(models.Model):
	content = models.TextField()
	
class Sentence(models.Model):
	fragment = models.TextField()
	article = models.ForeignKey(Document, on_delete=models.CASCADE)
	
	