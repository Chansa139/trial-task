import React, { useState, useEffect, useRef } from 'react';
import { ChatMessage, ChatRequest, BusinessConfig, Language, Intent } from './types';
import { sendMessage, getSupportedLanguages, getSupportedIntents, configureBusiness } from './api';
import ChatInterface from './components/ChatInterface';
import BusinessConfigPanel from './components/BusinessConfigPanel';
import LanguageSelector from './components/LanguageSelector';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import './App.css';

const App: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const [currentLanguage, setCurrentLanguage] = useState<string>('ms');
  const [supportedLanguages, setSupportedLanguages] = useState<Language[]>([]);
  const [supportedIntents, setSupportedIntents] = useState<Intent[]>([]);
  const [businessConfig, setBusinessConfig] = useState<BusinessConfig | null>(null);
  const [showConfig, setShowConfig] = useState(false);
  const [analytics, setAnalytics] = useState({
    totalMessages: 0,
    languagesDetected: {} as Record<string, number>,
    intentsClassified: {} as Record<string, number>,
    averageResponseTime: 0
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    initializeApp();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const initializeApp = async () => {
    try {
      const [languages, intents] = await Promise.all([
        getSupportedLanguages(),
        getSupportedIntents()
      ]);
      setSupportedLanguages(languages);
      setSupportedIntents(intents);
      
      // Add welcome message
      const welcomeMessage: ChatMessage = {
        id: `msg_${Date.now()}`,
        role: 'assistant',
        content: 'Selamat datang! Welcome! 欢迎! வரவேற்கிறோம்! How can I help you today?',
        timestamp: new Date(),
        detectedLanguage: 'ms',
        intent: 'general',
        confidence: 0.95
      };
      setMessages([welcomeMessage]);
    } catch (error) {
      console.error('Failed to initialize app:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    const userMessage: ChatMessage = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: content.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const request: ChatRequest = {
        message: content.trim(),
        session_id: sessionId,
        business_config: businessConfig
      };

      const response = await sendMessage(request);
      
      const assistantMessage: ChatMessage = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp,
        detectedLanguage: response.detected_language,
        intent: response.intent,
        confidence: response.confidence
      };

      setMessages(prev => [...prev, assistantMessage]);
      updateAnalytics(assistantMessage);
      
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: 'I apologize, but I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const updateAnalytics = (message: ChatMessage) => {
    setAnalytics(prev => ({
      totalMessages: prev.totalMessages + 1,
      languagesDetected: {
        ...prev.languagesDetected,
        [message.detectedLanguage || 'unknown']: (prev.languagesDetected[message.detectedLanguage || 'unknown'] || 0) + 1
      },
      intentsClassified: {
        ...prev.intentsClassified,
        [message.intent || 'unknown']: (prev.intentsClassified[message.intent || 'unknown'] || 0) + 1
      },
      averageResponseTime: prev.averageResponseTime // TODO: Calculate actual response time
    }));
  };

  const handleConfigureBusiness = async (config: BusinessConfig) => {
    try {
      await configureBusiness(config);
      setBusinessConfig(config);
      setShowConfig(false);
      
      // Add configuration success message
      const configMessage: ChatMessage = {
        id: `msg_${Date.now()}`,
        role: 'assistant',
        content: `Business configuration updated successfully! I'm now configured for ${config.business_name}.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, configMessage]);
    } catch (error) {
      console.error('Failed to configure business:', error);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setAnalytics({
      totalMessages: 0,
      languagesDetected: {},
      intentsClassified: {},
      averageResponseTime: 0
    });
    initializeApp();
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🇲🇾 Malaysian Customer Service Agent</h1>
          <div className="header-actions">
            <LanguageSelector
              languages={supportedLanguages}
              currentLanguage={currentLanguage}
              onLanguageChange={setCurrentLanguage}
            />
            <button 
              className="config-button"
              onClick={() => setShowConfig(!showConfig)}
            >
              ⚙️ Configure
            </button>
            <button 
              className="clear-button"
              onClick={clearChat}
            >
              🗑️ Clear
            </button>
          </div>
        </div>
      </header>

      <div className="app-content">
        <div className="main-panel">
          <ChatInterface
            messages={messages}
            isLoading={isLoading}
            onSendMessage={handleSendMessage}
            messagesEndRef={messagesEndRef}
          />
        </div>

        <div className="sidebar">
          <AnalyticsDashboard
            analytics={analytics}
            supportedLanguages={supportedLanguages}
            supportedIntents={supportedIntents}
          />
        </div>
      </div>

      {showConfig && (
        <BusinessConfigPanel
          onConfigure={handleConfigureBusiness}
          onClose={() => setShowConfig(false)}
          currentConfig={businessConfig}
        />
      )}
    </div>
  );
};

export default App;