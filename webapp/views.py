# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .forms import DocumentForm
from django.http import HttpResponse

# Create your views here.
def submit(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			# save it
			# break by sentences
			# process
			return redirect('review')
	# if method is not POST
	else:
		form = DocumentForm()
		return render(request=request,
								template_name='webapp/submit.html',
								context={'form': form})
	
def review(request):
	# return HttpResponse('\nDocument created!\n%s\n' % request.content)
	return HttpResponse('\nDocument created!\n')

def homepage(request):
	return redirect('submit')