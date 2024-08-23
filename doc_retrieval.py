import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from env_loader import CHROMA_PATH, DATA_PATH
from genai_loader import get_chat_model, get_embedding_function

PROMPT_TEMPLATE = """
Based on the following contexts from my documents that store all data about my education history, experience history, skills, certificates I have recieved and the projects I have done:

{context}

---

You are a chatbot on my portfolio website who answers professionally yet conscisely. Answer this question without any formatting (bold, italics, etc) as the chatbot: {question}
"""

def provide_ans(query_text):

    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    if len(results) == 0:
        print(f"No any matching results.")
        return prompt, "I could not find the answer to your query", []
    elif results[0][1] < 0.5:
        print(f"Unable to find suitable matching results.")
        print(f"The results were {results}")
        return prompt, "I couldn't find upto the mark answers for your question in my database! Pleaswe rephrase your query", []

    context_text = "\n\n---\n\n".join([f"\"{doc.page_content}\"\nScore:{_score}" for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = get_chat_model()
    response_text = model.generate_content(prompt).text

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    sources = decode_sources(sources)
    if __name__ == "__main__":
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print(formatted_response)
    return prompt, response_text, sources

def decode_sources(sources):
    sources = list(set(sources))
    new_sources = []
    for source in sources:
        _ = source.rfind('\\')
        file_name = source[_+1:]
        # print(file_name)
        if file_name == "certificates_data.json":
            new_sources.append("Certificate Section")
        elif file_name == "Current Resume.pdf":
            new_sources.append("Resume at Home")
        elif file_name == "education_history.json":
            new_sources.append("Education Subsection")
        elif file_name == "experience_data.json":
            new_sources.append("Experience Section")
        elif file_name == "projects_data.json":
            new_sources.append("Projects Section")
        elif file_name == "skills.json":
            new_sources.append("Skills Subsection")
    return new_sources

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    provide_ans(query_text)

if __name__ == "__main__":
    main()