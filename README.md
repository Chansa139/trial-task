# 🇲🇾 Malaysian Customer Service Agent

A multilingual AI customer service agent built with your agent orchestration framework, designed specifically for the Malaysian market.

## 🚀 Features

- **Multilingual Support**: Bahasa Malaysia, English, Chinese, Tamil
- **Intelligent Agent Orchestration**: Uses your BaseMasterAgent framework
- **Real-time Analytics**: Language detection, intent classification, performance metrics
- **Business Configuration**: Customizable for different businesses
- **Modern UI**: Beautiful, responsive interface built with React

## 🏗️ Architecture

### Backend (FastAPI + Your Agent Framework)
- **BaseMasterAgent**: Core orchestration engine
- **MalaysianCustomerServiceAgent**: Specialized implementation
- **Multi-step Processing**: Language detection → Intent classification → Knowledge retrieval → Response generation
- **RESTful API**: Clean endpoints for frontend integration

### Frontend (React + TypeScript)
- **Chat Interface**: Real-time messaging with typing indicators
- **Analytics Dashboard**: Live metrics and insights
- **Business Configuration**: Easy setup for different businesses
- **Responsive Design**: Works on desktop and mobile

## 🛠️ Setup Instructions

### 1. Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the backend server
cd backend
python main.py
```

The backend will run on `http://localhost:8000`

### 2. Frontend Setup (Lovable)

1. **Copy the Lovable frontend code** from the `lovable-frontend/` directory
2. **Paste into Lovable** and let it build the React app
3. **Update API URL** in `api.ts` if needed:
   ```typescript
   const API_BASE_URL = 'http://localhost:8000'; // Your backend URL
   ```

### 3. Test the Integration

1. Start the backend server
2. Open the Lovable frontend
3. Try these test messages:
   - **Bahasa Malaysia**: "Saya ada masalah dengan pesanan saya"
   - **English**: "I need help with my order"
   - **Chinese**: "我的订单有问题"
   - **Tamil**: "எனது ஆர்டரில் பிரச்சினை உள்ளது"

## 🎯 How It Works

### Agent Flow
```
User Message → Language Detection → Intent Classification → Knowledge Retrieval → Response Generation
```

### Supported Intents
- **Complaint**: Customer complaints or issues
- **Order**: Order-related inquiries
- **Support**: Technical support requests
- **Billing**: Billing and payment inquiries
- **General**: General questions or information

### Supported Languages
- 🇲🇾 **Bahasa Malaysia** (Primary)
- 🇺🇸 **English**
- 🇨🇳 **Chinese**
- 🇮🇳 **Tamil**

## 📊 Analytics Features

- **Language Detection**: Real-time language identification
- **Intent Classification**: Automatic categorization of customer requests
- **Performance Metrics**: Response times and success rates
- **Usage Statistics**: Message counts and trends

## ⚙️ Business Configuration

Configure the agent for your business:
- **Business Name**: Customize responses
- **Primary Language**: Set default language
- **Supported Languages**: Choose available languages
- **Knowledge Base**: Connect to your data sources
- **API Keys**: Secure integrations

## 🔧 API Endpoints

- `POST /chat` - Send message to agent
- `GET /languages` - Get supported languages
- `GET /intents` - Get supported intents
- `POST /configure` - Configure business settings
- `GET /health` - Health check

## 🚀 Deployment

### Backend Deployment
```bash
# Using Docker
docker build -t malaysian-agent-backend .
docker run -p 8000:8000 malaysian-agent-backend

# Using cloud platforms
# Deploy to Railway, Render, or AWS
```

### Frontend Deployment
- Deploy Lovable app to Vercel, Netlify, or your preferred platform
- Update API URL to point to your deployed backend

## 💰 Business Model

### Pricing Tiers
- **SME Package**: RM 500-1,500/month (1,000 interactions)
- **Business Package**: RM 2,000-5,000/month (10,000 interactions)
- **Enterprise Package**: RM 10,000-50,000/month (unlimited)

### Revenue Projections
- **Month 3**: RM 7,500/month (10 customers)
- **Month 6**: RM 100,000/month (50 customers)
- **Month 12**: RM 525,000/month (150 customers)

## 🎯 Next Steps

1. **Fix Critical Issues**: Address syntax errors in the framework
2. **Add Resilience**: Implement retry logic and circuit breakers
3. **Enhance Analytics**: Add more detailed metrics
4. **Scale**: Add more agent types and integrations
5. **Market**: Start with 5-10 pilot customers

## 🤝 Contributing

This is built on your agent framework. To contribute:
1. Fix the syntax errors in `BaseMasterAgent`
2. Add proper error handling and validation
3. Implement retry logic and circuit breakers
4. Add more agent types and integrations

## 📞 Support

For questions about the agent framework or deployment:
- Check the code comments for implementation details
- Review the API documentation
- Test with the provided sample messages

---

**Ready to revolutionize customer service in Malaysia! 🇲🇾**