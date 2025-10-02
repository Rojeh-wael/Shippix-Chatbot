"""
Shippix AI Chatbot Model - Backend API
This creates a standalone AI model service for your chatbot
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configure Gemini API
genai.configure(api_key='AIzaSyDqm1eaO-60qXSU9eKoUN14ON266dMVtQo')

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

# Order database (in production, use a real database)
ORDER_DATABASE = {
    'SPX12345': {
        'status': 'In Transit',
        'location': 'Chicago Distribution Center',
        'estimatedDelivery': '2025-09-27',
        'carrier': 'FedEx'
    },
    'SPX67890': {
        'status': 'Delivered',
        'location': 'Customer Address',
        'deliveredDate': '2025-09-23',
        'carrier': 'UPS'
    },
    'SPX54321': {
        'status': 'Processing',
        'location': 'Warehouse',
        'estimatedDelivery': '2025-09-28',
        'carrier': 'USPS'
    }
}

# System prompt for the AI model
SYSTEM_PROMPT = """You are a helpful customer service assistant for Shippix, a shipping company.

Your role:
- Help customers with shipping inquiries, order tracking, delivery questions
- Be friendly, professional, and concise
- If you need specific order details, ask for tracking numbers (format: SPX followed by numbers)
- For complex issues, offer to connect them with human support
- Always stay focused on shipping and delivery topics
- Use emojis sparingly but appropriately

Available services:
- Standard Shipping (5-7 days): $4.99
- Express Shipping (2-3 days): $9.99
- Overnight Shipping: $19.99
- Free shipping on orders over $50
- 30-day return policy
- Support: 1-800-SHIPPIX, support@shippix.com

Keep responses under 150 words unless detailed explanation is needed.
"""

# Store conversation history (in production, use Redis or database)
conversation_history = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Request body: {
        "message": "user message",
        "session_id": "unique_session_id",
        "context": {}
    }
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Check for order tracking
        import re
        order_match = re.search(r'\b(SPX\d+)\b', user_message, re.IGNORECASE)
        if order_match:
            order_number = order_match.group(1).upper()
            order_info = ORDER_DATABASE.get(order_number)
            
            if order_info:
                response = format_order_response(order_number, order_info)
                return jsonify({
                    'response': response,
                    'intent': 'order_tracking',
                    'order_info': order_info,
                    'source': 'database'
                })
        
        # Get or create conversation history
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Build conversation context
        history = conversation_history[session_id][-6:]  # Last 6 messages
        context = "\n".join([
            f"{'Customer' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in history
        ])
        
        # Generate AI response
        full_prompt = f"""{SYSTEM_PROMPT}

Previous conversation:
{context}

Customer: {user_message}

Please provide a helpful response as a Shippix customer service representative:"""
        
        response = model.generate_content(full_prompt)
        ai_response = response.text
        
        # Update conversation history
        conversation_history[session_id].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'response': ai_response,
            'intent': 'general',
            'source': 'ai',
            'session_id': session_id
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/track', methods=['POST'])
def track_order():
    """
    Order tracking endpoint
    Request body: {"order_number": "SPX12345"}
    """
    try:
        data = request.json
        order_number = data.get('order_number', '').upper()
        
        if not order_number:
            return jsonify({'error': 'Order number is required'}), 400
        
        order_info = ORDER_DATABASE.get(order_number)
        
        if order_info:
            response = format_order_response(order_number, order_info)
            return jsonify({
                'success': True,
                'response': response,
                'order_info': order_info
            })
        else:
            return jsonify({
                'success': False,
                'response': f"❌ Order {order_number} not found in our system. Please check the order number and try again."
            }), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'gemini-2.0-flash',
        'timestamp': datetime.now().isoformat()
    })

def format_order_response(order_number, order_info):
    """Format order tracking response"""
    response = f"📦 Order {order_number} Status:\n\n"
    response += f"🚛 Status: {order_info['status']}\n"
    response += f"📍 Location: {order_info['location']}\n"
    response += f"🚚 Carrier: {order_info['carrier']}\n"
    
    if 'estimatedDelivery' in order_info:
        response += f"📅 Estimated Delivery: {order_info['estimatedDelivery']}"
    elif 'deliveredDate' in order_info:
        response += f"✅ Delivered: {order_info['deliveredDate']}"
    
    return response

if __name__ == '__main__':
    print("🚀 Starting Shippix AI Model Backend...")
    print("📍 API will be available at: http://localhost:5000")
    print("📝 Endpoints:")
    print("   POST /api/chat - Main chat endpoint")
    print("   POST /api/track - Order tracking")
    print("   GET /api/health - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)