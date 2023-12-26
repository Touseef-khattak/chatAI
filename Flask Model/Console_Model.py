import os
import contextlib
import firebase_admin
from firebase_admin import credentials, db
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage
from langchain.prompts import HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
import smtplib
from email.message import EmailMessage
import config

class ChatBot:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = config.APIKEY

        # Initialize Firebase
        cred = credentials.Certificate("creds.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://ai-support-chatbot-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        self.ref = db.reference('/')

        # Initialize email settings
        self.your_email = "safiibhai74@gmail.com"
        self.your_password = "iujw wtop vsuo ywof "
        self.msg = EmailMessage()
        self.msg["Subject"] = "Query Referred"
        self.msg["From"] = self.your_email
        self.msg["To"] = "sarfarazahmedbehan@gmail.com"

        self.loader = CSVLoader(r'D:\AI Support Chat Bot\TA\TA Development\TIERED-AI-Master Model\Master Model\Docs\result.csv')
        self.index = VectorstoreIndexCreator().from_loaders([self.loader])

        self.chat_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                         """
                        %INSTRUCTIONS:
                            You are an E-Commerce AI ChatBot, that assists users related to E-Commerec Query, other than that you will say sorry.    
                                Adjust your behavior based on user queries Only for E-Commerce Domain. 
                                
                                For instance:

                                    *Act as a General Assistant for General E-Commerce queries

                                    *Act as an E-Commerce assistant for product-related inquiries.
                                    
                                    *Adapt your behavior according to the user's specific E-Commerce needs.

                                %REMEMBER:
                                    * You will say sorry, if the query is out of E-Commerce domain.

                                    %EXAMPLE: 
                                        User Query: what is AI?

                                        Your Response: Sorry, but that query is out of the E-Commerce domain. If you have any questions related to online shopping, product inquiries, or any assistance with an e-commerce platform, feel free to ask!

                                        User Query: Who is Elon Musk?
                                        
                                        Your Response: Sorry, but that query is out of the E-Commerce domain. If you have any questions related to online shopping, product inquiries, or any assistance with an e-commerce platform, feel free to ask!

                                        User Query: what is the capital city of turkey?

                                        Your Response: Sorry, but that query is out of the E-Commerce domain. If you have any questions related to online shopping, product inquiries, or any assistance with an e-commerce platform, feel free to ask!


                            """
                    )
                ),
                HumanMessagePromptTemplate.from_template("{text}"),
            ]
        )

        self.llm = ChatOpenAI(model="gpt-4-1106-preview")

        # Initialize the conversation memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.index.vectorstore.as_retriever(search_kwargs={"k": 1}),
            memory=self.memory
        )

    def chat_completion(self, prompt):
        # Get response from the chatbot model
        prompt_formation = str((self.chat_template.format_messages(text=prompt)))
        formation = str(self.chain({"question": prompt_formation}))

        for chunk in self.llm.stream(formation):
            print(chunk.content, end="", flush=True)

        # answer = formation['answer']
        # return answer

        # Display the response
        # print(answer)

    def log_query_to_database(self, ticket_id, query):
        data = {"Ticket_id": ticket_id, "Query": query}
        self.ref.push(data)

    def send_email_notification(self, query):
        body = f"Referred query: {query}  "
        self.msg.set_content(body)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.your_email, self.your_password)
            server.send_message(self.msg)

    def start_chat(self):
        # Command line interaction
        ticket_id = 1
        print("_____________________________________________________________")
        
        while True:
            # User input prompt
            user_input = input("Enter your Prompt: ")

            # Handle user input
            if user_input.strip().lower() in ['quit', 'q', 'exit']:
                print("You're welcome! If you have any more questions, feel free to ask.")
                break

            # Log query to the database
            self.log_query_to_database(ticket_id, user_input)
            
            # Send email notification
            self.send_email_notification(user_input)

            # Get response from chatbot
            response = self.chat_completion(user_input)

            ticket_id += 1
            # return response
            print("\n_____________________________________________________________\n")
            # print(response)
            
        

chat_bot_instance = ChatBot()
chat_bot_instance.start_chat()





