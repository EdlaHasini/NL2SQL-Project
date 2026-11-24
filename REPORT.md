# NL2SQL – AI-Powered Natural Language to SQL Interface

## 1. Project Overview

NL2SQL is an AI-powered application that allows users to interact with a database using simple English language questions instead of writing SQL queries manually.

The application uses an AI language model to understand user questions, generate SQL queries, execute them on an E-commerce database, and display the results through tables and visualizations.

The main aim of this project is to make database interaction easier, faster, and accessible to non-technical users.

## 2. Objectives

- Convert natural language questions into SQL queries.
- Allow users to retrieve information without knowing SQL.
- Connect an AI model with an SQLite database.
- Provide automatic data visualization.
- Implement security checks to prevent unsafe SQL operations.
- Improve query generation using retry and self-healing mechanisms.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | User interface |
| Ollama | Runs the local AI model |
| SQLCoder | Generates SQL queries |
| SQLite | Database management |
| Pandas | Data processing |
| Plotly | Interactive visualizations |
| SQLAlchemy | Database-related operations |
| SQLParse | SQL query parsing |
| Git & GitHub | Version control and project hosting |

## 4. System Architecture

The application follows this workflow:

1. User enters a question in the Streamlit interface.
2. The question is sent to the NL2SQL engine.
3. The AI model understands the question.
4. The engine generates an SQL query.
5. Security checks validate the generated query.
6. The query is executed against the SQLite database.
7. The result is returned as a Pandas DataFrame.
8. The visualization module generates charts or displays results.

### Architecture Flow

User Question  
↓  
Streamlit Interface  
↓  
NL2SQL Engine  
↓  
Ollama / SQLCoder  
↓  
SQL Query Generation  
↓  
Security Validation  
↓  
SQLite Database  
↓  
Pandas DataFrame  
↓  
Automatic Visualization  
↓  
Display Results to User

## 5. Database Description

The project uses an E-commerce sample database named `ecommerce.db`.

The database contains three main tables:

### Customers Table

Stores customer information.

- customer_id
- name
- email
- city

### Products Table

Stores product information.

- product_id
- product_name
- category
- price

### Orders Table

Stores customer order information.

- order_id
- customer_id
- order_date
- total_amount

These tables provide sample data for testing natural language queries.

## 6. Project Modules

### 6.1 app.py

This is the main application file.

Responsibilities:
- Creates the Streamlit interface.
- Displays the database schema.
- Accepts user questions.
- Calls the NL2SQL engine.
- Displays generated SQL queries.
- Shows query results and visualizations.

### 6.2 nl2sql_engine.py

This module handles natural language to SQL conversion.

Responsibilities:
- Retrieves database schema.
- Sends user questions to the AI model.
- Generates SQL queries.
- Handles query retries and corrections.
- Returns the generated SQL query and result DataFrame.

### 6.3 security.py

This module provides SQL security validation.

Responsibilities:
- Checks generated SQL queries.
- Identifies potentially unsafe SQL operations.
- Helps prevent unauthorized database modifications.

### 6.4 visualizer.py

This module handles automatic data visualization.

Responsibilities:
- Accepts query results.
- Analyzes the returned DataFrame.
- Generates suitable visualizations using Plotly.

### 6.5 setup_db.py

This file creates the sample E-commerce database.

Responsibilities:
- Creates database tables.
- Inserts sample customer information.
- Inserts sample product information.
- Inserts sample order information.

## 7. Security Features

The project focuses on safe database interaction.

The security layer is designed to:

- Restrict database operations to read-only queries.
- Detect potentially dangerous SQL commands.
- Validate generated queries before execution.
- Use database-level read-only access where configured.

The database execution layer should enforce read-only access independently of the SQL validation checks.

## 8. Self-Healing Mechanism

The project includes a retry mechanism for handling SQL generation or execution errors.

When an error occurs, the engine can attempt to correct the generated query and retry the operation.

This helps improve query reliability and reduces the need for users to manually write or correct SQL queries.

## 9. Sample User Queries

Users can enter questions such as:

1. Show all customers.
2. List all available products.
3. Find products in the Electronics category.
4. Show the total number of customers.
5. Find the total order amount.
6. Display customer orders.
7. Show products and their prices.

The AI converts supported questions into SQL queries and displays the results.

## 10. How to Run the Project

### Step 1: Activate the virtual environment

```bash
source nl2sql_env/Scripts/activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Create the database

```bash
python setup_db.py
```

### Step 4: Start Ollama

```bash
ollama run sqlcoder
```

Keep Ollama running.

### Step 5: Start the Streamlit application

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run app.py
```

### Step 6: Open the application

Visit:

```text
http://localhost:8501
```

Enter a natural language question and click the Generate & Run Query button.

## 11. Advantages

- Easy database interaction.
- No need to write SQL manually.
- Faster data retrieval.
- Automatic visualization.
- Local AI model support through Ollama.
- Security-focused query validation.
- User-friendly interface.

## 12. Future Enhancements

- Support multiple database systems.
- Improve AI query accuracy.
- Add user authentication.
- Support more complex SQL queries.
- Add query history.
- Improve error handling and self-correction.
- Provide downloadable reports and visualizations.

## 13. Conclusion

The NL2SQL project demonstrates how Artificial Intelligence can simplify database interaction by converting natural language questions into SQL queries.

By combining Python, Streamlit, Ollama, SQLCoder, SQLite, Pandas, and Plotly, the application provides an easy way to retrieve, analyze, and visualize database information.

The project helps non-technical users access database insights without requiring advanced SQL knowledge.

---

**Project Name:** NL2SQL – AI-Powered Natural Language to SQL Interface

**Repository:** https://github.com/EdlaHasini/NL2SQL-Project
