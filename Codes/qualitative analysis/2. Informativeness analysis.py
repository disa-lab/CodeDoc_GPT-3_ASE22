import pandas as pd
from math import ceil
import os
import ast
import statistics

def join_doc_tokens(text):
	ref_doc = ast.literal_eval(text)
	ref_doc = ' '.join(map(str, ref_doc))
	return ref_doc


lang_list = ['go','java','javascript','python','php','ruby']

all_lang_generated_doc_df = pd.DataFrame()

for lang in lang_list:
	file_name = lang+"_gpt3_DocAdded.xlsx"
	this_lang_generated_doc_df=pd.read_excel(file_name)
	if all_lang_generated_doc_df.empty:
		all_lang_generated_doc_df = this_lang_generated_doc_df
	else:
		all_lang_generated_doc_df = all_lang_generated_doc_df.append(this_lang_generated_doc_df,ignore_index=True)

all_actual_documentation_list = all_lang_generated_doc_df['docstring_tokens'].apply(join_doc_tokens)

all_lang_generated_doc_df['GPT-3 documentation'] =  all_lang_generated_doc_df['GPT-3 documentation'].astype(str)
all_generated_documentation_list = all_lang_generated_doc_df['GPT-3 documentation'].tolist()

# TfidfVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


# instantiate the vectorizer object
tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english')

# convert th documents into a matrix
total = all_actual_documentation_list
tfidfvectorizer.fit(total)

tfidf_tokens = tfidfvectorizer.get_feature_names()


tfidf_wm_train = tfidfvectorizer.transform(all_actual_documentation_list)
# convert test documents into a matrix
tfidf_wm_test = tfidfvectorizer.transform(all_generated_documentation_list)

#retrieve the terms found in the corpora

df_tfidfvect_train = pd.DataFrame(data = tfidf_wm_train.toarray(),columns = tfidf_tokens)
print("\nTD-IDF Vectorizer Actual:\n")

df_tfidfvect_train['Documentation'] = all_actual_documentation_list
df_tfidfvect_train['total_tf_idf']= df_tfidfvect_train[tfidf_tokens].sum(axis=1)

df_tfidfvect_train = df_tfidfvect_train[['Documentation','total_tf_idf']]
print(df_tfidfvect_train)


#retrieve the terms found in the corpora
df_tfidfvect_test = pd.DataFrame(data = tfidf_wm_test.toarray(),columns = tfidf_tokens)
print("\nTD-IDF Vectorizer Generated:\n")

df_tfidfvect_test['Documentation'] = all_generated_documentation_list
df_tfidfvect_test['total_tf_idf']= df_tfidfvect_test[tfidf_tokens].sum(axis=1)

df_tfidfvect_test = df_tfidfvect_test[['Documentation','total_tf_idf']]
print(df_tfidfvect_test)


## Calculation avg tf-idf of actual and generated doc
print("Avg TF-IDF of Actual Documentations:")
print(statistics.mean(df_tfidfvect_train['total_tf_idf'].tolist()))

print("Avg TF-IDF of Generated Documentations:")
print(statistics.mean(df_tfidfvect_test['total_tf_idf'].tolist()))

print(len(tfidf_tokens))
