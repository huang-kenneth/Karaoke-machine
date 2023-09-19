from flask import Flask, render_template, request
import main  # Import your Python script

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    includeVocals = request.form.get('includeVocals')  # Retrieve input from the form
    if includeVocals == "True":
        includeVocals = True
    else:
        includeVocals = False
    ytLink = request.form.get('ytLink')
    result = main.main(ytLink, includeVocals)  # Call your Python script
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)