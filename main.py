from fastmcp import FastMCP
import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")


mcp = FastMCP("ExpenseTracker")

def init_db():
	with sqlite3.connect(DB_PATH) as c:
		c.execute('''CREATE TABLE IF NOT EXISTS expenses (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					date TEXT NOT NULL,
					amount REAL NOT NULL,
					category TEXT NOT NULL,
					subcategory TEXT DEFAULT '',
					note TEXT DEFAULT '' )
				'''
				)
init_db()

@mcp.tool
def add_expense(date,amount,category,subcategory="", note=""):
	'''Add a new expenses entry to the database.'''
	with sqlite3.connect(DB_PATH) as cur:
		cur = cur.execute("INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
		      (date,amount,category,subcategory,note)
        )
		return {"status":"ok", "id": cur.lastrowid}

@mcp.tool
def list_expenses(start_date, end_date):
	'''list all the expenses entries from the database within an inclusive date range.'''
	with sqlite3.connect(DB_PATH) as cur:
		cur = cur.execute("SELECT id, date, amount, category, subcategory, note FROM expenses WHERE date BETWEEN ? and ? ORDER BY id ASC", (start_date, end_date))
		cols = [d[0] for d in cur.description]
		return [dict(zip(cols,r)) for r in cur.fetchall()]


@mcp.tool 
def delete_an_item(id):
    '''remove an item from the expenses database.'''
    with sqlite3.connect(DB_PATH) as conn:
        conn = conn.execute("DELETE FROM expenses where id = ?", (id))
        return {"status": "Deletion Successfull."}
    
@mcp.tool
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    query = '''SELECT category, SUM(amount) AS total_amount
    		   FROM expenses 
         	   WHERE date BETWEEN ? AND ?'''
    
    params = [start_date, end_date]
    
    if category:
        query += "AND category = ?"
    
    query += "GROUPBY category order by category ASC"
    
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    
@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    "Read fresh each time so you can edit the file without restarting"
    with open(CATEGORIES_PATH, "r", encoding='utf-8') as f:
        return f.read()
    
    
if __name__ == "__main__":
   mcp.run(transport="http", host="0.0.0.0", port=8000)

