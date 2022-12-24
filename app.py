from flask import Flask,render_template,url_for,request,jsonify
import numpy as np
import joblib
import logging
import warnings
warnings.filterwarnings('ignore')
formt = "%(lineno)d--%(name)s--%(asctime)s--%(levelname)s--%(message)s"
logging.basicConfig(filename='applog.log',level=logging.INFO , format=formt)
# load the model
minmax_scaler = joblib.load('models\preprocess_Model\minmax_scaler.scl')
model = joblib.load('models\ML_models\Decision_Tree96.lb')
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
    logging.info('successfully render the homepage')

@app.route('/predict')
def predict():
    return render_template('home.html')
    logging.info('successfully render the prediction form')

@app.route('/result' , methods=['POST'])
def result():
    if request.method == 'POST':
        logging.info('requesting the input')
        age = float(request.form["age"])
        sex = int(request.form["sex"])
        tsh = float(request.form["TSH"])
        TSH_measured = int(request.form["TSH_measured"])
        pregnant = int(request.form["pregnant"])
        TT4_measured = int(request.form["TT4_measured"])
        T4U_measured = int(request.form["T4U_measured"])
        fti = float(request.form["FTI"])
        fti_measured = int(request.form["FTI_measured"])
        I131_treatment = int(request.form["I131"])
        psych = int(request.form["psych"])
        on_thyroxine = int(request.form["thyroxine"])
        sick = int(request.form["sick"])
        logging.info('input inserted successfully')
        # scaled the features
        scaled = minmax_scaler.transform(np.array([[age,tsh,0,0,0,fti]]))
        age = scaled[0][0]
        tsh = scaled[0][1]
        fti = scaled[0][-1]
        #prepare the input for the prediction
        data = [[age,sex,tsh,TSH_measured,pregnant,
            TT4_measured,T4U_measured,
            fti,fti_measured,I131_treatment,psych,on_thyroxine,sick]]
        logging.info('successfully scaled the inputs')
        # do the prediction
        data = np.array(data)
        prediction = model.predict(data)
        data = prediction[0]
        # prediction encoding
        if  data ==2:
            data = "Negative"
        elif data == 1:
            data = 'Hypothyroidism'
        else:
            data ="Hyperthyroidism"
        
        try:
            logging.info('rendering the prediction')
            return render_template('prediction.html' ,pred = data )
            logging.info('successfully render the prediction')
        except Exception as e:
            logging.error(e)
            logging.info('error occured in during prediction rendering')

if __name__ =="__main__":
    app.run(debug=True)