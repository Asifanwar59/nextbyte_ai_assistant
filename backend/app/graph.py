# app/graph.py
from langgraph.graph import StateGraph, START, END
from guardrails import Guard
from guardrails.hub import DetectJailbreak, ToxicLanguage # 2026 hub validators

# Define the Agent State
class AgentState(TypedDict):
    messages: List[BaseMessage]
    context: List[str]
    is_safe: bool

# Initialize Guardrails
input_guard = Guard().use(DetectJailbreak, on_fail="exception")
output_guard = Guard().use(ToxicLanguage, on_fail="fix")

def retrieve_node(state: AgentState):
    # Logic to fetch from PDF vector store
    return {"context": ["...document chunks..."]}

def generate_node(state: AgentState):
    # Apply output guardrail to LLM response
    raw_response = llm.invoke(state["messages"])
    safe_response = output_guard.validate(raw_response.content)
    return {"messages": [AIMessage(content=safe_response.validated_output)]}

# Assemble Graph
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)
graph = workflow.compile()
