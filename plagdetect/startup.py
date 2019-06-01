import nltk

def initialize_punkt():
	try:
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		print('Punkt loaded successfully.')
	except Exception as e:
		print('Failed to load punk. Downloading it now.')
		nltk.download('punkt')