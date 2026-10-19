import os
import json
import threading
import time
from flask import Flask, request, jsonify, render_template_string
import redis

app = Flask(__name__)

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
STREAM_NAME = 'orders_stream'

@app.route('/', methods=['GET'])
def frontend():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Free Cloud Store with Upstash</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="font-family: Arial, sans-serif; margin: 20px; max-width: 600px;">
        <h2>☁️ Upstash-Powered Cloud Checkout</h2>
        <p>This store writes orders to a real, serverless external message broker!</p>
        <input type="text" id="item" placeholder="Enter Product Name" style="padding:10px; width:80%; max-width:300px; margin-bottom:10px;"><br>
        <button onclick="placeOrder()" style="padding:10px 20px; background-color:#28a745; color:white; border:none; border-radius:4px; cursor:pointer;">Buy Now</button>
        <p id="status" style="font-weight:bold; color:#007bff; margin-top:15px;"></p>

        <script>
            async function placeOrder() {
                const item = document.getElementById('item').value;
                if(!item) return alert('Enter an item!');
                document.getElementById('status').innerText = 'Streaming order to Upstash...';
                const response = await fetch('/api/order', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ item: item, quantity: 1 })
                });
                const data = await response.json();
                document.getElementById('status').innerText = data.message;
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/api/order', methods=['POST'])
def place_order():
    order_data = request.json
    payload = {"order_json": json.dumps(order_data)}
    message_id = r.xadd(STREAM_NAME, payload, id='*')
    return jsonify({
        "status": "Success", 
        "message": f"Order streamed to Upstash! Message ID: {message_id}"
    }), 202

def run_stream_consumer():
    print("Upstash Redis Stream Consumer thread started...")
    last_id = '0-0'
    while True:
        try:
            response = r.xread({STREAM_NAME: last_id}, count=1, block=2000)
            if response:
                for stream, messages in response:
                    for message_id, data in messages:
                        order = json.loads(data['order_json'])
                        print(f"🔥 [UPSTASH CONSUMER] Read Msg {message_id} -> Processing: {order}")
                        last_id = message_id
        except Exception as e:
            print(f"Consumer Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=run_stream_consumer, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
