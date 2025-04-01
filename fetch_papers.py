import arxiv
import openai
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain import hub
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.parsers import GrobidParser
from langchain_community.document_loaders.generic import GenericLoader
from langgraph.graph import START, StateGraph
from langchain.chat_models import init_chat_model
from typing_extensions import List, TypedDict
SHORT_SELECTION_PAPER_COUNT = 3


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")


llm = init_chat_model("gpt-4o-mini", model_provider="openai")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  
)

def summarize(text):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=OPENAI_ASSISTANT_ID,
        instructions="Summarize the paper in 2-3 sentences"
    )
    
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value
    

def fetch_papers(query, max_results=3):
    filenames = []
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=SHORT_SELECTION_PAPER_COUNT,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = client.results(search)
    papers = []
    for r in results:
        summary = summarize(r.summary)
        arxiv_id = r.entry_id.split('/')[-1]
        paper_info = {
            'title': r.title,
            'id': arxiv_id,
            'summary': summary,
            'authors': r.authors,
            'url': r.pdf_url,
            'published': r.published
        }
        papers.append(paper_info)
        
        filename = "".join(c for c in r.title if c.isalnum() or c in (' ', '-', '_')).rstrip() + ".pdf"
        filenames.append(filename)
        paper = next(arxiv.Client().results(arxiv.Search(id_list=[arxiv_id])))
        paper.download_pdf(dirpath="./papers", filename=filename)
        loader = GenericLoader.from_filesystem(
            "./papers",
            glob="*",
            suffixes=[".pdf"],
            parser= GrobidParser(segment_sentences=False)
        )
        docs = loader.load()
        document_chunks = vector_store.add_documents(documents=docs)
        print(document_chunks[:3])

        
        
    return filenames, papers



if not os.path.exists("./papers"):
    os.makedirs("./papers")



class State(TypedDict):
    question: str
    answer: str
    context: List[Document]
    
    
            


        