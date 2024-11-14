from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
app = Flask(__name__)
CORS(app) 
df_sredondeo =pd.read_csv("earthquake_1995-2023.csv")
df = df_sredondeo.round(1)
df['intensidad'] = np.where(df['magnitude'] <= 3.5, 'leve',
                           np.where(df['magnitude'] <= 6.5, 'moderado', 'fuerte'))
def mapear_intensidad(valor):
    if valor == 'moderado':
        return 1
    elif valor == 'fuerte':
         return 0
df['intensidad'] = df['intensidad'].apply(mapear_intensidad)
X = df[['magnitude', 'sig']]
y = df['intensidad']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train) 
# with open("modelo_terremotos.pkl", "wb") as file:
#     pickle.dump(model, file)

@app.route('/')
def home():
    return "Bienvenido a la API de predicción de terremotos"
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = [
        data['magnitude'] ,  
        data['sig']         
]
        prediction = model.predict([features])
        # Se convierte el  resultado a un tipo de Python serializable (por ejemplo, lista de enteros)
        prediction = [int(pred) for pred in prediction]  # Convierte int64 a int
        return jsonify({'La intensidad del Terremoto es :': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
