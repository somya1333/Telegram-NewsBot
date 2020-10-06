import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"

from gnewsclient import gnewsclient
client=gnewsclient.NewsClient()

import dialogflow_v2 as dialogflow
# from dialogflow_v2.types import TextInput, QueryInput
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-ndnn"

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input=dialogflow.types.TextInput(text=text,language_code=language_code)
    query_input=dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)
    if response.intent.display_name == 'news.search':
        return "news.search", f"{dict(response.parameters)}"
    else:
        return "small_talk", response.fulfillment_text

def fetch_news(parameters):
    client.topic = parameters.get('category')
    client.location = parameters.get('geo-country')
    client.language = parameters.get('language')
    # client.sort = parameters.get('sort')
    # client.date = parameters.get('date-time')
    # client.keyword = parameters.get('keyword')
    # client.source = parameters.get('source')
    return client.get_news()[:3]