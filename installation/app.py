from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
import os
import time
import sys
from myparser import MyParser


app = Flask(__name__)
CORS(app)

# Variables to track execution status and filename
is_executing = False
executing_file = None
execution_message = None
myParser = MyParser()

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/getAll', methods=['GET'])
def get_all_files():
    print("Current Directory:", os.getcwd())
    files = [f for f in os.listdir('chors') if f.endswith('.chor')]
    sorted_files = sorted(files)
    
    print(sorted_files)
    return jsonify(sorted_files)

@app.route('/get/<filename>', methods=['GET'])
def get_file(filename):
    if filename.endswith('.chor'):
        file_path = os.path.join(os.getcwd(),'chors', filename)
        if os.path.exists(file_path):
            print("File path:", file_path)
            return send_from_directory(os.path.join(os.getcwd(),'chors'), filename)
    return abort(404, description="File not found")





@app.route('/new', methods=['POST'])
def create_file():
    filename = request.json.get('filename')
    content = request.json.get('content', '')
    if filename and filename.endswith('.chor'):
        file_path = os.path.join(os.getcwd(),'chors', filename)
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({"success": "File created"})
    return abort(400, description="Invalid filename")



@app.route('/edit/<filename>', methods=['POST'])
def edit_file(filename):
    if filename.endswith('.chor'):
        content = request.data.decode('utf-8')
        file_path = os.path.join(os.getcwd(),'chors', filename)
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({"success": "File updated"})
    return abort(404, description="File not found")

@app.route('/execute/<filename>', methods=['POST'])
def execute_action(filename): 
    global is_executing, executing_file, execution_message, myParser
    if is_executing:
        return abort(400, description="Wait! Another file is currently executing.")
    
    file_path = os.path.join(os.getcwd(), 'chors', filename)
    if file_path.endswith('.chor') and os.path.exists(file_path):
        
        
        is_executing = True    
        execution_message = myParser.execute(file_path, filename)
        is_executing = False

        return jsonify({"success": f"File {filename} executed"})

    return abort(404, description="File not found")

@app.route('/stop/<filename>', methods=['POST'])
def stop_action(filename): 
    global myParser, is_executing
    if not is_executing:
         return jsonify({"success": f"File {filename} is not executing"})   
   
    myParser.stop()
    return jsonify({"success": f"File {filename} stopped"})

 


@app.route('/check_execution_status')
def check_execution_status():
   return jsonify({"is_executing": is_executing, "message": execution_message})
   
    
@app.route('/reset_status', methods=['POST'])
def reset_status():
    global executing_file, elapsed_time, execution_message
    executing_file = None
    elapsed_time = None
    execution_message = None
    return jsonify({"success": "Status reset"})
 


@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(os.getcwd(),'chors', filename)
    if file_path.endswith('.chor') and os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": "File deleted"})
    return abort(404, description="File not found")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
