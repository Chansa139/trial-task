import React from 'react';
import { Analytics, Language, Intent } from '../types';
import './AnalyticsDashboard.css';

interface AnalyticsDashboardProps {
  analytics: Analytics;
  supportedLanguages: Language[];
  supportedIntents: Intent[];
}

const AnalyticsDashboard: React.FC<AnalyticsDashboardProps> = ({
  analytics,
  supportedLanguages,
  supportedIntents
}) => {
  const getLanguageName = (code: string) => {
    const language = supportedLanguages.find(lang => lang.code === code);
    return language ? language.native_name : code;
  };

  const getIntentName = (code: string) => {
    const intent = supportedIntents.find(int => int.code === code);
    return intent ? intent.name : code;
  };

  const getTopLanguage = () => {
    const entries = Object.entries(analytics.languagesDetected);
    if (entries.length === 0) return null;
    return entries.reduce((a, b) => a[1] > b[1] ? a : b);
  };

  const getTopIntent = () => {
    const entries = Object.entries(analytics.intentsClassified);
    if (entries.length === 0) return null;
    return entries.reduce((a, b) => a[1] > b[1] ? a : b);
  };

  const topLanguage = getTopLanguage();
  const topIntent = getTopIntent();

  return (
    <div className="analytics-dashboard">
      <h3>📊 Analytics</h3>
      
      <div className="analytics-section">
        <div className="metric-card">
          <div className="metric-value">{analytics.totalMessages}</div>
          <div className="metric-label">Total Messages</div>
        </div>
      </div>

      <div className="analytics-section">
        <h4>🌍 Languages Detected</h4>
        {Object.keys(analytics.languagesDetected).length > 0 ? (
          <div className="language-stats">
            {Object.entries(analytics.languagesDetected)
              .sort(([,a], [,b]) => b - a)
              .map(([code, count]) => (
                <div key={code} className="stat-item">
                  <span className="stat-label">{getLanguageName(code)}</span>
                  <span className="stat-value">{count}</span>
                </div>
              ))}
            {topLanguage && (
              <div className="top-stat">
                Most used: {getLanguageName(topLanguage[0])} ({topLanguage[1]})
              </div>
            )}
          </div>
        ) : (
          <div className="no-data">No language data yet</div>
        )}
      </div>

      <div className="analytics-section">
        <h4>🎯 Intent Classification</h4>
        {Object.keys(analytics.intentsClassified).length > 0 ? (
          <div className="intent-stats">
            {Object.entries(analytics.intentsClassified)
              .sort(([,a], [,b]) => b - a)
              .map(([code, count]) => (
                <div key={code} className="stat-item">
                  <span className="stat-label">{getIntentName(code)}</span>
                  <span className="stat-value">{count}</span>
                </div>
              ))}
            {topIntent && (
              <div className="top-stat">
                Most common: {getIntentName(topIntent[0])} ({topIntent[1]})
              </div>
            )}
          </div>
        ) : (
          <div className="no-data">No intent data yet</div>
        )}
      </div>

      <div className="analytics-section">
        <h4>⚡ Performance</h4>
        <div className="metric-card">
          <div className="metric-value">{analytics.averageResponseTime.toFixed(2)}s</div>
          <div className="metric-label">Avg Response Time</div>
        </div>
      </div>

      <div className="analytics-section">
        <h4>🔧 System Status</h4>
        <div className="status-indicators">
          <div className="status-item">
            <span className="status-dot online"></span>
            <span>Agent Online</span>
          </div>
          <div className="status-item">
            <span className="status-dot online"></span>
            <span>API Connected</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;