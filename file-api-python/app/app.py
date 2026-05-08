from flask import Flask, request, jsonify
import os

app = Flask(__name__)

upload_folders = "uploads"

os.makedirs(upload_folders,exist_ok=True)

@app.route("/")
def home():
    return {
        "message": "Python File Upload API Running"   
    }

@app.route("/upload",methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({
            "Eror": "No file provided"
        }), 400
    
    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "Error": "Empty filename"
        }), 400
    

    filepath = os.path.join(upload_folders,file.filename)

    file.save(filepath)

    return jsonify({
        "message": "File uploaded successfully",
        "filename": file.filename
    })
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)