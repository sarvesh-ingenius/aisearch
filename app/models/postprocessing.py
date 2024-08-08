from app.resources.data import table_cte_mapper
from flask import current_app as app

def post_process_query(tables, query):
    query = query.strip()
    if query[0:4].lower() == 'with':
        query = query[4:]
    pre_query = """WITH
"""
    modify = False
    
    for table in tables:
        if table not in table_cte_mapper:
            app.logger.warning(f'CTE not found for the table {table}!')
        else:
            modify = True
            pre_query += f"""{table_cte_mapper[table]}
"""
    if modify:
        query = pre_query + query 
    return query
    