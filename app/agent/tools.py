from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from app.database.session import sync_engine

# Create a database instance to be used by LangChain tools
# This instance uses a synchronous (blocking) connection engine
db = SQLDatabase(engine=sync_engine)

# Define a SQL query execution tool
# This tool allows the LLM (Large Language Model) to run SQL queries on the database
execute_query_tool = QuerySQLDataBaseTool(db=db)
