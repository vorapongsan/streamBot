# pip install streamlit  langchain python-dotenv  langchain-openai

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)



# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # AI introduction message
    introduction_message = AIMessage(content="สวัสดีค่ะ! ฉันชื่อ ZBot, AI นักพยากรณ์ดวงชะตา กรุณาบอกวันเกิดและเวลาที่เกิดของคุณ แล้วฉันจะทำนายโชคชะตาและแนะนำแนวทางให้คุณค่ะ")
    st.session_state.chat_history.append(introduction_message)


st.set_page_config(page_title="Zbot Chat", page_icon="🔥")
st.title("ZBot: Guiding Your Future with AI-Powered Insights")

# coveration 

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)

# get response
def get_response(query,chat_history):
    template = """
     "system",
     "You name is ZBot.\
     You are a very skilled AI fortune teller. Use the following information to make predictions for the user.\
     Ask the user to provide their date of birth and time of birth.\
     You have to show how to calculate the zodiac sign and the fortune of the user.\
     You will encourage the user, giving them motivation and hope.\
     You will answer the question in Thai.\

        Answer the following questions considering the history of the conversation:
        Chat history: {chat_history}
        User question: {user_question}
        """
    prompt = PromptTemplate.from_template(template)
    # llm = ChatOpenAI()
    chain = prompt | llm | StrOutputParser()
    return chain.stream({"chat_history": chat_history, "user_question": query})


# user input
user_query = st.chat_input("Enter your query here")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content = user_query))

    with st.chat_message("Human"):
         st.markdown(user_query)
    
    with st.chat_message("AI"):
        #ai_response = get_response(user_query, st.session_state.chat_history)
        #st.markdown(ai_response)
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history)) 

    st.session_state.chat_history.append(AIMessage(content = ai_response))




