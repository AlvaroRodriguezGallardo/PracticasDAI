
import React, { createContext, useContext, useState, useEffect } from 'react';


// 1. Crear un contexto
const CategoriaContext = createContext();

// 2. Crear un proveedor de contexto
export const CategoriaProvider = ({ children }) => {
  const [categorias, setCategorias] = useState([]);

  useEffect(() => {
    let apiUrl = `http://localhost:8000/api/categorias`;
    const headers = {
      Authorization: `Bearer token_dai`,
      'X-CSRFToken': obtenerCSRFToken()
    };

    axios.get(apiUrl, { headers: headers })
      .then(response => {
        setCategorias(response.data);
      })
      .catch(error => {
        console.error('Error: ', error);
      });
  }, []);

  return (
    <CategoriaContext.Provider value={{ categorias }}>
      {children}
    </CategoriaContext.Provider>
  );
}

// 3. Crear un hook para usar el contexto
export const useCategorias = () => {
  const context = useContext(CategoriaContext);
  if (!context) {
    throw new Error('useCategorias debe usarse dentro de un CategoriaProvider');
  }
  return context;
}