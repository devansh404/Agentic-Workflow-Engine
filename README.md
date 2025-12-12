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

<img width="959" height="473" alt="Screenshot 2025-12-12 135710" src="https://github.com/user-attachments/assets/3280734e-3ddd-4f35-8b59-365052def6c2" />

<img width="959" height="475" alt="Screenshot 2025-12-12 135805" src="https://github.com/user-attachments/assets/e4f4ccb7-96ec-4567-b0f2-23bb97524a6a" />

<img width="959" height="475" alt="Screenshot 2025-12-12 135829" src="https://github.com/user-attachments/assets/4ac0b467-23f8-464c-87aa-3958793cffc0" />

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
```
* View frontend on <https://localhost:8000> in the browser.
* Click on `Run Workflow` Button to execute `run_workflow` function of the backend API and fetch response from `/graph/run`
