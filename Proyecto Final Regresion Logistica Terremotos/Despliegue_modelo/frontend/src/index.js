// index.js en la carpeta src
import React from "react";
// import ReactDOM from "react-dom";
import ReactDOM from 'react-dom/client';
import App from "./App"; // Aquí importa el componente principal de la app
import './index.css';  // Si tienes un archivo de estilos

// ReactDOM.render(
//   <React.StrictMode>
//     <App /> {/* Este es tu componente principal */}
//   </React.StrictMode>,
//   document.getElementById("root") // Asegúrate de que React monte en el div con id 'root'
// );

const root = ReactDOM.createRoot(document.getElementById('root')); // Crea el root
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);