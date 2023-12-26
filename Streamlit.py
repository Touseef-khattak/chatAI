# CODE ONLY FOR STREAMLIT APP #


# import os
# import smtplib
# import config
# import streamlit as st
# import firebase_admin
# from langchain.globals import set_llm_cache
# from langchain.cache import InMemoryCache
# from firebase_admin import credentials, db
# from email.message import EmailMessage
# from langchain.chains import ConversationalRetrievalChain
# from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders.csv_loader import CSVLoader
# from langchain.indexes import VectorstoreIndexCreator
# from langchain.memory import ConversationBufferMemory
# from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
# from langchain.schema.messages import SystemMessage
# from PIL import Image
# import langchain

# class ChatBot:
#     os.environ["OPENAI_API_KEY"] = config.APIKEY
#     set_llm_cache(InMemoryCache())

#     ticket_id_key = "ticket_id"
#     ticket_id = 1

#     def __init__(self):
#         cred = credentials.Certificate("creds.json")
#         firebase_admin.initialize_app(cred, {'databaseURL': 'https://aibot-1bd6d-default-rtdb.asia-southeast1.firebasedatabase.app/'})
#         self.ref = db.reference('/')

#         # Retrieve or initialize ticket_id from Firebase
#         ticket_id_snapshot = self.ref.child(ChatBot.ticket_id_key).get()
#         if ticket_id_snapshot is not None:
#             ChatBot.ticket_id = ticket_id_snapshot
#         else:
#             self.ref.child(ChatBot.ticket_id_key).set(ChatBot.ticket_id)
    
#     def __init__(self):
#         # Check if Firebase app is already initialized
#         if not firebase_admin._apps:
#             cred = credentials.Certificate("creds.json")
#             firebase_admin.initialize_app(cred, {'databaseURL': 'https://aibot-1bd6d-default-rtdb.asia-southeast1.firebasedatabase.app/'})
#         self.ref = db.reference('/')

#          # Initialize email settings
#         self.your_email = "syedhussainshah01@gmail.com"
#         self.your_password = "eohs qjam vvkf ytoe "
#         self.msg = EmailMessage()
#         self.msg["Subject"] = "Query Referred"
#         self.msg["From"] = self.your_email
#         self.msg["To"] = "safiibhai74@gmail.com"


#         self.loader = CSVLoader(r'C:\Users\warda\OneDrive\Desktop\Master Model\Docs\Fitness.csv')
#         self.index = VectorstoreIndexCreator().from_loaders([self.loader])

#         # Define system messages for each assistant

#         self.chat_template = ChatPromptTemplate.from_messages(
#             [
#                 SystemMessage(
#                     content=(
#                         """
#                       Adjust your behavior based on user queries. 
                      
#                       For instance:

#                         *Act as a General Assistant for General queries

#                         *Act as an E-Commerce assistant for product-related inquiries.

#                         *Function as a FAQ Assistant for frequently asked questions.
                        
#                         *Adapt your behavior according to the user's specific needs.
                        
#                         """
#                     )
#                 ),
#                 HumanMessagePromptTemplate.from_template("{text}"),
#             ]
#         )
        
            
#         self.llm = ChatOpenAI(model="gpt-4-1106-preview")
#         self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
#         self.chain = ConversationalRetrievalChain.from_llm(
#             llm=self.llm,
#             retriever=self.index.vectorstore.as_retriever(search_kwargs={"k": 1}),
#             memory=self.memory
#         )

#     def chat_completion(self, prompt):

#         # Log query to the database
#         self.log_query_to_database(prompt)

#         prompt_formation = str(self.chat_template.format_messages(text=prompt))
#         formation = self.chain({"question": prompt_formation})
#         answer = formation['answer']
#         return answer
    
#     def log_query_to_database(self,query):
#         data = {"Ticket_id": ChatBot.ticket_id, "Query": query}
#         self.ref.push(data)

#         # Increment ticket_id in the database
#         ChatBot.ticket_id += 1
#         self.ref.child(ChatBot.ticket_id_key).set(ChatBot.ticket_id)

#     def send_email_notification(self, query):
#         body = f"Referred query: {query}  "
#         self.msg.set_content(body)

#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(self.your_email, self.your_password)
#             server.send_message(self.msg)

# # <-------Some Styling using Streamlit------->
#     im = Image.open(r"C:\Users\warda\OneDrive\Desktop\Master Model\assets\favicon.ico")

#     st.set_page_config(
#         page_title = "AI SUPPORT CHATBOT",
#         page_icon=im,
#         layout="centered",
#         menu_items=None,
#     )

# #----->End of Styling<------


#     def start_chat(self):
#         st.title("AI SUPPORT CHATBOT")
        
#         user_input = st.text_input("Enter your Prompt:")

#         if user_input:
#             if user_input.lower() in ['quit', 'q', 'exit']:
#                 st.write("You're welcome! If you have any more questions, feel free to ask.")
#             else:
#                 # Check if the prediction is already in the cache
#                 cached_result = self.llm.predict(self.chat_completion(user_input))
#                 if cached_result is not None:
#                     answer = cached_result

#                 else:
#                     answer = self.chat_completion(user_input)

#                 st.write(answer)
#                 self.log_query_to_database(user_input)
#                 self.send_email_notification(user_input)

# # Instantiate and run the chat bot
# chat_bot_instance = ChatBot()
# chat_bot_instance.start_chat()



