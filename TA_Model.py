import os
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
import smtplib
from email.message import EmailMessage
import config

class ChatBot:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = config.APIKEY

        # Initialize Firebase
        cred = credentials.Certificate("creds.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://aibot-1bd6d-default-rtdb.asia-southeast1.firebasedatabase.app/'})
        self.ref = db.reference('/')

        # Initialize email settings
        self.your_email = "syedhussainshah01@gmail.com"
        self.your_password = "eohs qjam vvkf ytoe "
        self.msg = EmailMessage()
        self.msg["Subject"] = "Query Referred"
        self.msg["From"] = self.your_email
        self.msg["To"] = "safiibhai74@gmail.com"

        # Initialize chat model and conversation chain
        self.loader = CSVLoader(r'D:\AI Support Chat Bot\TA\TA Development\TIERED-AI-Master Model\Master Model\Docs\result.csv')
        self.index = VectorstoreIndexCreator().from_loaders([self.loader])

        self.chat_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        """
                        %INSTRUCTIONS

                        ->You will be equipped to provide general product information when a user asks a general question.

                            EXAMPLES
                                - What is Adidas, Amazon, and Apple?
                                - Give me details about Sony.
                                - Who is the founder of Ebay?

                        ->You will be working as an E-Commerce assistant when a user asks a specific question about any product's
                        Features like:

                                EXAMPLES

                                    -Technical specifications
                                        Performance capabilities
                                        Unique selling points
                                        Compatibility with other products or systems
                                        Special features or functionalities
                                        Price:

                                    -Base price
                                        Discounts or promotions
                                        Payment options
                                        Warranty and support costs
                                        Any additional fees or charges
                                        Limitations:

                                    -Technical constraints
                                        Compatibility limitations
                                        Usage restrictions
                                        Geographic or regulatory limitations
                                        Any known issues or drawbacks
                                        Sizes:

                                    -Dimensions
                                        Weight
                                        Available colors or styles
                                        Capacity or storage options
                                        Customization possibilities
                                        Availability:

                                    -Stock status
                                        Pre-order options
                                        Shipping details
                                        Delivery timeframes
                                        Regional availability
                                        Warranty and Support:

                                    -Warranty period
                                        Support options
                                        Return or exchange policies
                                        Troubleshooting guidance
                                        Customer service contact information
                                        User Reviews:

                                    -Aggregated user ratings
                                        Testimonials or reviews
                                        Common user feedback
                                        Issues raised by other users
                                        Upgrades and Accessories:

                                    -Compatibility with upgrades
                                        Available accessories or add-ons
                                        Suggestions for complementary products
                                                            
                                It should be capable of adopting a formal and technical manner to provide accurate and detailed information.

                        ->ou will be addressing customer inquiries, FAQs etc

                            EXAMPLES
                                -Customer Inquiries:

                                        Product Usage: Providing guidance on how to use the product effectively.
                                        Compatibility: Addressing questions about the product's compatibility with other devices or software.
                                        Technical Issues: Assisting users with troubleshooting and technical problems.
                                        Order Status: Updating customers on the status of their orders, including shipping and delivery details.
                                        Returns and Exchanges: Guiding users through the process of returning or exchanging a product.

                                -FAQs (Frequently Asked Questions):

                                        Shipping Information: Clarifying details about shipping methods, costs, and delivery times.
                                        Payment Options: Explaining the various payment methods accepted and any associated fees.
                                        Product Availability: Providing information about product stock status and availability.
                                        Refund Policy: Clarifying the company's policy on refunds and the steps involved.
                                        Security and Privacy: Addressing concerns about the security of online transactions and user privacy.

                        ->You will be working as a Ticketing system to manage, enabling it to effectively manage customer support tickets. "
                        
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
        formation = self.chain({"question": prompt_formation})
        answer = formation['answer']

        # Display the response
        print(answer)

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
            self.chat_completion(user_input)

            ticket_id += 1

# Instantiate and run the chat bot
chat_bot_instance = ChatBot()
chat_bot_instance.start_chat()





