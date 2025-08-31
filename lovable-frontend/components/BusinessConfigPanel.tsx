import React, { useState } from 'react';
import { BusinessConfig } from '../types';
import './BusinessConfigPanel.css';

interface BusinessConfigPanelProps {
  onConfigure: (config: BusinessConfig) => void;
  onClose: () => void;
  currentConfig?: BusinessConfig | null;
}

const BusinessConfigPanel: React.FC<BusinessConfigPanelProps> = ({
  onConfigure,
  onClose,
  currentConfig
}) => {
  const [config, setConfig] = useState<BusinessConfig>({
    business_name: currentConfig?.business_name || '',
    primary_language: currentConfig?.primary_language || 'Bahasa Malaysia',
    supported_languages: currentConfig?.supported_languages || ['Bahasa Malaysia', 'English'],
    knowledge_base_url: currentConfig?.knowledge_base_url || '',
    api_key: currentConfig?.api_key || ''
  });

  const [selectedLanguages, setSelectedLanguages] = useState<string[]>(config.supported_languages);

  const availableLanguages = [
    'Bahasa Malaysia',
    'English',
    'Chinese',
    'Tamil',
    'Malay',
    'Mandarin',
    'Cantonese'
  ];

  const handleLanguageToggle = (language: string) => {
    setSelectedLanguages(prev => 
      prev.includes(language)
        ? prev.filter(lang => lang !== language)
        : [...prev, language]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const updatedConfig = {
      ...config,
      supported_languages: selectedLanguages
    };
    onConfigure(updatedConfig);
  };

  return (
    <div className="config-overlay">
      <div className="config-panel">
        <div className="config-header">
          <h2>⚙️ Business Configuration</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        <form onSubmit={handleSubmit} className="config-form">
          <div className="form-group">
            <label htmlFor="business_name">Business Name</label>
            <input
              type="text"
              id="business_name"
              value={config.business_name}
              onChange={(e) => setConfig(prev => ({ ...prev, business_name: e.target.value }))}
              placeholder="Enter your business name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="primary_language">Primary Language</label>
            <select
              id="primary_language"
              value={config.primary_language}
              onChange={(e) => setConfig(prev => ({ ...prev, primary_language: e.target.value }))}
            >
              {availableLanguages.map(lang => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Supported Languages</label>
            <div className="language-checkboxes">
              {availableLanguages.map(language => (
                <label key={language} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={selectedLanguages.includes(language)}
                    onChange={() => handleLanguageToggle(language)}
                  />
                  <span className="checkmark"></span>
                  {language}
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="knowledge_base_url">Knowledge Base URL (Optional)</label>
            <input
              type="url"
              id="knowledge_base_url"
              value={config.knowledge_base_url}
              onChange={(e) => setConfig(prev => ({ ...prev, knowledge_base_url: e.target.value }))}
              placeholder="https://api.example.com/knowledge"
            />
          </div>

          <div className="form-group">
            <label htmlFor="api_key">API Key (Optional)</label>
            <input
              type="password"
              id="api_key"
              value={config.api_key}
              onChange={(e) => setConfig(prev => ({ ...prev, api_key: e.target.value }))}
              placeholder="Your API key"
            />
          </div>

          <div className="form-actions">
            <button type="button" onClick={onClose} className="cancel-button">
              Cancel
            </button>
            <button type="submit" className="save-button">
              Save Configuration
            </button>
          </div>
        </form>

        <div className="config-preview">
          <h4>Configuration Preview</h4>
          <div className="preview-content">
            <p><strong>Business:</strong> {config.business_name || 'Not set'}</p>
            <p><strong>Primary Language:</strong> {config.primary_language}</p>
            <p><strong>Supported Languages:</strong> {selectedLanguages.join(', ') || 'None selected'}</p>
            <p><strong>Knowledge Base:</strong> {config.knowledge_base_url || 'Not configured'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BusinessConfigPanel;