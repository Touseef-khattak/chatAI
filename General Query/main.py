from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from dotenv import load_dotenv, find_dotenv
import os
import spacy
import pandas as pd

os.environ["OPENAI_API_KEY"] = "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"

# small English model
nlp = spacy.load('en_core_web_sm')

load_dotenv(find_dotenv())

default_responses_df = pd.read_csv('default_responses.csv')
df = pd.read_csv('amazon.csv')

chat = ChatOpenAI(model_name='gpt-4-1106-preview', temperature=0.0)
agent = create_pandas_dataframe_agent(chat, df, verbose=False)

response_cache = {}

def get_similar_queries(user_query):
    similar_queries = []
    for index, row in default_responses_df.iterrows():
        similarity = nlp(user_query).similarity(nlp(row['user_query']))
        if similarity > 0.8:
            similar_queries.append(row['user_query'])
    return similar_queries


def process_query(query):
    similar_queries = get_similar_queries(query.lower())
    if similar_queries:
        # Return a default response for the most similar query
        default_response = default_responses_df.loc[
            default_responses_df['user_query'] == similar_queries[0], 'default_response'
        ].values[0]
        return default_response
    else:
        if query in response_cache:
            return response_cache[query]
        else:
            response = agent.run(query)
            response_cache[query] = response
            return response

def user_input():
    while True:
        user_query = input("You: ")
        if user_query.lower() == 'quit':
            print("Exiting...")
            break
        
        response = process_query(user_query)
        print("Bot:", response)

# user input loop
user_input()

