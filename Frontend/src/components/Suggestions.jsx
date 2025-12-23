    import React from 'react';

    export default function SuggestionPanel({ correctedText, matches, onApplyCorrection }) {
    return (
        <div>
        <h3 style={{ marginTop: 0 }}>Corrections</h3>
        {matches.length > 0 && (
            <>
            <div style={{ marginBottom: 12 }}>
                <button
                className="neon-btn"
                onClick={() => onApplyCorrection(correctedText)}
                disabled={!correctedText}
                >
                Apply All Fixes
                </button>
            </div>
            <h4>Corrected Version:</h4>
            <p style={{ whiteSpace: 'pre-wrap', opacity: 0.9, background: 'rgba(0,0,0,0.2)', padding: '8px', borderRadius: '4px' }}>
                {correctedText || "No corrections available."}
            </p>
            <hr style={{ borderColor: 'rgba(255,255,255,0.1)' }} />
            </>
        )}

        <h4>Issues Found ({matches.length})</h4>
        {matches.length > 0 ? (
            matches.map((match, i) => (
            <div key={i} style={{ marginBottom: 16, borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '8px' }}>
                <div style={{ fontWeight: 600 }}>{match.shortMessage || 'Issue'}</div>
                <div style={{ opacity: 0.8, fontSize: 14, marginTop: 4 }}>{match.message}</div>
                {match.replacements?.length > 0 && (
                <div style={{ marginTop: 6, fontSize: 14 }}>
                    Suggestion: <code style={{ color: 'var(--good)', fontWeight: 'bold' }}>{match.replacements[0].value}</code>
                </div>
                )}
            </div>
            ))
        ) : (
            <p style={{ opacity: 0.7 }}>No issues found. Looks good!</p>
        )}
        </div>
    );
    }
