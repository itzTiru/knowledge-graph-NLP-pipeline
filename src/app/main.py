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
    
    progress_bar = st.progress(0)
    
    max_sentences = st.sidebar.slider("Max Sentences to Process", 5, 100, 20)
    
    for i, sent in enumerate(sentences[:max_sentences]):
        ents = ner_extractor.extract_entities(sent)
        ents = [e for e in ents if e['score'] > 0.8]
        
        rels = relation_extractor.extract_relations(sent, ents)
        
        all_entities.extend(ents)
        all_relations.extend(rels)
        progress_bar.progress((i + 1) / max_sentences)
        
    st.success(f"Extracted {len(all_entities)} entities and {len(all_relations)} relations.")
    
    if st.button("Build Knowledge Graph"):
        graph_builder.create_graph(all_entities, all_relations)
        st.success("Graph built in Neo4j!")
        
        st.subheader("Graph Visualization")
        reasoner.load_graph_from_neo4j()
        
        net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", directed=True)
        net.from_nx(reasoner.nx_graph)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
            net.save_graph(tmp_html.name)
            with open(tmp_html.name, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
        components.html(html_content, height=600, scrolling=True)

        st.subheader("Graph Analysis")
        centrality = reasoner.calculate_centrality()
        if centrality:
            st.write("Top 5 Central Nodes:")
            st.write(centrality[:5])
            
    os.remove(tmp_path)
