    import React, { useState, useCallback, useMemo } from 'react';

    const API_URL = 'http://localhost:8000';

    const TASKS = [
    { value: 'correct', label: '1️⃣ Grammar & Legal Correction' },
    { value: 'draft_affidavit', label: '2️⃣ Affidavit Generator' },
    { value: 'legal_notice', label: '3️⃣ Legal Notice Creator' },
    { value: 'complaint_letter', label: '4️⃣ Complaint Letter Generator' },
    { value: 'contract_maker', label: '5️⃣ Agreement / Contract Maker' },
    { value: 'document_summarizer', label: '6️⃣ Document Summarizer' },
    { value: 'term_explainer', label: '7️⃣ Legal Term Explainer' },
    { value: 'format_checker', label: '8️⃣ Legal Format Checker' },
    { value: 'tone_improver', label: '9️⃣ Formal Rewriter / Tone Improver' },
    { value: 'contract_review', label: '🔟 Contract Review' },
    ];

    export default function App() {
    const [inputText, setInputText] = useState('');
    const [processedText, setProcessedText] = useState('');
    const [mode, setMode] = useState('correct');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const currentTask = useMemo(() => TASKS.find(t => t.value === mode), [mode]);

    const getPlaceholderText = () => {
        switch (mode) {
        case 'correct': return 'Paste a block of legal text here to check for grammatical errors, spelling mistakes, and stylistic improvements...';
        case 'draft_affidavit': return 'Provide the key details for the affidavit. For example: "My name is John Doe, son of Richard Doe, resident of 123 Law Street. I need to declare that I witnessed the signing of the will on January 1st, 2025..."';
        case 'legal_notice': return 'Describe the situation requiring a legal notice. Include parties involved, the issue, and the required action...';
        case 'document_summarizer': return 'Paste the full text of a long legal document (e.g., a judgment or article) to receive a concise summary...';
        case 'term_explainer': return 'Enter a single legal term or phrase (e.g., "res judicata", "force majeure") to get a clear explanation...';
        case 'contract_review': return 'Paste the full text of a contract clause or agreement. The AI will review it for risks, ambiguities, and non-standard terms...';
        default: return 'Enter your text or instructions here...';
        }
    };

    const handleProcessText = useCallback(async () => {
        if (!inputText.trim()) return;
        setLoading(true);
        setError('');
        setProcessedText('');
        try {
        const response = await fetch(`${API_URL}/process`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputText, mode }),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'An error occurred during processing.');
        }
        setProcessedText(data.processed_text);
        } catch (err) {
        setError(err.message);
        } finally {
        setLoading(false);
        }
    }, [inputText, mode]);

    const handleDownloadPdf = async () => {
        if (!processedText) return;
        const title = currentTask?.label.replace(/[^a-zA-Z0-9]+/g, '_') || 'Legal_Document';
        try {
        const response = await fetch(`${API_URL}/generate-pdf`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: processedText, title: title }),
        });
        if (!response.ok) throw new Error('PDF generation failed.');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${title}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
        window.URL.revokeObjectURL(url);
        } catch (err) {
        setError(`PDF Download Error: ${err.message}`);
        }
    };

    return (
        <div className="dashboard-layout">
        <aside className="sidebar">
            <div className="sidebar-header">LA.</div>
            <nav>
            <ul className="task-list">
                {TASKS.map((task) => (
                <li
                    key={task.value}
                    className={`task-list-item ${mode === task.value ? 'active' : ''}`}
                    onClick={() => setMode(task.value)}
                >
                    
                    {task.label}
                </li>
                ))}
            </ul>
            </nav>
        </aside>

        <main className="main-content">
            <header className="workspace-header">
            
            <h1 className="workspace-title">{currentTask?.label}</h1>
            <button className="action-btn" onClick={handleProcessText} disabled={loading || !inputText.trim()}>
                {loading ? 'Processing...' : 'Process Text'}
            </button>
            </header>

            <section className="workspace-panels">
            <div className="panel">
                <div className="panel-header">Input Details</div>
                <textarea
                className="text-area"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={getPlaceholderText()}
                />
            </div>
            <div className="panel">
                <div className="panel-header">Generated Output</div>
                <div className="output-container">
                <div className="output-area">
                    {
                        error && <div style={{ color: '#e63946', marginBottom: '15px' }}><strong>Error:</strong> {error}</div>
                    }
                    {
                        loading ? 'Generating response...' : (processedText || '')
                    }
                </div>
                {processedText && (
                    <div className="output-footer">
                    <button className="download-btn" onClick={handleDownloadPdf}>
                        Download PDF
                    </button>
                    </div>
                )}
                </div>
            </div>
            </section>
        </main>
        </div>
    );
    }
