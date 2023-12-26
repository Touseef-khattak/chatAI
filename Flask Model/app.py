# from flask import Flask, request, jsonify
# from Model import chat_bot_instance

# app = Flask(__name__)

# @app.route('/startChat', methods=['POST'])
# def startChat():
#     print(request.form)
#     user_input = request.form['user_input']
#     response = chat_bot_instance.start_chat(user_input)
#     return jsonify({'response': response})
    
    
# if __name__ == '__main__':
#     app.run(debug=True, port=9090)


from flask import Flask, request, jsonify
from Model import chat_bot_instance

app = Flask(__name__)

@app.route('/startChat', methods=['POST'])
def startChat():
    print(request.form)
    user_input = request.form.get('user_input')  # Use get() to avoid KeyError
    response = chat_bot_instance.start_chat(user_input)
    return jsonify({'response': response})
    
if __name__ == '__main__':
    app.run(debug=True, port=9090)
