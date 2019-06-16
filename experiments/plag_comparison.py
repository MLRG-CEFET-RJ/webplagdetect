import sqlite3 as lite
from numpy import mean
from sklearn.metrics import f1_score, accuracy_score
APP_DB = 'db.sqlite3'
PLAG_DB = 'plag.db'

APP_DOC_ID = 2
PLAG_DOC_ID = 3327

APP_SQL = 'select fragment, plag from webapp_sentence where document_id = ? order by id'
PLAG_SQL = 'select fragment, isplag from sentence where fk_article_id = ? order by id'


def get_cleared_sentences(db_path, sql, doc_id):
	db = lite.connect(db_path)
	cursor = db.cursor()
	results = cursor.execute(sql, (doc_id,)).fetchall()
	cursor.close()
	db.close()
	return [(x[0].replace('\n', ' ').replace('\r', ' '), x[1]) for x in results]

def print_report(app_doc_id, plag_doc_id):
	app_results = get_cleared_sentences(APP_DB, APP_SQL, app_doc_id)
	plag_results = get_cleared_sentences(PLAG_DB, PLAG_SQL, plag_doc_id)
	y_true = [x[1] for x in plag_results]
	y_pred = [x[1] for x in app_results]
	# if len(app_results) == len(plag_results):
	# 	lines = ['\t'.join(('p', 'e'))]
	for i in range(len(app_results)):
		if app_results[i][0].split() != plag_results[i][0].split():
			raise Exception('Sentences do not match')
	acc = accuracy_score(y_true, y_pred)
	f1 = f1_score(y_true, y_pred)
	print 'app_id: {:4d} | plag_id: {:4d} | accuracy: {:.4f} | f1 score: {:.4f}'.format(app_doc_id, plag_doc_id, acc, f1)
	
	return acc, f1

def print_latex_table_lines(ids, accs, f1s):
	tuples = zip(ids, accs, f1s)
	tuples = sorted(tuples, key=lambda x: x[0])
	print '---'
	print 'Latex table:'
	print '---'
	for tuple in tuples:
		print 'suspicious-document{:05d}.txt & {:.4f} & {:.4f}\\\\'.format(tuple[0], tuple[1], tuple[2])
	print '---'
	print 'Total mean & {:.4f} & {:.4f}\\\\'.format(mean(accs), mean(f1s))
	

if __name__ == '__main__':
	app_doc_ids  = [1,    2,    3,    4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,   18,   19,   20,   21,   22]
	plag_doc_ids = [1, 3327,  922,   54, 3546,  849, 3339,  462, 1770, 2259, 4140,  122, 2136, 3463, 3534, 3660, 4711, 1986, 3175, 3412, 3755, 3412]
	accs = []
	f1s = []
	for i in range(len(app_doc_ids)):
		acc, f1 = print_report(app_doc_ids[i], plag_doc_ids[i])
		accs.append(acc)
		f1s.append(f1)
	print 'Total accuracy: {:.4f} | Total f1 score: {:.4f} \\\\'.format(mean(accs), mean(f1s))
	print_latex_table_lines(plag_doc_ids, accs, f1s)
