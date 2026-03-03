from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import json, glob, os

from env_loader import DATA_PATH

def get_pdf_loader():
    pdf_loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    return pdf_loader

def get_txt_loader():
    text_loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
    return text_loader

def _get_field_description(meta_fields: dict, field_key: str) -> str:
    """Get field description from _meta.fields"""
    if meta_fields and field_key in meta_fields:
        return meta_fields[field_key]
    return ""

def _inject_context_into_object(obj: dict, meta_fields: dict, parent_context: str = "") -> str:
    """Inject field context into each field of an object and return as string"""
    if not meta_fields:
        return json.dumps(obj, indent=2)
    
    enriched_fields = []
    for key, val in obj.items():
        field_desc = _get_field_description(meta_fields, key)
        if field_desc:
            enriched_fields.append(f"[{field_desc}] {key}: {val}")
        else:
            enriched_fields.append(f"{key}: {val}")
    
    # Add parent context if provided
    if parent_context:
        return f"[{parent_context}]\n" + "\n".join(enriched_fields)
    return "\n".join(enriched_fields)

def get_json_semantic_docs():
    docs = []
    number_of_jsons = 0
    
    for filepath in glob.glob(os.path.join(DATA_PATH, "*.json")):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            number_of_jsons += 1

        # Extract _meta information
        meta = data.get("_meta", {})
        data_type = meta.get("data_type", "")
        meta_fields = meta.get("fields", {})
        
        # Get the data key (skip _meta)
        data_keys = [k for k in data.keys() if k != "_meta"]
        
        # Get items (value of the single data key)
        items = data[data_keys[0]]
        
        if isinstance(items, list):
            # Array: experiences, projects, certificates, educations, facts
            for idx, item in enumerate(items):
                if isinstance(item, dict):
                    enriched = _inject_context_into_object(item, meta_fields, data_type)
                    docs.append(Document(
                        page_content=enriched,
                        metadata={"source": os.path.basename(filepath), "data_type": data_type, "index": idx}
                    ))
                else:
                    docs.append(Document(
                        page_content=str(item),
                        metadata={"source": os.path.basename(filepath), "data_type": data_type, "index": idx}
                    ))
        else:
            # Dict with categories/fields: skills.json, about_data.json
            for cat_key, cat_val in items.items():
                if isinstance(cat_val, list) and cat_val and isinstance(cat_val[0], dict):
                    # Category with objects (like skills)
                    cat_desc = meta.get("categories", {}).get(cat_key, "")
                    for idx, item in enumerate(cat_val):
                        enriched = _inject_context_into_object(item, meta_fields, cat_desc)
                        docs.append(Document(
                            page_content=enriched,
                            metadata={"source": os.path.basename(filepath), "section": cat_key, "data_type": data_type, "index": idx}
                        ))
                else:
                    # Simple field value
                    field_desc = meta_fields.get(cat_key, "")
                    context = f"[{field_desc}]" if field_desc else ""
                    val_str = json.dumps(cat_val, indent=2) if isinstance(cat_val, (list, dict)) else str(cat_val)
                    docs.append(Document(
                        page_content=f"{context} {cat_key}: {val_str}" if context else f"{cat_key}: {val_str}",
                        metadata={"source": os.path.basename(filepath), "section": cat_key, "data_type": data_type}
                    ))

    print(f"{number_of_jsons} found ({len(docs)} objects detected)")
    return docs

def get_text_splitter():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )
    return text_splitter