import { Bot, User } from 'lucide-react';
import type { Message, PhoneDetails, ComparisonData } from '../types/api.types';
import { PhoneDetailCard } from './PhoneDetailCard';
import { PhoneComparison } from './PhoneComparison';
import { PhoneList } from './PhoneList';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  const renderContextData = () => {
    if (!message.context_data) return null;

    switch (message.intent) {
      case 'details':
        return (
          <div className="mt-3">
            <PhoneDetailCard phone={message.context_data as PhoneDetails} />
          </div>
        );

      case 'compare':
        return (
          <div className="mt-3">
            <PhoneComparison comparison={message.context_data as ComparisonData} />
          </div>
        );

      case 'search_recommendation':
        const phones = message.context_data as PhoneDetails[];
        return (
          <div className="mt-3">
            <PhoneList phones={phones} />
          </div>
        );

      default:
        return null;
    }
  };

  if (isUser) {
    return (
      <div className="flex items-start gap-3 justify-end">
        <div className="bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 max-w-[80%] shadow-md">
          <p className="text-sm leading-relaxed">{message.content}</p>
        </div>
        <div className="bg-blue-100 rounded-full p-2 flex-shrink-0">
          <User className="w-5 h-5 text-blue-600" />
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-3">
      <div className="bg-gradient-to-br from-cyan-500 to-blue-500 rounded-full p-2 flex-shrink-0">
        <Bot className="w-5 h-5 text-white" />
      </div>
      <div className="flex-1 max-w-[85%]">
        <div className="bg-gray-100 rounded-2xl rounded-tl-sm px-4 py-3 shadow-md">
          <p className="text-sm leading-relaxed text-gray-900 whitespace-pre-wrap">
            <ReactMarkdown>
              {message.content}
            </ReactMarkdown>
          </p>
        </div>
        {renderContextData()}
      </div>
    </div>
  );
}
