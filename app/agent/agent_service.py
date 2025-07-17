from langchain_core.messages import HumanMessage
from app.agent.graph import app_graph, db

class AgentService:
    """
    This service encapsulates the logic for interacting with the LangGraph agent.
    """
    def __init__(self):
        # Get the database schema information to provide to the LLM
        self.db_schema = db.get_table_info()

    def _create_prompt(self, query: str) -> str:
        """
        Create a complete and structured prompt for the LLM.
        """
        prompt_template = f"""
        You are a smart agent specialized in MySQL databases.
        Your task is to answer user questions about the store data.
        You must convert natural language questions (in Persian) into precise SQL queries and execute them.

        Important notes:
        1. Only use the tools provided to you.
        2. Never create queries that modify data (UPDATE, DELETE, INSERT). Use SELECT only.
        3. Provide the final answer in Persian, briefly and clearly for a non-technical user.
        4. If the question is ambiguous or cannot be executed, inform the user.

        Database schema is as follows:
        ---
        {self.db_schema}
        ---

        User question: "{query}"

        Now, determine the necessary steps to answer this question, and if needed, generate and execute the appropriate SQL query.
        """
        return prompt_template.strip()

    async def run_agent(self, query: str, session_id: str) -> str:
        """
        Run the agent graph with a given query.
        """
        # Build the full prompt
        full_prompt = self._create_prompt(query)
        
        # Initial input for the graph
        inputs = {"messages": [HumanMessage(content=full_prompt)]}
        
        # Run the graph asynchronously
        final_state = await app_graph.ainvoke(inputs)
        
        # Extract the final response from the last message
        response_message = final_state["messages"][-1]
        
        return response_message.content

agent_service = AgentService()
