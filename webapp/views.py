# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from urlparse import urlparse
from .forms import DocumentForm
from . import core

# Create your views here.
def submit(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			output = core.detect_plagiarism(instance)
			request.session['output'] = output
			return redirect('review')
	# if method is not POST
	else:
		form = DocumentForm()
		return render(request=request,
								template_name='webapp/submit.html',
								context={'form': form})
	
def review(request):
	# output = '<b>This is plag.</b> this is not plag.'
	return render(request=request,
								template_name='webapp/review.html',
								context={'output': request.session['output']})

def homepage(request):
	return redirect('submit')