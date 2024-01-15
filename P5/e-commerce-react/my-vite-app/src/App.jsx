import React, { useEffect,useState } from 'react';
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
//import './App.css'
//import React from 'react';
import Navegacion from './componentes/Navegacion';
import Resultados from './componentes/Resultados';

function App() {
  let [productos, setProductos] = useState([]);   // se usa elevación de estado: la variable 'producto' es actualizada por 'setProductos'
  let [categorias, setCategorias] = useState([]);

  useEffect(() => { // Para que se ejecute solo cuando se renderiza la página, se usa useEffect
  
    getCategorias();
  }, []);

  //const categorias = [
  //  { id: '1', title: 'jewelery', image: 'imagenes/71YAIFU48IL._AC_UL640_QL65_ML3_.jpg' },
  //  { id: '2', title: 'mens clothing', image: 'imagenes/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg'},
  //  { id: '3', title: 'womens clothing', image: 'imagenes/81XH0e8fefL._AC_UY879_.jpg'},
  //  { id: '4', title: 'electronics', image: 'imagenes/81QpkIctqPL._AC_SX679_.jpg'}
  //];
  
  function obtenerCSRFToken() {
    const cookieValue = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      .split('=')[1];
  
    return cookieValue;
  }

  function getCategorias(){
    let apiUrl = `http://localhost:8000/api/categorias`;
    const headers = {
      Authorization: `Bearer token_dai`,
      'X-CSRFToken': obtenerCSRFToken()
    };

    axios.get(apiUrl, {headers: headers})
    .then(response => {
      console.log('Respuesta de la API: ',response.data);
      setCategorias(response.data);
    })
    .catch(error => {
      console.error('Error al enviar o recibir la solicitud: ',error);
    })
  }

  return (
    <div>
      <Navegacion setProductos={setProductos} categorias={categorias} />
      <div style={{ marginTop: '100px' }}>
        <Resultados productos={productos} setProductos={setProductos} categorias={categorias} />
      </div>
    </div>
  );
}

//function App() {
//  let [productos, setProductos] = useState([]);

//  return (
//    <CategoriaProvider> {/* Se incluye el proveedor de contexto. Así, para las categorías solo hace una llamada a la API y tenemos el valor */}
//      <div>
//        <Navegacion setProductos={setProductos} />
//        <div style={{ marginTop: '100px' }}>
//          <Resultados productos={productos} setProductos={setProductos} />
//        </div>
//      </div>
//    </CategoriaProvider>
//  );
//}

export default App;
