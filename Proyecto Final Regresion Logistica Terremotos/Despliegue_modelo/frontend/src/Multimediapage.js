import React from 'react';

const MultimediaPage = () => {
  // Matriz de URLs de las imágenes
  const imageUrls = [
    'https://via.placeholder.com/100', 'https://via.placeholder.com/100', // Rellenar con más URLs
    // Añadir hasta completar 36 enlaces
  ];

  return (
    <div>
      <h1>Página de Multimedia</h1>
      <table>
        <tbody>
          {[...Array(6)].map((_, rowIndex) => (
            <tr key={rowIndex}>
              {[...Array(6)].map((_, colIndex) => (
                <td key={colIndex}>
                  <img
                    src={imageUrls[rowIndex * 6 + colIndex]}
                    alt={`Imagen ${rowIndex * 6 + colIndex + 1}`}
                    width="100"
                    height="100"
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MultimediaPage;
