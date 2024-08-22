from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
from env_loader import DATA_PATH
from doc_loader import download_files, generate_data_store
from doc_retrieval import provide_ans

app = Flask(__name__)
CORS(app)

@app.route('/refresh_files')
def refresh_data():
    try:
        download_files()
        return "DATA REFRESHED", 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Error downloading the files and loading the vector database because {e}"}), 503

@app.route('/prepare_database')
def prepare_vector_database():
    try:
        if not os.path.exists(DATA_PATH):
            download_files()
        generate_data_store()
        return "VECTOR DATABASE READY", 200
    except Exception as e:
        print(e)
        return jsonify({"error": f"Error loading the vector database because {e}"}), 503

@app.route('/query', methods=['POST'])
def query_documents():
    user_query = request.form.get('user_query')
    if not user_query:
        return jsonify({"error": "No query provided"}), 404
    try:
        prompt_with_context, response, sources = provide_ans(user_query)
        return jsonify({"answer": response, "context": prompt_with_context, "sources": sources})
    except Exception as e:
        print(e)
        return jsonify({"error": f"Error fetching the query response because {e}"}), 503

@app.route('/')
def start_to_run():
    return "THE SERVER HAS STARTED", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])