from flask import Flask, render_template, request, jsonify
import sys
import os

# Add current directory to path so we can import devices and utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from devices import authorization_list
    import utils
except ImportError as e:
    print(f"Error importing modules: {e}")
    authorization_list = []

app = Flask(__name__)

def get_token(device_index):
    try:
        raw_token = authorization_list[int(device_index)]
        # utils.py adds "Bearer ", so we need to strip it if present here
        if raw_token.startswith("Bearer "):
            return raw_token.split("Bearer ")[1].strip()
        return raw_token
    except (IndexError, ValueError):
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/devices')
def list_devices():
    # Return list of indices
    return jsonify({"devices": list(range(len(authorization_list)))})

@app.route('/api/proxy/<action>', methods=['POST'])
def proxy_action(action):
    data = request.json
    device_index = data.get('device_index')
    token = get_token(device_index)
    
    if not token:
        return jsonify({"error": "Invalid device index or token"}), 400

    try:
        if action == 'query_fee':
            plate = data.get('plate')
            if not plate:
                return jsonify({"error": "Plate number required"}), 400
            result = utils.query_park_fee(token, plate)

        elif action == 'exchange':
            result = utils.exchange_office_coupon(token)

        elif action == 'points':
            # Assuming query_vip_info_office returns points/bonus info
            result = utils.query_vip_info_office(token)

        elif action == 'bonus':
             result = utils.get_cert_bonus(token)
            
        elif action == 'park_records':
            result = utils.get_park_records(token)
            
        elif action == 'coupons':
            result = utils.get_coupon_list(token)

        elif action == 'sign_in':
            result = utils.sign_shangyuewan(token)
            
        else:
            return jsonify({"error": "Unknown action"}), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
