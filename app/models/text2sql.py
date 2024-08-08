import time
import re

from app.models.LLMs.gemini import get_generated_text
from app.models.LLMs.prompts import create_prompt, prompt_template
from app.models.utilities import clean_db_result 
from app.resources.vector_indices import table_index, few_shots_index
from app.models.postprocessing import post_process_query
from flask import current_app as app

def get_tables_from_question(question, k=5):
    table_list = table_index.search(question, k)
    print(table_list)
    table_list = [clean_db_result(x) for x in table_list] 

    return table_list

  
def write_query(question, team):
    table_schemas, table_names = table_index.search(question, k=1, filter = {'Team' : team})
    print("************* DEBUG - ", table_names)
    if len(table_schemas) == 0:
        print('**************** DEBUG2')
        return None
    table_names = [x['Table'] for x in table_names]
    app.logger.info('List of Tables : ')
    app.logger.info(table_names)
    example_questions, example_metadata = few_shots_index.search(question, k = 3, filter = {'Table' : table_names})
    egs = []
    for ques, metadict in zip(example_questions, example_metadata):
        egs.append((ques, metadict['Query']))

    prompt = create_prompt(prompt_template, "\n".join(table_schemas), egs, question)
    print("------------------------------------------------------------------------\n", prompt)
    generated_query = get_generated_text(prompt)
    tables_used_in_query = [t for t in table_names if re.search(t, generated_query) is not None]
    final_query = post_process_query(tables_used_in_query, generated_query)
    return final_query