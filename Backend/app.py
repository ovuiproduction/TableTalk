# from flask import Flask, request, render_template ,jsonify
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# import sqlite3
# import pandas as pd
# from flask_cors import CORS

# app = Flask(__name__, template_folder="templates", static_folder="static")
# CORS(app)

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)
# genai_model = genai.GenerativeModel("gemini-1.5-flash")


# def generate_response(prompt):
#     response = genai_model.generate_content(prompt)
#     return response.text

# def sql_query_generation_prompt(text):
#     prompt = f'''
    
#     '''
#     return prompt

# def extract_name(filename):
#     return filename.rsplit('.', 1)[0]

# def extract_type(filename):
#     return filename.rsplit('.', 1)[1]


# def csv_to_db(file):
#     df = pd.read_csv(file)
#     db_file = extract_name(file.filename) + ".db"  # Ensure correct file extension
#     conn = sqlite3.connect(db_file)
#     df.to_sql("tableName", conn, if_exists="replace", index=False)
#     conn.close()
#     return db_file


# def excel_to_db(file):
#     df = pd.read_excel(file)
#     db_file = extract_name(file.filename) + ".db"
#     conn = sqlite3.connect(db_file)
#     df.to_sql("tableName", conn, if_exists="replace", index=False)
#     conn.close()
#     return db_file


# def sql_to_db(file):
#     db_file = extract_name(file.filename) + ".db"
    
#     if os.path.exists(db_file):
#         os.remove(db_file)
        
#     file.save(os.path.join('uploads', file.filename))

#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()

#     with open(os.path.join('uploads', file.filename), "r", encoding="utf-8") as f:
#         sql_script = f.read()
        
#     sql_script = sql_script.replace("AUTO_INCREMENT", "AUTOINCREMENT")
#     sql_script = sql_script.replace("ENGINE=InnoDB;", "") 

#     try:
#         cursor.executescript(sql_script)
#         conn.commit()
#     except sqlite3.Error as e:
#         return f"SQL Error: {str(e)}"
#     finally:
#         conn.close()

#     return db_file



# @app.route('/')
# def cover():
#     return render_template('index.html')


# @app.route('/process-file', methods=['POST'])
# def processFile():
#     file = request.files['file']
#     if not file:
#         return "No file uploaded", 400
    
#     file_type = extract_type(file.filename)
#     if file_type == "csv":
#         db = csv_to_db(file)
#     elif file_type == "xlsx":
#         db = excel_to_db(file)
#     elif file_type == "sql":
#         db = sql_to_db(file)
#     else:
#         return "Unsupported file format", 400

#     conn = sqlite3.connect(db)
#     global cursor = conn.cursor()

#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     table_row = cursor.fetchone()
#     if not table_row:
#         return "No table found in database", 500
#     table_name = table_row[0]

#     cursor.execute(f"SELECT * FROM {table_name}")
#     data = cursor.fetchall()
#     conn.close()
#     return jsonify(data)


# @app.route('/query',methods=['POST'])
# def userQuery():
#     query = request.form['query']
#     prompt = sql_query_generation_prompt(query)
#     sql_query = generate_response(prompt)
#     cursor.execute(sql_query)
#     data = cursor.fetchAll()
#     print(data)
#     return data
    

# if __name__ == '__main__':
#     os.makedirs("uploads", exist_ok=True)
#     app.run(host="0.0.0.0", port=5000)


# from flask import Flask, request, render_template, jsonify
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# import sqlite3
# import pandas as pd
# from flask_cors import CORS

# app = Flask(__name__, template_folder="templates", static_folder="static")
# CORS(app)

# # Load API key from environment variables
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)
# genai_model = genai.GenerativeModel("gemini-1.5-flash")

# db_filename = None  # Store the uploaded database filename globally

# def generate_response(prompt):
#     response = genai_model.generate_content(prompt)
#     return response.text if response and response.text else ""

# def sql_query_generation_prompt(text,table_info):
#     return f'''
#     You are expert in converting the natural language query to corresponding sql query. Convert natural language queries into accurate SQL queries based on the given table schema and the natural language query. Ensure that the generated SQL queries handle various types of queries, including simple retrieval, complex retrieval, simple operations, complex operations, and multi-step queries.
    
#     Guidelines for Query Conversion:

#     Understand the Intent:
#         Analyze the user's query to determine what data needs to be retrieved or processed.
#         Identify the required tables, columns, and conditions.
#         Ensure SQL Accuracy:
#         Generate syntactically correct SQL queries.
#         Use appropriate joins, conditions, and grouping operations where necessary.

#     Handle Various Query Types:
#         Simple retrieval queries
#         Complex retrieval queries
#         Simple operations (SUM, COUNT, MIN, MAX, AVG, etc.)
#         Complex operations involving multiple conditions and aggregations
#         Multi-step queries where one query's output serves as input for another
    
#     Edge Case Handling:
#         Missing columns or incorrect column references
#         Handling NULL values
#         Ensuring efficient query execution
    
#     Example Queries and Their SQL Conversions:
    
#     -- 1. Simple Retrieval Query
#     -- User Query: "Retrieve all employees from the 'employees' table."
#     -- Sql Query : SELECT * FROM employees;

#     -- 2. Complex Retrieval Query
#     -- User Query: "Find all employees who work in the 'HR' department and earn more than $50,000."
#     -- Sql Query : SELECT * FROM employees WHERE department = 'HR' AND salary > 50000;

#     -- 3. Simple Operation Query
#     -- User Query: "Find the total salary paid to employees."
#     -- Sql Query : SELECT SUM(salary) AS total_salary FROM employees;

#     -- 4. Complex Operational Query
#     -- User Query: "Find the average salary of employees in each department."
#     -- Sql Query : SELECT department, AVG(salary) AS avg_salary FROM employees GROUP BY department;

#     -- 5. Multi-Step Query
#     -- User Query: "Find the department with the highest total salary expense."
#     -- Sql Query : WITH DepartmentSalary AS (
#         SELECT department, SUM(salary) AS total_salary 
#         FROM employees 
#         GROUP BY department
#         )
#         SELECT department FROM DepartmentSalary ORDER BY total_salary DESC LIMIT 1;

#     -- 6. Join Query (Multiple Tables)
#     -- User Query: "Retrieve all orders along with customer names from 'orders' and 'customers' tables."
#     -- Sql Query :  SELECT orders.order_id, customers.customer_name, orders.order_date 
#                     FROM orders
#                     JOIN customers ON orders.customer_id = customers.customer_id;

#     -- 7. Query with Subquery
#     -- User Query: "Find employees who earn more than the average salary."
#     -- Sql Query :  SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);

#     -- 8. Query with Date Filtering
#     -- User Query: "Retrieve all orders placed in the last 30 days."
#     -- Sql Query : SELECT * FROM orders WHERE order_date >= NOW() - INTERVAL 30 DAY;

#     -- 9. Handling NULL Values
#     -- User Query: "Retrieve all customers who have not placed any orders."
#     -- Sql Query :  SELECT customers.* FROM customers
#                     LEFT JOIN orders ON customers.customer_id = orders.customer_id
#                     WHERE orders.order_id IS NULL;

#     -- 10. Query with CASE Statement
#     -- User Query: "Categorize employees based on salary: Low (<50K), Medium (50K-100K), High (>100K)."
#     -- Sql Query :  SELECT employee_id, employee_name, salary,
#                     CASE 
#                         WHEN salary < 50000 THEN 'Low'
#                         WHEN salary BETWEEN 50000 AND 100000 THEN 'Medium'
#                         ELSE 'High'
#                     END AS salary_category
#                     FROM employees;

#     ### Given User Query : {text}
#     ### Table info : {table_info}
    
#     #Output format
#     only provide the sql query , no need to explain anything only sql query
    
#     Now generate the query .
# '''

# def extract_name(filename):
#     return filename.rsplit('.', 1)[0]

# def extract_type(filename):
#     return filename.rsplit('.', 1)[1]

# def csv_to_db(file):
#     df = pd.read_csv(file)
#     db_file = extract_name(file.filename) + ".db"
#     conn = sqlite3.connect(db_file)
#     df.to_sql("tableName", conn, if_exists="replace", index=False)
#     conn.close()
#     return db_file

# def excel_to_db(file):
#     df = pd.read_excel(file)
#     db_file = extract_name(file.filename) + ".db"
#     conn = sqlite3.connect(db_file)
#     df.to_sql("tableName", conn, if_exists="replace", index=False)
#     conn.close()
#     return db_file

# def sql_to_db(file):
#     db_file = extract_name(file.filename) + ".db"
#     if os.path.exists(db_file):
#         os.remove(db_file)
#     os.makedirs("uploads", exist_ok=True)
#     file_path = os.path.join("uploads", file.filename)
#     file.save(file_path)
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             sql_script = f.read().replace("AUTO_INCREMENT", "AUTOINCREMENT").replace("ENGINE=InnoDB;", "")
#         cursor.executescript(sql_script)
#         conn.commit()
#     except sqlite3.Error as e:
#         return f"SQL Error: {str(e)}"
#     finally:
#         conn.close()
#     return db_file

# @app.route('/')
# def cover():
#     return render_template('index.html')

# @app.route('/process-file', methods=['POST'])
# def process_file():
#     global db_filename
#     file = request.files.get('file')
#     if not file:
#         return jsonify({"error": "No file uploaded"}), 400
#     file_type = extract_type(file.filename)
#     if file_type == "csv":
#         db_filename = csv_to_db(file)
#     elif file_type == "xlsx":
#         db_filename = excel_to_db(file)
#     elif file_type == "sql":
#         db_filename = sql_to_db(file)
#     else:
#         return jsonify({"error": "Unsupported file format"}), 400
#     return jsonify({"database": db_filename})

# @app.route('/process-query', methods=['POST'])
# def user_query():
#     global db_filename
    
#     if not db_filename:
#         return jsonify({"error": "No database available. Upload a file first."}), 400
    
#     query = request.form.get('query')
#     if not query:
#         return jsonify({"error": "No query provided"}), 400
   
#     conn = sqlite3.connect(db_filename)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchone()
#     if not tables:
#         conn.close()
#         return jsonify({"error": "No table found in database"}), 500
#     table_name = tables[0]
#     # cursor.execute(f"PRAGMA table_info({table_name})")
#     # columns = [row[1] for row in cursor.fetchall()]
#     cursor.execute(f"Describe {table_name}")
#     table_info = cursor.fetchall()
#     if not table_info:
#         return jsonify({"error": "No columns found in the table"}), 400
    
#     prompt = sql_query_generation_prompt(query,table_info)
#     sql_query = generate_response(prompt)
#     print(sql_query)
#     # if not sql_query:
#     #     return jsonify({"error": "Failed to generate SQL query"}), 500
    
#     # try:
#     #     cursor.execute(sql_query)
#     #     data = cursor.fetchall()
#     # except sqlite3.Error as e:
#     #     conn.close()
#     #     return jsonify({"error": f"SQL Error: {str(e)}"}), 500
#     # conn.close()
#     # return jsonify(data)
#     return jsonify(sql_query)

# if __name__ == '__main__':
#     os.makedirs("uploads", exist_ok=True)
#     app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai
import sqlite3
import pandas as pd
from flask_cors import CORS
import re

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Load API key from environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in environment variables.")

genai.configure(api_key=GOOGLE_API_KEY)
genai_model = genai.GenerativeModel("gemini-1.5-flash")

db_filename = None  # Store the uploaded database filename globally

def generate_response(prompt):
    response = genai_model.generate_content(prompt)
    return response

def sql_query_generation_prompt(text,table_title, table_info):
    return f'''
    You are expert in converting the natural language query to corresponding sql query. Convert natural language queries into accurate SQL queries based on the given table schema and the natural language query. Ensure that the generated SQL queries handle various types of queries, including simple retrieval, complex retrieval, simple operations, complex operations, and multi-step queries.
    
    Guidelines for Query Conversion:

    Understand the Intent:
        Analyze the user's query to determine what data needs to be retrieved or processed.
        Identify the required tables, columns, and conditions.
        Ensure SQL Accuracy:
        Generate syntactically correct SQL queries.
        Use appropriate joins, conditions, and grouping operations where necessary.

    Handle Various Query Types:
        Simple retrieval queries
        Complex retrieval queries
        Simple operations (SUM, COUNT, MIN, MAX, AVG, etc.)
        Complex operations involving multiple conditions and aggregations
        Multi-step queries where one query's output serves as input for another
    
    Edge Case Handling:
        Missing columns or incorrect column references
        Handling NULL values
        Ensuring efficient query execution
    
    Example Queries and Their SQL Conversions:
    
    -- 1. Simple Retrieval Query
    -- User Query: "Retrieve all employees from the 'employees' table."
    -- Sql Query : SELECT * FROM employees;

    -- 2. Complex Retrieval Query
    -- User Query: "Find all employees who work in the 'HR' department and earn more than $50,000."
    -- Sql Query : SELECT * FROM employees WHERE department = 'HR' AND salary > 50000;

    -- 3. Simple Operation Query
    -- User Query: "Find the total salary paid to employees."
    -- Sql Query : SELECT SUM(salary) AS total_salary FROM employees;

    -- 4. Complex Operational Query
    -- User Query: "Find the average salary of employees in each department."
    -- Sql Query : SELECT department, AVG(salary) AS avg_salary FROM employees GROUP BY department;

    -- 5. Multi-Step Query
    -- User Query: "Find the department with the highest total salary expense."
    -- Sql Query : WITH DepartmentSalary AS (
        SELECT department, SUM(salary) AS total_salary 
        FROM employees 
        GROUP BY department
        )
        SELECT department FROM DepartmentSalary ORDER BY total_salary DESC LIMIT 1;

    -- 6. Join Query (Multiple Tables)
    -- User Query: "Retrieve all orders along with customer names from 'orders' and 'customers' tables."
    -- Sql Query :  SELECT orders.order_id, customers.customer_name, orders.order_date 
                    FROM orders
                    JOIN customers ON orders.customer_id = customers.customer_id;

    -- 7. Query with Subquery
    -- User Query: "Find employees who earn more than the average salary."
    -- Sql Query :  SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);

    -- 8. Query with Date Filtering
    -- User Query: "Retrieve all orders placed in the last 30 days."
    -- Sql Query : SELECT * FROM orders WHERE order_date >= NOW() - INTERVAL 30 DAY;

    -- 9. Handling NULL Values
    -- User Query: "Retrieve all customers who have not placed any orders."
    -- Sql Query :  SELECT customers.* FROM customers
                    LEFT JOIN orders ON customers.customer_id = orders.customer_id
                    WHERE orders.order_id IS NULL;

    -- 10. Query with CASE Statement
    -- User Query: "Categorize employees based on salary: Low (<50K), Medium (50K-100K), High (>100K)."
    -- Sql Query :  SELECT employee_id, employee_name, salary,
                    CASE 
                        WHEN salary < 50000 THEN 'Low'
                        WHEN salary BETWEEN 50000 AND 100000 THEN 'Medium'
                        ELSE 'High'
                    END AS salary_category
                    FROM employees;

    ### Given User Query : {text}
    ### Table Name : {table_title}
    ### Table info : {table_info}
    
    #Output format
    only provide the sql query , no need to explain anything only sql query
    
    Now generate the query .
    '''
    # return f'''
    # You are an expert in converting natural language queries to SQL. Generate accurate SQL queries based on the given table schema and user query.
    
    # User Query: {text}
    # Table Name : {table_title}
    # Table Schema: {table_info}
    
    # Only return the SQL query without any explanation.
    # '''

def extract_sql_query(response):
    sql_query = response.text.strip()
    sql_query = re.sub(r"```(?:sql)?\s*", "", sql_query)
    sql_query = re.sub(r"```", "", sql_query)
    return sql_query

def extract_name(filename):
    return filename.rsplit('.', 1)[0]

def extract_type(filename):
    return filename.rsplit('.', 1)[1]

def csv_to_db(file):
    df = pd.read_csv(file)
    db_file = extract_name(file.filename) + ".db"
    conn = sqlite3.connect(db_file)
    df.to_sql("tableName", conn, if_exists="replace", index=False)
    conn.close()
    return db_file

def excel_to_db(file):
    df = pd.read_excel(file)
    db_file = extract_name(file.filename) + ".db"
    conn = sqlite3.connect(db_file)
    df.to_sql("tableName", conn, if_exists="replace", index=False)
    conn.close()
    return db_file

def sql_to_db(file):
    db_file = extract_name(file.filename) + ".db"
    if os.path.exists(db_file):
        os.remove(db_file)
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sql_script = f.read().replace("AUTO_INCREMENT", "AUTOINCREMENT").replace("ENGINE=InnoDB;", "")
        cursor.executescript(sql_script)
        conn.commit()
    except sqlite3.Error as e:
        return f"SQL Error: {str(e)}"
    finally:
        conn.close()
    return db_file

@app.route('/')
def cover():
    return render_template('index.html')

@app.route('/process-file', methods=['POST'])
def process_file():
    global db_filename
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    file_type = extract_type(file.filename)
    if file_type == "csv":
        db_filename = csv_to_db(file)
    elif file_type == "xlsx":
        db_filename = excel_to_db(file)
    elif file_type == "sql":
        db_filename = sql_to_db(file)
    else:
        return jsonify({"error": "Unsupported file format"}), 400
    return jsonify({"database": db_filename})

@app.route('/process-query', methods=['POST'])
def user_query():
    global db_filename
    
    if not db_filename:
        return jsonify({"error": "No database available. Upload a file first."}), 400
    
    query = request.form.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
   
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        conn.close()
        return jsonify({"error": "No tables found in database"}), 500
    
    table_schemas = {}
    table_title = tables[0]
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_info = cursor.fetchall()
        schema = {col[1]: col[2] for col in table_info}  # {column_name: data_type}
        table_schemas[table_name] = schema

    
    prompt = sql_query_generation_prompt(query,table_title, table_schemas)
    response = generate_response(prompt)

    sql_query = extract_sql_query(response)
    print(sql_query)
    
    cursor.execute(sql_query)
    data = cursor.fetchall()
   
    conn.close()
    return jsonify({'data':data})

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
