import React from 'react';
import { Language } from '../types';
import './LanguageSelector.css';

interface LanguageSelectorProps {
  languages: Language[];
  currentLanguage: string;
  onLanguageChange: (languageCode: string) => void;
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  languages,
  currentLanguage,
  onLanguageChange
}) => {
  const getLanguageFlag = (code: string) => {
    const flags: Record<string, string> = {
      'ms': '🇲🇾',
      'en': '🇺🇸',
      'zh': '🇨🇳',
      'ta': '🇮🇳'
    };
    return flags[code] || '🌐';
  };

  return (
    <div className="language-selector">
      <select
        value={currentLanguage}
        onChange={(e) => onLanguageChange(e.target.value)}
        className="language-select"
      >
        {languages.map(language => (
          <option key={language.code} value={language.code}>
            {getLanguageFlag(language.code)} {language.native_name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;