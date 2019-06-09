# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Document(models.Model):
	content = models.TextField()
	
	def __str__(self):
		s = self.content[:50] + '...' if len(self.content) > 50 else self.content
		return s
	
class Sentence(models.Model):
	fragment = models.TextField()
	plag = models.BooleanField(default=False)
	document = models.ForeignKey(Document, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.fragment
	
	