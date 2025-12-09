from flask import Flask, request, render_template
import os
import cantools

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/utility')
def utility():
    return render_template('utility.html')

@app.route('/calculate_load', methods=['POST'])
def calculate_load():
    bus_speed = float(request.form['bus_speed'])
    if 'dbcfile2' not in request.files:
        return "No file part"
    
    file = request.files['dbcfile2']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        db = cantools.database.load_file(file_path)
        total_bits = 0
        for msg in db.messages:
            frame_size = 47 + msg.length * 8
            total_bits += frame_size
        bus_load = (total_bits / bus_speed) * 100

        result = f"""
        Total messages : {len(db.messages)}
        Total bits : {total_bits}
        Estimated Load : {bus_load:.2f}%
        """
        return render_template("utility.html", result=result)

# -----------------------------
# FIXED: Must be outside routes
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
