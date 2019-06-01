import nltk

from .models import Sentence

def break_by_sentences(data):
	tokenizer = get_tokenizer()
	sentences = tokenizer.tokenize(data)
	return sentences

def get_tokenizer():
		return nltk.data.load('tokenizers/punkt/english.pickle')

def save_sentences(document):
	sentences = break_by_sentences(document.content)
	for sentence in sentences:
		sentence_instance = Sentence(fragment=sentence, document=document)
		sentence_instance.save()
	setence_instances = Sentence.objects.filter(document__id=document.id)
	
	
	return setence_instances

def tag_sentences(text, plags):
	for plag in plags:
		text = text.replace(plag, '<b>' + plag + '</b>', 1)
	return text
	
def get_plag_sentences(sentence_instances):
	return [sentence_instances.first().fragment]
	
def detect_plagiarism(document):
	document.save()
	sentence_instances = save_sentences(document)
	print('Detecting plagiarism...')
	# TODO change to real plagiarism detection
	plags = get_plag_sentences(sentence_instances)
	output = tag_sentences(document.content, plags)
	return output
	