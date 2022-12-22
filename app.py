from flask import Flask,render_template,url_for,request,jsonify
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    return render_template('home.html')

@app.route('/result' , methods=['POST'])
def result():
    if request.method == 'POST':
        return render_template('prediction.html' ,pred = str(786) )
        # return jsonify(str('welcome'))


if __name__ =="__main__":
    app.run(debug=True)