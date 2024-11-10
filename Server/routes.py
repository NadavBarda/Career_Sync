from flask import jsonify, request, Blueprint,session
from controller.chatbot_controller import handle_chat_request
from algorithm.chatbot import Chatbot
from token_utils import generate_token
from utils import insert_new_user, login_user
from flask_cors import CORS
app = Blueprint('routes', __name__)
CORS(app)


@app.route('/signup', methods=['POST'])
def handle_post():
    data = request.json
    newUser = insert_new_user(data)
    if newUser:
        return jsonify(data), 200
    else:
        return 'Failed to add user to the database', 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        
        user = login_user(username, password)
        if user:
            
            token = generate_token(username)
            
            if token:
                session['username'] = username
                session['logged_in'] = True
                return jsonify({
                    "message": "Login successful!",
                    "token": token,
                    "user": user
                }), 200
            else:
                return jsonify({"message": "Failed to generate token"}), 500
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception:
        return jsonify({"message": "Internal Server Error"}), 500

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({"message": "Logged out successfully"}), 200


chatbot = Chatbot()


'''
need to add token warper need to check fisrt the client side how he send data
'''

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        bot_response = handle_chat_request(data,chatbot)
        
        if bot_response is None:
            return jsonify({"message": "Internal Server Error"}), 500
        
        return jsonify({"response": bot_response}), 200
    except Exception as e:
        print(f"Error in /chat route: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

