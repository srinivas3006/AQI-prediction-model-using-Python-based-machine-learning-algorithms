from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle

app = Flask(__name__)
model = pickle.load(open("finalized_model.pkl", "rb"))
model1 = pickle.load(open("finalized_model_regressor.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        PM2 = request.form["PM10"]
        PM10 = request.form["PM10"]
        NO = request.form["NO"]
        NO2 = request.form["NO2"]
        NOx = request.form["NOx"]
        NH3 = request.form["NH3"]
        CO = request.form["CO"]
        SO2 = request.form["SO2"]
        O3 = request.form["O3"]
        Benzene = request.form["Benzene"]
        Toluene = request.form["Toluene"]
        Xylene = request.form["Xylene"]
        prediction = model.predict([[PM2, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene]])
        output2 = model1.predict([[PM2, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene]])
        out_dict = {'Severe': 0, 'Very Poor': 1, 'Poor': 2, 'Moderate': 3, 'Satisfactory': 4, 'Good': 5}
        key_list = list(out_dict.keys())
        val_list = list(out_dict.values())
        position = val_list.index(prediction[0])
        output = key_list[position]

        return render_template('index.html', prediction_text="Predicted Air Quality Class Is : {0}".format(output),prediction_text1="Predicted Air Quality Index is : {0}".format(output2[0]))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
