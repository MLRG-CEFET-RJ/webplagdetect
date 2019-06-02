from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = ['content']
	
	def __init__(self, *args, **kwargs):
		super(DocumentForm, self).__init__(*args, **kwargs)
		self.fields['content'].widget = forms.Textarea(attrs={'id': 'my_input'})
	