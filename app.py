from flask import Flask, request, jsonify
from TA_Model import chat_bot_instance
import pymysql
import gzip

app = Flask('master model')

@app.route('/startChat', methods=['POST'])
def startChat():
    user_input = request.form['user_input']
    response = chat_bot_instance.start_chat(user_input)
    return jsonify({'response': response})
    
    
if __name__ == '__main__':
    app.run(debug=True)