import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [terremotoData, setTerremotoData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const features = {
      magnitude: 2, 
      sig: 500,
      
    };
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/predict", features);
      setTerremotoData(response.data);
    } catch (err) {
      setError("Error al obtener la predicción");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="App">
     <center> <h1>Regresion Logistica para Clasificacion </h1></center>
     <center> <h1>Intensidad terremotos</h1></center>
      
      <form onSubmit={handleSubmit}>
      <center> <button type="submit" disabled={loading}>
          {loading ? "Enviando..." : "Predecir"}
        </button></center>
      </form>
        <center>{loading && <p>Prediciendo intensidad...</p>}</center>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {terremotoData && (
        <div>
          <center><h2>Predicción</h2>
          <h4>2 "leve"</h4>
          <h4>1 "Moderado"</h4>
          <h4>0 "Fuerte"</h4>
          
          <pre>{JSON.stringify(terremotoData, null, 2)}</pre> </center>
        </div>
      )}
    </div>
  );
}
export default App;
