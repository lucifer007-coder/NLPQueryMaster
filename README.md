# NLPQueryMaster

This project creates a Streamlit application that allows users to interact with an SQLite database using natural language queries. The app translates user queries into SQL commands and returns the results from the database. The project leverages Azure OpenAI for natural language processing and HuggingFace for embeddings.

## Features
1. **Natural Language Interface**: Users can input queries in plain English, and the app translates them into SQL.
2. **Database Schema Viewer**: Sidebar displays the schema of the database, allowing users to explore tables and their contents.
3. **AI-Powered**: Uses Azure OpenAI for processing natural language queries and HuggingFace for embedding models.

## Requirements
- Python 3.7+
- Dependencies listed in `requirements.txt`

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Azure OpenAI Credentials
Create a `credentials.yaml` file in the root directory with your Azure OpenAI credentials:

### 3. Run the Application
```bash
streamlit run app.py
```

## File Structure
1. **app.py**: Main application file.
2. **credentials.yaml**: Configuration file for Azure OpenAI credentials (not included in the repository for security reasons).
3. **sample.db**: Example SQLite database file.
4. **requirements.txt**: List of dependencies.

## Usage
1. **Launch the App**: Run the application using the setup instructions above.
2. **Interact with the Database**: Use the chat interface to input natural language queries.
3. **View Results**: The app will display the corresponding SQL query and its results.

### Modules
1. **streamlit**: Used for creating the web interface.
2. **sqlalchemy**: For interacting with the SQLite database.
3. **llama_index**: For natural language processing and query generation.

## License
This project is licensed under the MIT License.

## Acknowledgements
1. **Streamlit** for providing an easy-to-use web application framework.
2. **Azure OpenAI** for powerful language models.
3. **HuggingFace** for state-of-the-art embeddings.
