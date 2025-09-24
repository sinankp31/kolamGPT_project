import React from 'react';
import { Bot, User } from 'lucide-react';
import { parseMarkdown } from '../../utils/markdownParser';

const ChatMessage = ({ msg }) => {
  const isBot = msg.sender === 'bot';
  const messageHtml = parseMarkdown(msg.text || '');

  return (
    <div className={`flex items-start gap-4 py-6 px-4 md:px-0 ${isBot ? '' : 'bg-white/5 dark:bg-black/5'}`}>
      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-600 dark:bg-gray-800 text-white flex-shrink-0">
        {isBot ? <Bot size={20} /> : <User size={20} />}
      </div>
      <div className="flex-1 pt-1">
        <p className="font-semibold text-gray-800 dark:text-gray-200 mb-2">{isBot ? 'KolamGPT' : 'You'}</p>
        {msg.image && <img src={msg.image} alt="Uploaded kolam" className="my-2 max-w-xs rounded-lg border border-gray-300 dark:border-gray-600" />}
        <div className="prose dark:prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: messageHtml }} />
      </div>
    </div>
  );
};

export default ChatMessage;