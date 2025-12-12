const { useState } = React;

function App() {

    const [text, setText] = useState("");
    const [maxLength, setMaxLength] = useState(0);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const runWorkflow = async () => {
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await fetch('/graph/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    graph_id: "default_summary_graph",
                    initial_state: {
                        text: text,
                        max_length: parseInt(maxLength)
                    }
                })
            });

            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <h1>Mini Agent Workflow Engine</h1>
            <p>Enter text below to process it through the summarization refinement workflow.</p>

            <div className="input-group">
                <label htmlFor="inputText">Input Text</label>
                <textarea
                    id="inputText"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste your text here to regenerate a summary..."
                />
            </div>

            <div className="input-group">
                <label htmlFor="maxLength">Max Summary Length (words)</label>
                <input
                    type="number"
                    id="maxLength"
                    value={maxLength}
                    onChange={(e) => setMaxLength(e.target.value)}
                    min="1"
                />
            </div>

            <button onClick={runWorkflow} disabled={loading} id="runBtn">
                {loading ? 'Running...' : 'Run Workflow'}
            </button>

            <div id="output" style={{ display: (loading || result || error) ? 'block' : 'none' }}>
                {loading && <div style={{ textAlign: 'center', color: '#666' }}>Processing...</div>}

                {error && (
                    <div style={{ color: 'red', padding: '10px', background: '#fff5f5', borderRadius: '4px' }}>
                        Error: {error}
                    </div>
                )}

                {result && (
                    <div className="result-box">
                        <div className="section-title">Final Summary</div>
                        <div style={{ fontSize: '1.1em', lineHeight: '1.6', color: '#1a202c', padding: '10px', background: '#fff', border: '1px solid #e2e8f0', borderRadius: '4px' }}>
                            {result.final_state.current_summary || "No summary generated"}
                        </div>

                        <div className="section-title">Final State Details</div>
                        <pre>{JSON.stringify(result.final_state, null, 2)}</pre>

                        <div className="section-title">Execution Log</div>
                        <div style={{ maxHeight: '200px', overflowY: 'auto', background: 'white', padding: '10px', border: '1px solid #e2e8f0', borderRadius: '4px' }}>
                            {result.logs.map((log, index) => (
                                <div key={index} className="log-entry">› {log}</div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
