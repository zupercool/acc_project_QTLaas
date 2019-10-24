from flask import Flask, jsonify
import subprocess
import sys
app = Flask(__name__)
@app.route('/run', methods=['GET'])
def start_deployment():
    # Should run the script
    return "Complete"
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
