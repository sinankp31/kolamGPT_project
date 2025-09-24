export const parseMarkdown = (text) => {
    // Basic markdown to HTML conversion
    let html = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>')       // Italic
        .replace(/`([^`]+)`/g, '<code class="bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 px-1.5 py-0.5 rounded-md text-sm">$1</code>') // Inline code
        .replace(/^- (.*)$/gm, '<li>$1</li>');     // List items

    // Wrap consecutive list items in <ul>
    if (html.includes('<li>')) {
        html = `<ul>${html.replace(/<\/li>\n<li>/g, '</li><li>')}</ul>`
               .replace(/<\/li><ul>/g, '</li>\n<ul>') // Fix nested lists if any
               .replace(/<\/ul><li>/g, '</ul>\n<li>'); 
    }

    return html.replace(/\n/g, '<br />'); // Newlines
};