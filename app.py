from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from env_loader import DATA_PATH
from doc_loader import download_files, init_faiss_index
from doc_retrieval import provide_ans

app = Flask(__name__)
CORS(app)

@app.route('/refresh_files')
def refresh_data():
    try:
        download_files()
        init_faiss_index()  # Rebuild FAISS after downloading new files
        return "DATA REFRESHED AND VECTOR DATABASE UPDATED", 200
    except Exception as e:
        print(e)
        return jsonify({"error": f"Error refreshing data: {e}"}), 503

@app.route('/query', methods=['POST'])
def query_documents():
    user_query = request.form.get('user_query')
    mode = request.form.get('site_mode')
    if not user_query:
        return jsonify({"error": "No query provided"}), 404
    try:
        prompt_with_context, response, sources = provide_ans(mode, user_query)
        return jsonify({
            "answer": response, 
            "context": prompt_with_context, 
            "sources": sources
        })
    except Exception as e:
        print(e)
        return jsonify({"error": f"Error fetching the query response because {e}"}), 503

@app.route('/stay_alive', methods=['GET'])
def stay_alive():
    return "ALIVE", 200

@app.route('/')
def start_to_run():
    return "THE SERVER HAS STARTED", 200

if __name__ == '__main__':
    # Ensure data exists
    if not os.path.exists(DATA_PATH):
        download_files()
    # Initialize FAISS index: load existing and rebuild in background
    init_faiss_index()
    app.run(host='0.0.0.0', port=os.environ['PORT'])