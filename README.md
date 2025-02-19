# TableTalk - Your Data, Your Language

## Overview
TableTalk is a system that enables users to interact with tabular data using natural language. Users can upload tabular data files and retrieve relevant information without writing SQL queries. The system leverages Large Language Models (LLMs) to convert natural language queries into SQL, allowing seamless data exploration and analysis.

## Features
- **Natural Language to SQL Conversion**: Translates user queries into SQL queries for efficient data retrieval.
- **Complex Query Handling**: Supports multi-step queries, aggregations, and complex retrieval tasks.
- **File Upload Support**: Allows users to upload tabular data files for analysis.
- **Intuitive UI**: User-friendly interface built with React for seamless interaction.
- **SQLite3 Integration**: Efficiently manages tabular data for querying and analysis.
- **LLM Optimization**: Implements prompt engineering techniques to improve query accuracy.

## Technologies Used
- **Frontend**: React
- **Backend**: Flask
- **Database**: SQLite3
- **AI/ML**: Large Language Models (LLMs) for query conversion
- **Optimization**: Prompt Engineering for LLM performance improvement

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Node.js & npm
- SQLite3

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/tabletalk.git
cd tabletalk/backend

# Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
```

### Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

## Usage
1. Upload a CSV/Excel file containing tabular data.
2. you can upload sql file as well.
3. Enter a natural language query (e.g., "Show me the total sales for January").
4. The system will generate and execute an SQL query.
5. View the results displayed on the UI.

## Example Queries
- `What is the average price of all products?`
- `List the top 5 customers by total purchases.`
- `Show the revenue generated each month.`

## Future Enhancements
- Support for multiple database engines
- Advanced AI-driven query optimization
- Multi-file and multi-table querying support
- Role-based access control for secure data management
