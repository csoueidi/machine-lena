from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
import os
import time
import sys
import logging
from datetime import datetime
from myparser import MyParser


app = Flask(__name__)
CORS(app)

# Variables to track execution status and filename
is_executing = False
executing_file = None
execution_message = None
myParser = MyParser()

# Debug mode variables
debug_mode = False
debug_log_file = None
debug_logger = None

def setup_debug_logging():
    """Set up debug logging to file"""
    global debug_log_file, debug_logger
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    debug_log_file = os.path.join(log_dir, f'choreography_debug_{timestamp}.log')
    
    # Create a separate logger for choreography debugging
    debug_logger = logging.getLogger('choreography_debug')
    debug_logger.setLevel(logging.DEBUG)
    debug_logger.handlers = []  # Clear any existing handlers
    
    # File handler
    file_handler = logging.FileHandler(debug_log_file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    debug_logger.addHandler(file_handler)
    
    # Console handler (optional)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    debug_logger.addHandler(console_handler)
    
    debug_logger.info("=== Choreography Debug Mode Enabled ===")
    debug_logger.info(f"Logging to: {debug_log_file}")
    return debug_log_file

def log_choreography_debug(message):
    """Log choreography debug messages"""
    if debug_mode and debug_logger:
        debug_logger.info(message)
    print(message)  # Always print to console

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/getAll', methods=['GET'])
def get_all_files():
    print("Current Directory:", os.getcwd())
    files = [f for f in os.listdir('play') if f.endswith('.chor')]
    sorted_files = sorted(files)
    
    print(f"Files found: {sorted_files}")
    return jsonify(sorted_files)

@app.route('/get/<filename>', methods=['GET'])
def get_file(filename):
    if filename.endswith('.chor'):
        file_path = os.path.join(os.getcwd(),'play', filename)
        if os.path.exists(file_path):
            print(f"Fetching file: {file_path}")
            return send_from_directory(os.path.join(os.getcwd(),'play'), filename)
    return abort(404, description="File not found")

@app.route('/')
def index():
    return send_from_directory('../ui', 'index.html')




@app.route('/new', methods=['POST'])
def create_file():
    filename = request.json.get('filename')
    content = request.json.get('content', '')
    if filename and filename.endswith('.chor'):
        file_path = os.path.join(os.getcwd(),'play', filename)
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Created file: {filename}")
        return jsonify({"success": "File created"})
    return abort(400, description="Invalid filename")



@app.route('/edit/<filename>', methods=['POST'])
def edit_file(filename):
    if filename.endswith('.chor'):
        content = request.data.decode('utf-8')
        file_path = os.path.join(os.getcwd(),'play', filename)
        with open(file_path, 'w') as file:
            file.write(content)
        log_choreography_debug(f"Edited choreography file: {filename} ({len(content)} chars)")
        return jsonify({"success": "File updated"})
    return abort(404, description="File not found")

@app.route('/execute/<filename>', methods=['POST'])
def execute_action(filename): 
    global is_executing, executing_file, execution_message, myParser
    if is_executing:
        return abort(400, description="Wait! Another file is currently executing.")
    
    file_path = os.path.join(os.getcwd(), 'play', filename)
    if file_path.endswith('.chor') and os.path.exists(file_path):
        
        log_choreography_debug(f"========== STARTING EXECUTION: {filename} ==========")
        if debug_mode:
            # Read and log the choreography content
            with open(file_path, 'r') as f:
                content = f.read()
            log_choreography_debug(f"Choreography content:\n{content}")
            log_choreography_debug("=" * 60)
        
        # Set debug logger on parser if debug mode is enabled
        if debug_mode:
            myParser.set_debug_logger(debug_logger)
        else:
            myParser.set_debug_logger(None)
        
        is_executing = True    
        execution_message = myParser.execute(file_path, filename)
        is_executing = False
        log_choreography_debug(f"========== FINISHED EXECUTION: {filename} ==========\n")

        return jsonify({"success": f"File {filename} executed"})

    return abort(404, description="File not found")

@app.route('/stop/<filename>', methods=['POST'])
def stop_action(filename): 
    global myParser, is_executing
    if not is_executing:
         return jsonify({"success": f"File {filename} is not executing"})   
   
    log_choreography_debug(f"STOPPING execution: {filename}")
    myParser.stop()
    return jsonify({"success": f"File {filename} stopped"})

@app.route('/reset', methods=['POST'])
def reset_machine():
    """Reset the machine by moving all motors to position 0 at speed 0.5"""
    global is_executing, executing_file, execution_message, myParser
    
    if is_executing:
        return abort(400, description="Wait! Another file is currently executing.")
    
    log_choreography_debug("========== STARTING RESET SEQUENCE ==========")
    
    # Create a temporary reset choreography in memory
    reset_content = """set_frps 0.5
sync {
    move(1, 0)
    move(2, 0)
    move(3, 0)
    move(4, 0)
}"""
    
    # Create temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.chor', delete=False) as temp_file:
        temp_file.write(reset_content)
        temp_file_path = temp_file.name
    
    try:
        # Set debug logger on parser if debug mode is enabled
        if debug_mode:
            myParser.set_debug_logger(debug_logger)
            log_choreography_debug(f"Reset choreography content:\n{reset_content}")
        else:
            myParser.set_debug_logger(None)
        
        is_executing = True
        execution_message = myParser.execute(temp_file_path, "reset")
        is_executing = False
        
        log_choreography_debug("========== FINISHED RESET SEQUENCE ==========\n")
        
        return jsonify({"success": "Machine reset complete"})
    finally:
        # Clean up temporary file
        import os
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.route('/check_execution_status')
def check_execution_status():
    current_line = None
    current_command = None
    execution_logs = []
    if myParser.visitor is not None:
        current_line = myParser.visitor.current_line
        current_command = myParser.visitor.current_command
        execution_logs = myParser.visitor.execution_logs.copy()
    return jsonify({
        "is_executing": is_executing, 
        "message": execution_message,
        "current_line": current_line,
        "current_command": current_command,
        "execution_logs": execution_logs
    })
   
    
@app.route('/reset_status', methods=['POST'])
def reset_status():
    global executing_file, elapsed_time, execution_message
    executing_file = None
    elapsed_time = None
    execution_message = None
    return jsonify({"success": "Status reset"})
 


@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(os.getcwd(),'play', filename)
    if file_path.endswith('.chor') and os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {filename}")
        return jsonify({"success": "File deleted"})
    return abort(404, description="File not found")

@app.route('/debug/toggle', methods=['POST'])
def toggle_debug():
    global debug_mode, debug_log_file, debug_logger
    debug_mode = not debug_mode
    
    if debug_mode:
        debug_log_file = setup_debug_logging()
        return jsonify({"debug_mode": True, "log_file": debug_log_file, "message": "Choreography debug mode enabled"})
    else:
        if debug_logger:
            debug_logger.info("=== Choreography Debug Mode Disabled ===")
            # Close handlers
            for handler in debug_logger.handlers[:]:
                handler.close()
                debug_logger.removeHandler(handler)
        return jsonify({"debug_mode": False, "log_file": debug_log_file, "message": "Choreography debug mode disabled"})

@app.route('/debug/status', methods=['GET'])
def debug_status():
    return jsonify({
        "debug_mode": debug_mode,
        "log_file": debug_log_file
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
