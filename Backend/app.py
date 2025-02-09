from flask import Flask, request, render_template, jsonify,send_from_directory
import os
from dotenv import load_dotenv
import google.generativeai as genai
import sqlite3
import pandas as pd
from flask_cors import CORS
import re
import time
from flask_cors import cross_origin
from evaluation import final_score

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
    -- Sql Query :  SELECT employee_id, employee_name, salary
                    CASE 
                        WHEN salary < 50000 THEN 'Low'
                        WHEN salary BETWEEN 50000 AND 100000 THEN 'Medium'
                        ELSE 'High'
                    END AS salary_category
                    FROM employees;
                    
    --- 11. Date format
    --- User Query : "What product line is in the latest entry?"
    --- sql query : "SELECT product_line
                    FROM your_table 
                    ORDER BY date(substr(date_column, 7, 4) || '-' || substr(date_column, 4, 2) || '-' || substr(date_column, 1, 2)) DESC 
                    LIMIT 1;"
                    
    ### Given User Query : {text}
    ### Table Name : {table_title}
    ### Table info : {table_info}
   
    #Output format
    In output with the query you should return the column name and the row index that are involved to execute the query.
    
    ## Example 
    SELECT MAX(Rating) FROM tableName WHERE `Product line` = 'Home and lifestyle'
    columns Involved : ["Rating","Product line"]
    Row Involved : [In my table it have ROW_ID column. Write the sql query to get the ROW_ID of rows that are involved to execute the query.]
    
    When you genearte the query then if date , month if it is in one digit keep it is in one digit only
    1/5/2019 it should be 1/5/2019 . Do not convert it to 01/05/2019
    To get the Column index you should refer the table info.
    
    only provide the python dictionary , no need to explain anything. 
    
    python dictionary
        sql_query: .....,
        columns : .....,
        row_query : ....
    
    Now generate the query .
    '''

def extract_sql_query(response):
    # print(response.text)
    dict = response.text.strip()
    dict = re.sub(r"```(?:python)?\s*", "", dict)
    dict = re.sub(r"```", "", dict)
    return dict

def extract_name(filename):
    return filename.rsplit('.', 1)[0]

def extract_type(filename):
    return filename.rsplit('.', 1)[1]

def csv_to_db(file):
    df = pd.read_csv(file)
    df.insert(0, "ROW_ID", range(0, len(df)))
    df.to_csv("updated_input")
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
    
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not tables:
        conn.close()
        return jsonify({"error": "No tables found in database"}), 500
    
    table_title = tables[0]
    table_schemas = {}
    table_info = ""
    
    table_title = tables[0]
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_info = cursor.fetchall()
        schema = {col[1]: col[2] for col in table_info} 
        table_schemas[table_name] = schema
    
    
    df = pd.read_excel("predicted.xlsx")
    queries = df['question']
  
    query_list = queries.iloc[0:len(queries)]
    
    filtered_rows = []
    filtered_cols = []
    generated_responses = []

    for query in query_list:
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        prompt = sql_query_generation_prompt(query,table_title, table_schemas)
        time.sleep(5)
        response = generate_response(prompt)
       
        data_dict = extract_sql_query(response)
        data_dict = eval(data_dict)
        
        try:
            cursor.execute(data_dict['sql_query'])
            ans = cursor.fetchall()
            ans = ",".join(str(row[0]) for row in ans) if ans else "" 

            cursor.execute(data_dict['row_query'])
            rows = cursor.fetchall()
            rows_str = ",".join(str(row[0]) for row in rows) if rows else "" 
        except Exception as e:
            ans = ""     
            rows_str = "" 
        
        cols = data_dict['columns']
        col_list = []
        for col in cols:
            for col_info in table_info:
                if col_info[1] == col: 
                    col_list.append(col_info[0]-1)
                    break 
       
        col_str = ",".join(map(str, col_list))
     
        filtered_rows.append(rows_str)
        filtered_cols.append(col_str)
        generated_responses.append(ans)
        
    while(len(filtered_rows) != len(queries)): 
        filtered_rows.append("")
        filtered_cols.append("")
        generated_responses.append("")
        
    # Assign lists to DataFrame columns
    df['filtered row index'] = filtered_rows
    df['filtered column index'] = filtered_cols
    df['generated response'] = generated_responses
    
    df.to_excel("predicted.xlsx")
    conn.close()
    
    file_path = "static/files/predicted.xlsx"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)

    return jsonify({'status': "ok", 'url': f"http://localhost:5000/download_file/predicted.xlsx"})


@app.route('/download_file/<filename>', methods=["GET"])
def download_file(filename): 
    return send_from_directory("static/files", filename, as_attachment=True)

@app.route('/evalute-file',methods=["POST"])
@cross_origin()
def evalute_file():
    table_score,res_score,total_score,f_score = final_score(1000,11)
    return jsonify({
    'status':"ok",
    'score': {
        'table_score': table_score,
        'res_score': res_score,
        'total_score': total_score,
        'f_score': f_score
    }
    })
    
if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
