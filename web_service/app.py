from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
from topsis_sarishti.topsis import run_topsis

app = Flask(__name__)

# Create upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- EMAIL CONFIG ----------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)
# ---------------------------------------------


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        file = request.files['file']
        weights = request.form['weights']
        impacts = request.form['impacts']
        email = request.form['email']

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(UPLOAD_FOLDER, "result.csv")

        file.save(input_path)

        # Run TOPSIS
        run_topsis(input_path, weights, impacts, output_path)

        # Send Email
        msg = Message(
            subject="TOPSIS Result - Sarishti",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )

        msg.body = "Please find attached your TOPSIS result."

        with app.open_resource(output_path) as fp:
            msg.attach("result.csv", "text/csv", fp.read())

        mail.send(msg)

        return f"<h2 style='color:green;'>SUCCESS: Results sent to {email}!</h2>"
    except Exception as e:
        return f"<h2 style='color:red;'>Error: {str(e)}</h2>"


if __name__ == '__main__':
    app.run(debug=True)
