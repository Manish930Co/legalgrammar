    import React from 'react';


    const renderHighlightedText = (text, matches) => {
    if (!matches.length) {
        return <span>{text}</span>;
    }

    const segments = [];
    let lastIndex = 0;
    const sortedMatches = [...matches].sort((a, b) => a.offset - b.offset);

    sortedMatches.forEach(match => {

        if (match.offset > lastIndex) {
        segments.push(text.slice(lastIndex, match.offset));
        }


        const errorClass =
        match.issueType === 'misspelling'
            ? 'spell'
            : match.category?.toLowerCase().includes('grammar')
            ? 'bad'
            : 'warn';

        const highlightedText = text.substr(match.offset, match.length);
        const replacement = match.replacements?.[0]?.value || 'No suggestion';
        segments.push(
        <mark
            key={`${match.offset}-${match.length}`}
            className={errorClass}
            title={`${match.message} → ${replacement}`}
        >
            {highlightedText}
        </mark>
        );
        lastIndex = match.offset + match.length;
    });


    if (lastIndex < text.length) {
        segments.push(text.slice(lastIndex));
    }

    return segments.map((segment, index) => (
        <React.Fragment key={index}>{segment}</React.Fragment>
    ));
    };

    export default function Editor({ text, onChange, matches }) {
    return (
        <div className="editor-area">
        <div className="highlighted">{renderHighlightedText(text, matches)}</div>
        <textarea
            className="editor"
            value={text}
            onChange={e => onChange(e.target.value)}
            placeholder="Type like you text your bestie. We’ll fix the chaos ✨"
            spellCheck="false"
        />
        </div>
    );
    }
