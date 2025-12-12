import uuid
from typing import Dict, Any, List, Callable, Optional, Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Mini Agent Workflow Engine")

class WorkflowError(Exception):
    pass

class WorkflowGraph:
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Callable[[Dict], str]] = {}
        self.entry_point: str = ""
        self.end_point: str = "END"

    def add_node(self, name: str, func: Callable):
        """Register a node (function) that modifies stat."""
        self.nodes[name] = func

    def set_entry_point(self, node_name: str):
        self.entry_point = node_name

    def add_edge(self, from_node: str, to_node: str):
        """Define simple sequenc."""
        self.edges[from_node] = to_node

    def add_conditional_edge(self, from_node: str, condition_func: Callable[[Dict], str]):
        """Define branching/looping logic based on state."""
        self.conditional_edges[from_node] = condition_func

    async def run(self, initial_state: Dict[str, Any]):
        """Executes the graph end-to-end."""
        if not self.entry_point:
            raise WorkflowError("No entry point defined.")
        
        current_node_name = self.entry_point
        state = initial_state.copy()
        execution_log = []

        while current_node_name != self.end_point:
            if current_node_name not in self.nodes:
                raise WorkflowError(f"Node '{current_node_name}' not found.")

            # 1. Run the node
            node_func = self.nodes[current_node_name]
            try:
                # Nodes return a dict to update the state
                result_update = node_func(state)
                state.update(result_update)
                execution_log.append(f"Executed {current_node_name}")
            except Exception as e:
                execution_log.append(f"Error in {current_node_name}: {str(e)}")
                break

            # 2. Determine next node
            if current_node_name in self.conditional_edges:
                # Dynamic routing (Branching/Looping)
                next_node = self.conditional_edges[current_node_name](state)
                current_node_name = next_node
            elif current_node_name in self.edges:
                # Static routing
                current_node_name = self.edges[current_node_name]
            else:
                # Dead end, treat as finish
                break
        
        return state, execution_log

# ==========================================
# 2. OPTION B: SUMMARIZATION + REFINEMENT 
# ==========================================
# Since no ML is required, we use rule-based string manipulation.

def node_split_text(state: Dict) -> Dict:
    """Step 1: Split text into chunks"""
    text = state.get("text", "")
    # Simple rule: split by periods for this demo
    chunks = [s.strip() for s in text.split('.') if s.strip()]
    return {"chunks": chunks}

def node_generate_summaries(state: Dict) -> Dict:
    """Step 2: Generate summaries"""
    chunks = state.get("chunks", [])
    summaries = [" ".join(c.split()[:4]) + "..." for c in chunks]
    return {"chunk_summaries": summaries}

def node_merge_summaries(state: Dict) -> Dict:
    """Step 3: Merge summaries"""
    summaries = state.get("chunk_summaries", [])
    merged = " ".join(summaries)
    return {"current_summary": merged}

def node_refine_summary(state: Dict) -> Dict:
    """Step 4: Refine final summary"""
    current = state.get("current_summary", "")
    
    # Mock refinement: remove the last word to shorten it
    words = current.split()
    if len(words) > 1:
        refined = " ".join(words[:-1])
    else:
        refined = current
    return {"current_summary": refined}

def condition_check_length(state: Dict) -> str:
    """Step 5: Loop until summary length under limit"""
    current_summary = state.get("current_summary", "")
    limit = state.get("max_length")
    
    if len(current_summary.split()) > limit:
        return "refine_summary" # LOOP
    return "END"

# Register these tools/nodes
tool_registry = {
    "split_text": node_split_text,
    "generate_summaries": node_generate_summaries,
    "merge_summaries": node_merge_summaries,
    "refine_summary": node_refine_summary
}

# ==========================================
# 3. FASTAPI ENDPOINTS & IN-MEMORY DB
# ==========================================

# In-memory storage
graphs_db: Dict[str, WorkflowGraph] = {}
runs_db: Dict[str, Dict] = {}

# Pre-register the Option B graph for easy testing
def create_summarization_graph():
    graph = WorkflowGraph()
    graph.add_node("split_text", node_split_text)
    graph.add_node("generate_summaries", node_generate_summaries)
    graph.add_node("merge_summaries", node_merge_summaries)
    graph.add_node("refine_summary", node_refine_summary)
    
    graph.set_entry_point("split_text")
    graph.add_edge("split_text", "generate_summaries")
    graph.add_edge("generate_summaries", "merge_summaries")
    graph.add_edge("merge_summaries", "refine_summary")
    
    # The conditional edge handles the loop
    graph.add_conditional_edge("refine_summary", condition_check_length)
    
    return graph

graphs_db["default_summary_graph"] = create_summarization_graph()

# --- Pydantic Models ---
class GraphCreateRequest(BaseModel):
    nodes: List[str]
    edges: Dict[str, str]

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

# --- Endpoints ---

@app.post("/graph/create")
async def create_graph(payload: GraphCreateRequest):
    """
    Create a new custom graph definition.
    Note: For this simple demo, it maps string names to the pre-defined tools in tool_registry.
    """
    graph_id = str(uuid.uuid4())
    new_graph = WorkflowGraph()
    
    # 1. Add Nodes
    for node_name in payload.nodes:
        if node_name in tool_registry:
            new_graph.add_node(node_name, tool_registry[node_name])
        else:
            # Fallback or error - simplistic handling for assignment
            pass

    # 2. Add Edges
    for start, end in payload.edges.items():
        new_graph.add_edge(start, end)
        
    # Set first node as entry for simplicity
    if payload.nodes:
        new_graph.set_entry_point(payload.nodes[0])

    graphs_db[graph_id] = new_graph
    return {"graph_id": graph_id, "message": "Graph created successfully"}

@app.post("/graph/run")
async def run_workflow(payload: RunRequest):
    """Input: graph_id + initial state. Output: final state + execution + log."""
    if payload.graph_id not in graphs_db:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    graph = graphs_db[payload.graph_id]
    run_id = str(uuid.uuid4())
    
    # Initialize run status
    runs_db[run_id] = {"status": "running", "state": payload.initial_state}
    
    # Execute (Blocking for simplicity, though async is preferred for real apps)
    final_state, logs = await graph.run(payload.initial_state)
    
    runs_db[run_id] = {
        "status": "completed",
        "final_state": final_state,
        "logs": logs
    }
    
    return {"run_id": run_id, "final_state": final_state, "logs": logs}

@app.get("/graph/state/{run_id}")
async def get_run_state(run_id: str):
    """Return the current state of an ongoing workflo."""
    if run_id not in runs_db:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return runs_db[run_id]

# Mount frontend at root. Placed at the end to avoid shadowing API routes.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)