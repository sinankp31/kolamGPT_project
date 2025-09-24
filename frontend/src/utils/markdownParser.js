// Simple markdown parser for basic formatting

export const parseMarkdown = (text) => {
  if (!text) return '';

  let html = text
    // Bold text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Italic text
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // Code blocks
    .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Headers
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    // Lists
    .replace(/^\* (.*$)/gm, '<li>$1</li>')
    .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
    // Line breaks
    .replace(/\n/g, '<br>');

  // Wrap consecutive list items
  html = html.replace(/(<li>.*<\/li>\s*)+/g, '<ul>$&</ul>');

  return html;
};