import os
import sqlite3
from langchain.tools import tool

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _execute_query(db_name: str, sql_query: str) -> str:
    db_path = os.path.join(DATA_DIR, f"{db_name}.db")
    if not os.path.exists(db_path):
        return f"Error: Database '{db_name}.db' not found. Run 'python setup_databases.py' first."

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No results found for the given query."

        columns = rows[0].keys()
        results = []
        for row in rows[:50]:
            row_str = " | ".join(f"{col}: {row[col]}" for col in columns)
            results.append(row_str)

        output = f"Found {len(rows)} result(s):\n" + "\n".join(results)
        if len(rows) > 50:
            output += f"\n... and {len(rows) - 50} more rows (showing first 50)"
        return output

    except Exception as e:
        return f"SQL Error: {str(e)}"

@tool
def InstitutionsDBTool(sql_query: str) -> str:
    return _execute_query("institutions", sql_query)

@tool
def HospitalsDBTool(sql_query: str) -> str:
    return _execute_query("hospitals", sql_query)

@tool
def RestaurantsDBTool(sql_query: str) -> str:
    return _execute_query("restaurants", sql_query)
