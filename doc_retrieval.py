import argparse
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from models_loader import get_chat_model, get_embedding_function
# If the answer is still not answerable with the provided context, say politely: 
# "I don't have necessary information in my records to answer your query. Please rephrase or check Mudit's portfolio website for more details."

PROMPT_TEMPLATE = """
You are a professional chatbot on Mudit's portfolio website.
You have access to structured documents that describe Mudit, his education, experience, skills, certifications, and projects. 
You also have access to Mudit's resume and a small structure document with some fun facts about Mudit.
Always answer in a concise, factual, and professional tone, as if you are representing Mudit to a recruiter or colleague.
Always answer without any formatting (bold, italics, etc).
If the answer is not directly answerable with the provided context, try to make sense of the context to make up a valid response by mentioning what your context is how while you're not completely sure, this is what you feel could answer the user's query.

Context:
{context}

Question: {question}
"""

def provide_ans(query_text):

    embedding_function = get_embedding_function()
    db = FAISS.load_local("faiss_index", embedding_function, allow_dangerous_deserialization=True)

    retriever = db.as_retriever(search_kwargs={"k": 10})
    results = retriever.invoke(query_text)

    context_text = "\n---\n".join([f"\"{doc.page_content}\"" for doc in results])
    prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = get_chat_model()
    response_text = model.generate_content(prompt).text

    sources = [doc.metadata.get("source", None) for doc in results]
    sources = decode_sources(sources)

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
        if file_name == "about_data.json":
            new_sources.append("About Section")
        elif file_name == "certificates_data.json":
            new_sources.append("Certificate Section")
        elif file_name == "Current Resume.pdf":
            new_sources.append("Resume at Home Section")
        elif file_name == "education_history.json":
            new_sources.append("Education Subsection")
        elif file_name == "experience_data.json":
            new_sources.append("Experience Section")
        elif file_name == "facts_data.json":
            new_sources.append("Facts Mini-section")
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