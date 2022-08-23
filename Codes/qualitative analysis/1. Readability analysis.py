import pandas as pd
from math import ceil
import os
import textstat
import ast
import statistics

#Flesch-Kincaid Grade Readability for a list of texts
def readability_measure_FleschKincaid(texts):
	readability_list = []
	for text in texts:
		readability_list.append(textstat.flesch_kincaid_grade(str(text)))
	mean_readability = statistics.mean(readability_list)
	median_readability = statistics.median(readability_list)
	return mean_readability, median_readability

def avg_len(texts):
	len_list = []
	for text in texts:
		len_list.append(len(str(text).split())) # Splitting to count words instead of characters
	#print(max(texts, key = len))
	return statistics.mean(len_list)


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



#Quality of Generated Docs
# Reference Paper: 1. How Documentation Evolves Over Time by Schreck et al.
#		   2. Automatic quality assessment of source code comments: the JavadocMiner by Khamis et al.


print("Readability Analysis:")
print("---------------------")
print("Mean and Median Readability of Actual Documentations:")
print(readability_measure_FleschKincaid(all_actual_documentation_list))
print("Mean and Median Readability of Generated Documentations:")
print(readability_measure_FleschKincaid(all_generated_documentation_list))


print("")
print("Length Analysis:")
print("-----------------")
print("Mean Length of Actual Documentations:")
print(avg_len(all_actual_documentation_list))


print("Mean Length of Generated Documentations:")
print(avg_len(all_generated_documentation_list))
