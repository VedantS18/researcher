from fetch_papers import fetch_papers
from rag import ResearchChatbot

def main():
    query = input("Enter a research topic to fetch papers about: ")
    filenames, papers = fetch_papers(query)
    
    print("\nFetched and processed these papers:")
    for paper in papers:
        print(f"- {paper['title']}")
    
    print("\nStarting chat interface...")
    chatbot = ResearchChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()