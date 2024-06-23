import yaml
import os
import sqlite3
import pandas as pd
import streamlit as st
from typing import Dict, Any
from sqlalchemy import create_engine, inspect
from llama_index.llms import AzureOpenAI
from llama_index.llm_predictor import LLMPredictor
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import SQLDatabase, ServiceContext, NLSQLTableQueryEngine

def setup_credentials(file_path: str):
    with open(file_path) as f:
        credentials = yaml.safe_load(f)
    os.environ['AD_OPENAI_API_KEY'] = credentials['AD_OPENAI_API_KEY']
    return credentials

def load_db_llm(credentials):
    engine = create_engine("sqlite:///ecommerce_platform1.db")
    sql_database = SQLDatabase(engine)
    llm = AzureOpenAI(**{
        'deployment_name': credentials['AD_DEPLOYMENT_ID'],
        'model': credentials['AD_ENGINE'],
        'api_key': credentials['AD_OPENAI_API_KEY'],
        'api_version': credentials['AD_OPENAI_API_VERSION'],
        'azure_endpoint': credentials['AD_OPENAI_API_BASE'],
        'max_tokens': 512
    })
    embedding_llm = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embedding_llm)
    return sql_database, service_context, engine

class Main(BaseLlamaPack):
    def __init__(self, page: str = "Natural Language to SQL Query", run_from_main: bool = False):
        self.page = page

    def get_modules(self) -> Dict[str, Any]:
        return {}

    def run(self):
        st.set_page_config(page_title=self.page, layout="centered", initial_sidebar_state="auto", menu_items=None)
        credentials = setup_credentials('/Users/1zuu/Desktop/LLM RESEARCH/LlamaIndex Cooking/cadentials.yaml')
        sql_database, service_context, engine = load_db_llm(credentials)

        st.title(f"{self.page}💬")
        st.info("Explore Snowflake views with this AI-powered app. Pose any question and receive exact SQL queries.", icon="ℹ️")

        def add_to_message_history(role, content):
            st.session_state.setdefault("messages", []).append({"role": role, "content": str(content)})

        def get_table_data(table_name, conn):
            query = f"SELECT * FROM {table_name}"
            return pd.read_sql_query(query, conn)

        def load_db_llm():
            # Load the SQLite database
            engine = create_engine("sqlite:///ecommerce_platform1.db")
            sql_database = SQLDatabase(engine)
            llm = AzureOpenAI(...)
            embedding_llm = HuggingFaceEmbedding(...)
            service_context = ServiceContext.from_defaults(llm=llm, embed_model=embedding_llm)
            return sql_database, service_context, engine

        # Sidebar for database schema viewer
        st.sidebar.markdown("## Database Schema Viewer")
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        selected_table = st.sidebar.selectbox("Select a Table", table_names)
        db_file = 'ecommerce_platform1.db'
        conn = sqlite3.connect(db_file)

        # Display the selected table
        if selected_table:
            df = get_table_data(selected_table, conn)
            st.sidebar.text(f"Data for table '{selected_table}':")
            st.sidebar.dataframe(df)

        conn.close()
        
        if "query_engine" not in st.session_state:  # Initialize the query engine
            st.session_state["query_engine"] = NLSQLTableQueryEngine(
                sql_database=sql_database,
                synthesize_response=True,
                service_context=service_context
            )

        for message in st.session_state["messages"]:  # Display the prior chat messages
            with st.chat_message(message["role"]):
                st.write(message["content"])


        if prompt := st.chat_input(
            "Enter your natural language query about the database"
        ):  # Prompt for user input and save to chat history
            with st.chat_message("user"):
                st.write(prompt)
            add_to_message_history("user", prompt)

        # If last message is not from assistant, generate a new response
        if st.session_state["messages"][-1]["role"] != "assistant":
            with st.spinner():
                with st.chat_message("assistant"):
                    response = st.session_state["query_engine"].query("User Question:"+prompt+". ")
                    sql_query = f"```sql\n{response.metadata['sql_query']}\n```\n**Response:**\n{response.response}\n"
                    response_container = st.empty()
                    response_container.write(sql_query)
                    # st.write(response.response)
                    add_to_message_history("assistant", sql_query)

if __name__ == "__main__":
    Main(run_from_main=True).run()
