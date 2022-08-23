#!pip install openai
import os
import openai
import pandas as pd
import numpy as np
import time
import random
from time import sleep
import regex as re


## Add your OpenAI keys here 
openai.organization = "XXX-XXXXXXXXXXXXXXXXXXXXX" # Replace with your OpenAI organisation id
openai.api_key = "XX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # Replace with your OpenAI API key


#remove in-line comment from code
def remove_comments_from_code(x, language):
	if language == "python":
		x = re.sub(re.compile("'''.*?'''", re.DOTALL), "", x)  # Remove '''...''' comments
		x = re.sub(re.compile('""".*?"""', re.DOTALL), "", x)  # Remove '''...''' comments
		x = re.sub(re.compile("(?<!(['\"]).)#[^\n]*?\n"), "\n", x)  # Remove #...\n comments
	elif language == "php":
		x = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", x)  # Remove '''...''' comments
		x = re.sub(re.compile("\/\/[a-zA-Z0-9]+\n{1}"), "\n", x)  # Remove #...\n comments
		x = re.sub(re.compile("#[a-zA-Z0-9]+\n{1}"), "\n", x)  # Remove #...\n comments
	elif language == 'ruby':
		x = re.sub(re.compile("(?<!(['\"]).)#[^\n]*?\n"), "\n", x)  # Remove #...\n comments
	elif language == 'go':
		x = re.sub(re.compile("\/\/[a-zA-Z0-9]+\n{1}"), "\n", x)  # Remove #...\n comments
	elif language == 'javascript':
		x = re.sub(re.compile("\/\/[ a-zA-Z0-9]"), "\n", x)  # Remove #...\n comments
		x = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", x)  # Remove '''...''' comments
	elif language == "java":
		x = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", x)  # Remove '''...''' comments
		x = re.sub(re.compile("\/\/[a-zA-Z0-9]+\n{1}"), "\n", x)  # Remove #...\n comments	
	return x


lang = 'go' #'choose language (options : java', 'python', 'ruby', 'php', 'javascript', 'go')

file_name = 'gpt3_'+lang



codesearch_df = pd.read_excel('1K Samples/'+file_name+".xlsx")



oneshot_df = pd.read_excel('One Shot Examples/gpt3_OneShotExample_' + lang + '.xlsx')
example_code= oneshot_df['code'].tolist()[0]
example_doc = oneshot_df['docstring'].tolist()[0]


gpt_3_doc_list = []


for idx,row in codesearch_df.iterrows():
	print(idx)
	sleep(10)
	code = row['code']
	code = remove_comments_from_code(code,language=lang)
	#doc = row['docstring']
	#print(code)
	#print(doc)
	prompt = "Code:\n"+example_code+"\nDocumentation:\n"+example_doc+'\nCode:\n'+code+"\n"+"Documentation:\n"
	zero_shot_results = dict()
	response = openai.Completion.create(
	    engine="code-davinci-002",#"text-davinci-002",#
	    prompt=prompt,
	    temperature=0.2,
	    max_tokens=256,
	    top_p=1,
	    frequency_penalty=0,
	    presence_penalty=0,
	    best_of = 1,
	    stop=["Code:"]
	)
	#print(response["choices"][0].text)
	#break

	gpt_3_doc_list.append(response["choices"][0].text)

codesearch_df['GPT-3 documentation'] = gpt_3_doc_list

codesearch_df.to_excel(lang+"_gpt3_DocAdded.xlsx", index = False)