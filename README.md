# 🚚 Shippix AI Chatbot

An intelligent customer support chatbot powered by Google's Gemini AI, designed to handle shipping inquiries, order tracking, and customer service for Shippix shipping company.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🤖 AI-Powered Responses
- **Natural Language Understanding**: Uses Google Gemini 2.0 Flash for intelligent conversation
- **Context-Aware**: Maintains conversation history for coherent multi-turn dialogues
- **Fallback System**: Gracefully handles backend failures with local processing

### 📦 Order Management
- **Real-time Order Tracking**: Track shipments with SPX tracking numbers
- **Status Updates**: Get current location, carrier info, and delivery estimates
- **Multiple Carriers**: Supports FedEx, UPS, USPS tracking

### 💬 Customer Support Features
- Shipping cost inquiries
- Delivery time estimates
- Address change requests
- Return and refund processing
- Package damage claims
- Order cancellations

### 🎨 User Interface
- **Modern Design**: Clean, responsive chat interface
- **Quick Actions**: One-click buttons for common queries
- **Typing Indicators**: Visual feedback during AI processing
- **Status Monitoring**: Real-time backend connection status
- **Mobile-Friendly**: Fully responsive design

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (HTML/JS)     │
│   Port: Browser │
└────────┬────────┘
         │
         │ HTTP/REST API
         │
┌────────▼────────┐
│  Backend API    │
│  (Flask/Python) │
│  Port: 5000     │
└────────┬────────┘
         │
         │ API Calls
         │
┌────────▼────────┐
│  Gemini API     │
│  (Google AI)    │
└─────────────────┘
```

**Client-Server Model:**
- **Frontend**: Single-page application (HTML/CSS/JavaScript)
- **Backend**: Flask REST API server (Python)
- **AI Engine**: Google Gemini 2.0 Flash model
- **Data Storage**: In-memory (can be extended to database)

## 🔧 Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 📦 Installation

### 1. Clone or Download the Project

```bash
# If using Git
git clone https://github.com/yourusername/shippix-chatbot.git
cd shippix-chatbot

# Or download and extract the ZIP file
```

### 2. Install Python Dependencies

```bash
pip install flask flask-cors google-generativeai
```

**Or using requirements.txt:**

```bash
pip install -r requirements.txt
```

### 3. Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

## ⚙️ Configuration

### Backend Configuration

Open `shippix_ai_backend.py` and update the API key:

```python
# Line 13
genai.configure(api_key='YOUR_API_KEY_HERE')  # Replace with your actual API key
```

### Frontend Configuration

If deploying the backend to a different URL, update `index.html`:

```javascript
// Line 290 (approximately)
const aiClient = new ShippixAIClient('http://localhost:5000');

// For production, change to your deployed backend URL:
const aiClient = new ShippixAIClient('https://your-backend-url.com');
```

### Order Database (Optional)

Customize the order database in `shippix_ai_backend.py`:

```python
ORDER_DATABASE = {
    'SPX12345': {
        'status': 'In Transit',
        'location': 'Chicago Distribution Center',
        'estimatedDelivery': '2025-09-27',
        'carrier': 'FedEx'
    },
    # Add more orders here
}
```

## 🚀 Usage

### Starting the Backend Server

```bash
python shippix_ai_backend.py
```

You should see:
```
🚀 Starting Shippix AI Model Backend...
📍 API will be available at: http://localhost:5000
📝 Endpoints:
   POST /api/chat - Main chat endpoint
   POST /api/track - Order tracking
   GET /api/health - Health check
 * Running on http://0.0.0.0:5000
```

### Opening the Frontend

1. **Option 1**: Open `index.html` directly in your browser
   ```bash
   open index.html  # macOS
   start index.html  # Windows
   xdg-open index.html  # Linux
   ```

2. **Option 2**: Use a local web server (recommended)
   ```bash
   # Python
   python -m http.server 8000
   
   # Node.js
   npx http-server
   ```
   Then visit `http://localhost:8000`

### Testing the Chatbot

Try these example queries:
- "What are your shipping costs?"
- "Track order SPX12345"
- "How long does delivery take?"
- "I need to change my delivery address"
- "I want to return an item"

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Chat Endpoint
Send a message to the AI chatbot.

**POST** `/api/chat`

**Request Body:**
```json
{
  "message": "What are your shipping costs?",
  "session_id": "unique_session_id",
  "context": {}
}
```

**Response:**
```json
{
  "response": "Our shipping costs are...",
  "intent": "shipping_costs",
  "source": "ai",
  "session_id": "unique_session_id"
}
```

#### 2. Track Order
Track a specific order by number.

**POST** `/api/track`

**Request Body:**
```json
{
  "order_number": "SPX12345"
}
```

**Response:**
```json
{
  "success": true,
  "response": "📦 Order SPX12345 Status: In Transit...",
  "order_info": {
    "status": "In Transit",
    "location": "Chicago Distribution Center",
    "estimatedDelivery": "2025-09-27",
    "carrier": "FedEx"
  }
}
```

#### 3. Health Check
Check if the backend is running properly.

**GET** `/api/health`

**Response:**
```json
{
  "status": "healthy",
  "model": "gemini-2.0-flash",
  "timestamp": "2025-10-02T10:30:00.000Z"
}
```

### cURL Examples

```bash
# Chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your shipping costs?", "session_id": "test123"}'

# Track order
curl -X POST http://localhost:5000/api/track \
  -H "Content-Type: application/json" \
  -d '{"order_number": "SPX12345"}'

# Health check
curl http://localhost:5000/api/health
```

## 📁 Project Structure

```
shippix-chatbot/
│
├── index.html                 # Frontend chat interface
├── shippix_ai_backend.py     # Backend Flask API server
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── docs/                      # Additional documentation
│   ├── API.md                # Detailed API documentation
│   └── DEPLOYMENT.md         # Deployment guides
│
└── training_data/            # Optional: Fine-tuning data
    └── training_data.jsonl   # JSONL format training examples
```

## 🎨 Customization

### Changing the System Prompt

Edit the `SYSTEM_PROMPT` in `shippix_ai_backend.py`:

```python
SYSTEM_PROMPT = """You are a helpful customer service assistant for Shippix...

Your role:
- Help customers with shipping inquiries
- Be friendly and professional
...
"""
```

### Adding New Orders

Add to the `ORDER_DATABASE` dictionary:

```python
ORDER_DATABASE = {
    'SPX99999': {
        'status': 'Delivered',
        'location': 'Customer Address',
        'deliveredDate': '2025-10-01',
        'carrier': 'FedEx'
    }
}
```

### Styling the Frontend

Modify the CSS in `index.html` (between `<style>` tags):

```css
/* Change primary color */
.chat-header {
    background: linear-gradient(135deg, #YOUR_COLOR_1, #YOUR_COLOR_2);
}
```

### Using a Database

Replace the in-memory dictionary with a database:

```python
# Example with SQLite
import sqlite3

def get_order(order_number):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
    return cursor.fetchone()
```

## 🌐 Deployment

### Deploy Backend to Cloud

#### Heroku
```bash
# Create Procfile
echo "web: python shippix_ai_backend.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### Google Cloud Run
```bash
# Create Dockerfile
# Deploy
gcloud run deploy shippix-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Railway
1. Push code to GitHub
2. Connect Railway to your repository
3. Add environment variables
4. Deploy automatically

### Deploy Frontend

#### GitHub Pages
```bash
git add index.html
git commit -m "Deploy frontend"
git push origin main
```

Enable GitHub Pages in repository settings.

#### Netlify
1. Drag and drop `index.html` to Netlify
2. Or connect your Git repository
3. Update backend URL in code

### Environment Variables

For production, use environment variables:

```python
import os
API_KEY = os.environ.get('GEMINI_API_KEY')
```

Set in your hosting platform:
```bash
# Heroku
heroku config:set GEMINI_API_KEY=your_key_here

# Railway
# Set in dashboard

# Local testing
export GEMINI_API_KEY=your_key_here
```

## 🐛 Troubleshooting

### Backend Won't Start

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install flask flask-cors google-generativeai
```

### Frontend Shows "Backend Offline"

**Problem**: Frontend can't connect to backend

**Solutions**:
1. Ensure backend is running: `python shippix_ai_backend.py`
2. Check backend URL matches in frontend code
3. Check firewall/antivirus settings
4. Try accessing `http://localhost:5000/api/health` directly

### API Key Errors

**Problem**: `403 Forbidden` or `API_KEY_INVALID`

**Solutions**:
1. Regenerate API key at [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Check for extra spaces in API key
3. Ensure API key has proper permissions

### CORS Errors

**Problem**: `blocked by CORS policy`

**Solutions**:
1. Ensure `flask-cors` is installed
2. Check CORS configuration in backend
3. Run frontend on local server instead of `file://`

### Slow Responses

**Problem**: AI responses take too long

**Solutions**:
1. Reduce `maxOutputTokens` in backend
2. Limit conversation history (currently 6 messages)
3. Use a faster Gemini model
4. Check your internet connection

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Coding Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Test thoroughly before submitting

