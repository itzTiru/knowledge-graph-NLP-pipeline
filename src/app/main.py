import streamlit as st
import os
import tempfile
from pyvis.network import Network
import streamlit.components.v1 as components

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.document_processing.loader import DocumentLoader
from src.document_processing.cleaner import TextCleaner
from src.nlp.ner import NERExtractor
from src.nlp.re import RelationExtractor
from src.graph.builder import GraphBuilder
from src.reasoning.analysis import GraphReasoner

@st.cache_resource
def load_models():
    ner = NERExtractor()
    re_extractor = RelationExtractor()
    return ner, re_extractor

ner_extractor, relation_extractor = load_models()
loader = DocumentLoader()
cleaner = TextCleaner()
graph_builder = GraphBuilder()
reasoner = GraphReasoner()

st.set_page_config(page_title="Knowledge Graph Extractor", layout="wide")

st.title("Knowledge Graph Extraction System")

st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt', 'pdf', 'html'])

if st.sidebar.button("Clear Graph"):
    graph_builder.clear_graph()
    st.sidebar.success("Graph cleared!")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    st.info("Processing document...")
    
    text = loader.load(tmp_path)
    st.text_area("Extracted Text (Snippet)", text[:500] + "...", height=150)
    
    cleaned_text = cleaner.clean(text)
    sentences = cleaner.split_sentences(cleaned_text)
    st.write(f"Found {len(sentences)} sentences.")
    
    all_entities = []
    all_relations = []
    
