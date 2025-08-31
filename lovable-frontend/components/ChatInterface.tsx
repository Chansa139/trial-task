import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '../types';
import MessageBubble from './MessageBubble';
import './ChatInterface.css';

interface ChatInterfaceProps {
  messages: ChatMessage[];
  isLoading: boolean;
  onSendMessage: (message: string) => void;
  messagesEndRef: React.RefObject<HTMLDivElement>;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  isLoading,
  onSendMessage,
  messagesEndRef
}) => {
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const getLanguageFlag = (languageCode?: string) => {
    const flags: Record<string, string> = {
      'ms': '🇲🇾',
      'en': '🇺🇸',
      'zh': '🇨🇳',
      'ta': '🇮🇳'
    };
    return flags[languageCode || ''] || '🌐';
  };

  const getIntentIcon = (intent?: string) => {
    const icons: Record<string, string> = {
      'complaint': '😠',
      'order': '📦',
      'support': '🔧',
      'billing': '💳',
      'general': '💬'
    };
    return icons[intent || ''] || '💬';
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className="message-container">
            <MessageBubble message={message} />
            {message.detectedLanguage && (
              <div className="message-metadata">
                <span className="language-indicator">
                  {getLanguageFlag(message.detectedLanguage)} {message.detectedLanguage}
                </span>
                {message.intent && (
                  <span className="intent-indicator">
                    {getIntentIcon(message.intent)} {message.intent}
                  </span>
                )}
                {message.confidence && (
                  <span className="confidence-indicator">
                    {Math.round(message.confidence * 100)}% confidence
                  </span>
                )}
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="message-container">
            <div className="message-bubble assistant loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <div className="input-container">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message in any language..."
            disabled={isLoading}
            className="chat-input"
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? '⏳' : '📤'}
          </button>
        </div>
        
        <div className="input-hints">
          <span>Try: "Saya ada masalah dengan pesanan saya" (Bahasa Malaysia)</span>
          <span>Or: "I need help with my order" (English)</span>
          <span>Or: "我的订单有问题" (Chinese)</span>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;