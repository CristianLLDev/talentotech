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
#en la escala de Richter, un terremoto se considera significativo a partir de una magnitud de 3.5.
df['terremoto'] = np.where(df['magnitude'] >= 3.5, 1, 0)
# Crear la columna 'intensidad' con las categorías especificadas
df['intensidad'] = np.where(df['magnitude'] <= 3.5, 'leve',
                           np.where(df['magnitude'] <= 6.5, 'moderado', 'fuerte'))


df['date_time']=pd.to_datetime(df['date_time'])
df['Year']=pd.DatetimeIndex(df["date_time"]).year
df['Month']=pd.DatetimeIndex(df["date_time"]).month
df.drop('date_time',axis=1,inplace=True)    

new_data = pd.DataFrame({
    'magnitude': np.random.uniform(0, 5, 1000),  # Magnitud entre 2.0 y 6.0
    'cdi': np.random.randint(0, 10, 1000),
    'mmi': np.random.randint(0, 10, 1000),
    'tsunami': np.random.randint(0, 1, 1000),  # 0 o 1
    'sig': np.random.randint(0, 1500, 1000),
    'nst': np.random.randint(0, 300, 1000),
    'dmin': np.random.uniform(0, 10, 1000),  # Rango ajustado
    'gap': np.random.uniform(0, 360, 1000),  # Máximo 360 grados
    'depth': np.random.uniform(0, 700, 1000),  # Profundidad razonable
    'latitude': np.random.uniform(-90, 90, 1000),
    'longitude': np.random.uniform(-180, 180, 1000),
    'Year': np.random.randint(2000, 2024, 1000),  # Años recientes
    'Month': np.random.randint(1, 13, 1000),  # Meses del 1 al 12
    'magType': np.random.randint(0, 10, 1000)  # Rango 
    })
new_data['terremoto'] = np.where(new_data['magnitude'] >= 3.5, 1, 0)
# Crear la columna 'intensidad' con las categorías especificadas
new_data['intensidad'] = np.where(new_data['magnitude'] <= 3.5, 'leve',
                           np.where(new_data['magnitude'] <= 6.5, 'moderado', 'fuerte'))

df = pd.concat([df, new_data], ignore_index=True)
def mapear_intensidad(valor):
    if valor == 'leve':
        return 2
    elif valor == 'moderado':
        return 1
    elif valor == 'fuerte':
        return 0
  
df['intensidad'] = df['intensidad'].apply(mapear_intensidad)

df.drop(['title', 'continent', 'alert','location','country','magType','net'],axis=1,inplace=True)
X = df[['magnitude', 'sig']]
y = df['intensidad']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = LogisticRegression(max_iter=1000) 
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
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
