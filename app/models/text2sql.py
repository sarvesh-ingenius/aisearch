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
#     table_list = ["""-- frontend clicks and events
# CREATE TABLE fpl_ds_analytics.sk_sohel_bq_events(
#     event_timestamp BIGINT, -- Timestamp of the event, divide by 1000000
#     event_name VARCHAR(50), -- Name of the event
#     user_id VARCHAR(50), -- Unique ID of the customer
#     platform VARCHAR(50), -- Name of the platform the customer used
#     event_date VARCHAR(50), –- Should be parsed in %Y%m%d format
#     app_info.id VARCHAR(50), –- ID of the mobile application the customer used
#     device.mobile_brand_name VARCHAR(50), -- Brand name of the mobile
#     device.mobile_model_name VARCHAR(50), -- Model name of the mobile
# );
# """]
    return table_list

# def write_query(question):
#     query = """SELECT
#   COUNT(DISTINCT e.user_id)
# FROM fpl_mis.bigquery_onecard_events AS e
# WHERE
#   e.event_name = 'Action'
#   AND FROM_UNIXTIME(e.event_timestamp) >= (
#     CURRENT_DATE - (3 * INTERVAL '7' DAY)
#   )"""
#     print('Writing Query')
#     return query
  
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
    # egs = [
    #   ("onescore customers with samsung mobile who clicked on the event event_name", "SELECT DISTINCT user_id FROM fpl_event.bigquery_onecard_events WHERE lower(app_info.id) = 'tech.fplabs.score' AND lower(device.mobile_brand_name) = 'samsung' AND lower(event_name) = lower('event_name');"),
    #   ("events triggered by onecard customers with samsung mobile between 2024-04-19 and 2024-05-29", "SELECT event_timestamp, event_name, user_id FROM fpl_event.bigquery_onecard_events WHERE lower(app_info.id) = 'com.creditcard.onecard' AND lower(device.mobile_brand_name) = 'samsung' AND FROM_UNIXTIME(event_timestamp / 1000000) BETWEEN DATE('2024-04-19') AND DATE('2024-05-29');"),
    #   ("journey of the customer id 938465289037543 between 2024-04-19 and 2024-05-29", "SELECT event_timestamp, event_name, user_id FROM fpl_event.bigquery_onecard_events WHERE user_id = '938465289037543' AND FROM_UNIXTIME(event_timestamp / 1000000) BETWEEN DATE('2024-04-19') and DATE('2024-05-29') ORDER BY event_timestamp;")
    # ] 
    prompt = create_prompt(prompt_template, "\n".join(table_schemas), egs, question)
    print("------------------------------------------------------------------------\n", prompt)
    generated_query = get_generated_text(prompt)
    tables_used_in_query = [t for t in table_names if re.search(t, generated_query) is not None]
    final_query = post_process_query(tables_used_in_query, generated_query)
    return final_query