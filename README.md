# Agentic-Workflow-Engine

This repository contains a lightweight, pure Python backend implementation of a workflow/graph engine, developed for the AI Engineering Internship assignment. It allows for defining nodes, connecting them via edges, maintaining shared state, and executing workflows via FastAPI.

## 🏗️ Project Components

The project follows a monolithic structure with a React-based frontend served by a FastAPI backend.

### 1. Backend (`main.py`)
The core of the application, serving multiple roles:
*   **Workflow Engine**: Implements a graph-based engine (`WorkflowGraph`) that manages nodes, state transitions, and conditional edges (loops/branching).
*   **Summarization Logic**: Defines the specific nodes for the demo use-case:
    *   `split_text`: Breaks input text into manageable chunks.
    *   `generate_summaries`: Creates mini-summaries for chunks.
    *   `merge_summaries`: Combines mini-summaries.
    *   `refine_summary`: Iteratively polishes the summary (looping logic).
*   **API Server**: A FastAPI application that exposes endpoints to creates graphs (`/graph/create`) and runs workflows (`/graph/run`).

### 2. Frontend (`frontend/`)
A modern, reactive web interface located in the `frontend` directory:
*   **`index.html`**: The entry point, which loads React, ReactDOM, and Babel from CDNs for a build-free developer experience.
*   **`script.jsx`**: A React component (`App`) containing the UI logic. It handles user input, communicates with the backend API, and displays real-time execution logs and results.
*   **`style.css`**: Contains the styling for a clean, responsive user interface.

## 🚀 How to Run

### Prerequisites
* Python 3.8+
* `fastapi`
* `uvicorn`

### Installation
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install fastapi uvicorn
    ```

### Execution
Run the application using the included runner or Uvicorn directly:

```bash
# Run via Python script
python main.py

# OR via Uvicorn directly
uvicorn main:app --reload