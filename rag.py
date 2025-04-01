from typing import List, Dict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain import hub
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

class ResearchChatbot:
    def __init__(self):
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.vector_store = Chroma(
            collection_name="research_papers",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )
        
    def chat(self):
        print("Research Assistant: Hi! I can help you understand research papers. What would you like to know?")
        print("(Type 'quit' to exit)")
        
        conversation_history = []
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'quit':
                break
                
            relevant_docs = self.vector_store.similarity_search(user_input)
            context = "\n".join(doc.page_content for doc in relevant_docs)
            
            messages = [
                SystemMessage(content=f"""You are a helpful research assistant. 
                Use the following context to answer questions:
                {context}
                
                If you don't know the answer, say so. Keep responses concise."""),
            ]
            
            for msg in conversation_history[-4:]:
                messages.append(msg)
                
            messages.append(HumanMessage(content=user_input))
            
            response = self.llm.invoke(messages)
            print("\nResearch Assistant:", response.content)
            
            conversation_history.append(HumanMessage(content=user_input))
            conversation_history.append(response)

if __name__ == "__main__":
    chatbot = ResearchChatbot()
    chatbot.chat()
