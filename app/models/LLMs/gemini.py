import google.generativeai as genai
import textwrap
from flask import current_app as app

API_KEY = 'your-gemini-api-key'

genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def get_generated_text(prompt):
    response = gemini_model.generate_content(prompt)
    try:
        response_text = response.text
        return response_text
    except Exception as e:
        app.logger.info('Error fetching response from Gemini')
        app.logger.info(e)
        return 'Oh o! Seems like I could not generate the code.'
