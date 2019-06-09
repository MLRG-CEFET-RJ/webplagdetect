import sys, os, shutil

import nltk

from django.db.models import Q

from preprocess import MyVocabularyProcessor
from .models import Sentence

import torch
from torch.autograd import Variable
from skipthoughts import UniSkip
from torch.nn import CosineSimilarity
from torch.autograd import Variable

sys.path.append('skip-thoughts.torch/pytorch')

MAX_DOCUMENT_LENGTH = 15

def detect_plagiarism(document):
	document.save()
	sentence_instances = save_sentences(document)
	print('Detecting plagiarism...')
	skip_thoughts(sentence_instances, document.id)
	output = get_report(document.content, document.id)
	return output

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

def get_report(text, doc_id):
	sentences = Sentence.objects.filter(document__id=doc_id).filter(plag=True)
	for sentence in sentences:
		text = text.replace(sentence.fragment, '<b>' + sentence.fragment + '</b>', 1)
	return text
	
def skip_thoughts(sentence_instances, doc_id):
	sentence_ids = [s.id for s in sentence_instances]
	sentences = [s.fragment for s in sentence_instances]
	vocab_processor = MyVocabularyProcessor(max_document_length=MAX_DOCUMENT_LENGTH, min_frequency=0, is_char_based=False)
	vocab_processor.fit_transform(sentences)
	
	## Extract word:id mapping from the object.
	vocab_dict = vocab_processor.vocabulary_._mapping
	
	sorted_vocab = sorted(vocab_dict.items(), key=lambda x: x[1])
	
	## Treat the id's as index into list and create a list of words in the ascending order of id's
	## word with id i goes at index i of the list.
	vocabulary = list(list(zip(*sorted_vocab))[0])
	
	dir_st = 'data/skip-thoughts'
	
	print("Creating skip-thoughts model...")
	uniskip = UniSkip(dir_st, vocabulary)
	
	input = Variable(torch.LongTensor(list(vocab_processor.fit_transform(sentences))))
	
	output_seq2vec = uniskip(input)
	
	incc, id_dict = build_cc_input(output_seq2vec, sentence_ids, doc_id)
	outcc = correlation_clustering(incc)
	clusters = load_clusters(outcc, id_dict)
	flag_plagiarism(clusters)
	
def build_cc_input(embeddings, ids, doc_id):
	i = 0
	filepath = 'data/cc/%s.in' % doc_id
	enum_ids = list(enumerate(ids, 1)) #needed for cc as ids must start from 1
	cos = CosineSimilarity(dim=0, eps=1e-6)
	with open(filepath, 'w') as f:
		f.writelines(['5\n', '100\n', str(len(ids)) + '\n', '100\n'])
		for id1 in ids:
			j = i + 1
			for id2 in ids[ids.index(id1)+1:]:
				input1 = embeddings[i]
				input2 = embeddings[j]
				similarity = cos(input1, input2).item()
				line = '  '.join((str(enum_ids[i][0]), str(enum_ids[j][0]), str(similarity - 0.5))) + '\n'
				f.write(line)
				j += 1
			i += 1
	return filepath, dict(enum_ids)

def correlation_clustering(infile, time_limit=3600):
	cmd = 'data/cc/CCP %s %d' % (infile, time_limit)
	return_code = os.system(cmd)
	outfile = infile.replace('in', 'out')
	shutil.move('out.txt', outfile)
	return infile.replace('in', 'out')

def load_clusters(filepath, ids_map):
	with open(filepath, 'r') as f:
		data = f.read()
		clusters = [line.split(' ') for line in data.split('\n')][:-1]
		clusters = [line[:-1] for line in clusters]
		clusters = [map(int, cluster) for cluster in clusters]
		clusters = [[x+1 for x in cluster] for cluster in clusters] # +1 to every node id due to c code limitations
		clusters = [[ids_map[node] for node in nodes] for nodes in clusters] # map node ids back to corresponding sentence ids
		return clusters
	
def flag_plagiarism(clusters):
	# Removes largest cluster. All others are taken as plagiarism.
	clusters.remove(max(clusters, key=lambda cluster: len(cluster)))
	# Flattens plag sentence ids
	plag = [sentence_id for sentence_ids in clusters for sentence_id in sentence_ids]
	# Update database
	Sentence.objects.filter(id__in=plag).update(plag=True)
	

		
		