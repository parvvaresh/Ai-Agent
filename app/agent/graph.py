import operator
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from app.core.config import settings
from app.agent.tools import execute_query_tool

# Define the tools that the agent can use
tools = [execute_query_tool]
tool_executor = ToolExecutor(tools)

# Define the LLM model (Gemini)
# temperature=0 makes responses more deterministic and less creative, which is suitable for generating SQL queries.
model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=settings.GOOGLE_API_KEY, temperature=0)

# Bind tools to the model
# This allows the model to know which tools are available and how to use them.
model_with_tools = model.bind_tools(tools)

class AgentState(TypedDict):
    """
    Defines the state of the graph. This dictionary passes information between different graph nodes.
    """
    messages: Annotated[List[BaseMessage], operator.add]

def should_continue(state: AgentState) -> str:
    """
    A conditional node that decides whether the cycle should continue or end.
    """
    last_message = state["messages"][-1]
    # If the last message does not have any tool calls, the LLM has reached a final answer.
    if not last_message.tool_calls:
        return "end"
    # Otherwise, proceed to the tool execution node.
    return "continue"

def call_model(state: AgentState) -> dict:
    """
    Node that calls the LLM model.
    """
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    # Append the model's response to the message list.
    return {"messages": [response]}

def call_tool(state: AgentState) -> dict:
    """
    Node that executes the tool selected by the model.
    """
    last_message = state["messages"][-1]
    # Execute all tool calls
    tool_invocations = []
    for tool_call in last_message.tool_calls:
        action = {"tool_name": tool_call["name"], "tool_input": tool_call["args"]}
        tool_invocations.append(action)

    # Run the tools
    tool_outputs = tool_executor.batch(tool_invocations, return_exceptions=True)
    
    # Convert tool outputs into messages appropriate for the LLM
    tool_messages = []
    for tool_call, output in zip(last_message.tool_calls, tool_outputs):
        tool_messages.append(
            {"tool_call_id": tool_call["id"], "role": "tool", "content": str(output)}
        )
    
    return {"messages": tool_messages}

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes to the graph
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

# Define the graph entry point
workflow.set_entry_point("agent")

# Add conditional edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

# Add edge from tool node back to agent node
workflow.add_edge("action", "agent")

# Compile the graph to create an executable agent
app_graph = workflow.compile()
