import React, { useState } from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { Rating } from 'primereact/rating';
import 'primereact/resources/themes/saga-blue/theme.css'; // Tema
import 'primereact/resources/primereact.min.css'; // CSS
import 'primeicons/primeicons.css'; // Iconos


function Resultados({ productos, setProductos, categorias}) {

  if (productos.length > 0) {
    // Se renderiza la búsqueda de productos
    return (
      <div className="container" style={{ marginLeft: '200px', marginTop: '50px' }}>
        <Container className="text-center">
          <Row className="g-4">
            {productos.map(producto => (
              <Producto key={producto.id} producto={producto} />
            ))}
          </Row>
        </Container>
      </div>
    );
  } else {
    // Se renderiza la página inicial (muestra categorías)
    return (
      <div className="container" style={{ marginLeft: '200px', marginTop: '50px' }}>
        <Container className="text-center">
          <Row className="g-4">
            {categorias.map(categoria => (
              <CategoriaPrincipio key={categoria.id} produ={categoria} setProductos={setProductos} />
            ))}
          </Row>
        </Container>
      </div>
    );
  }
}


function CategoriaPrincipio({ produ, setProductos }) {
    function obtenerCSRFToken() {
      const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
      
      return cookieValue;
    }

    function handleCategorySearch(categ){
      console.log('Se buscará categ: '+categ)
      if (categ=="mens clothing"){
        categ = "men's clothing";
      }
      if(categ=="womens clothing"){
        categ = "women's clothing";
      }
      let apiUrl = `http://localhost:8000/api/productosCategoria?categoria=${categ}`;
      // Necesitamos autenticarnos
      const headers = {
          Authorization: `Bearer token_dai`,
          'X-CSRFToken': obtenerCSRFToken()
      };
    
      axios.get(apiUrl, { headers: headers })
      .then(response => {
          setProductos(response.data);
            
      })
      .catch(error => {
          console.error('Error al enviar o recibir la solicitud:', error);
      });
    }
    return (
        <Col xs={12} md={6} lg={3} className="mb-4">
            <Card className="w-100" style={{ height: "auto" }}>
                <div style={{ height: "200px", overflow: "hidden" }}>
                    <ImagenProducto imagen={produ.image} nombre={produ.category} />
                </div>
                <Card.Body>
                    <Card.Title>{produ.category}</Card.Title>
                    <Button variant="primary" onClick={() => handleCategorySearch([produ.category])}>More!</Button>
                </Card.Body>
            </Card>
        </Col>
    );
}
  
function Producto({ producto }) {
  return (
    <Col xs={12} md={6} lg={4} className="mb-4">
      <Card className="w-100 h-100 d-flex flex-column">
        <div style={{ height: '200px', overflow: 'hidden' }}>
          <ImagenProducto imagen={producto.image} nombre={producto.title} />
        </div>
        <InformacionProducto 
          nombre={producto.title} 
          precio={producto.price} 
          rating={producto.rating}
          id={producto.id}
        />
      </Card>
    </Col>
  );
}
  
  
function ImagenProducto({ imagen, nombre }) {
  return (
    <div style={{ height: '200px', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <Card.Img src={imagen} alt={nombre} style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain' }} />
    </div>
  );
}

function InformacionProducto({ nombre, precio, rating, id }) {
  return (
    <Card.Body className="d-flex flex-column">
      <Card.Title>{nombre}</Card.Title>
      <Card.Text>{precio} €</Card.Text>
      <div className="mt-auto">
        <Button variant="primary">Ver más</Button>
        <Card.Text>
          <small className="text-muted">Average puntuation: {rating.rate}</small>
          <br/>
          <small className="text-muted">Votes: {rating.count}</small>
        </Card.Text>
        <Estrellas initialRating={rating.rate} id={id}/>

      </div>

    </Card.Body>
  );
}

function Estrellas({ initialRating,id }) {
  const [rating, setRating] = useState(initialRating);

  function obtenerCSRFToken() {
    const cookieValue = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      .split('=')[1];
    
    return cookieValue;
  }

  function onRatingChange(numero_estrella) {
    console.log(`Se ha clicado la estrella ${numero_estrella}`);
    let apiUrl = `http://localhost:8000/api/puntuar?id=${id}&calificacion=${numero_estrella}`;
  
    const headers = {
        Authorization: `Bearer token_dai`,
        'X-CSRFToken': obtenerCSRFToken()
    };
    console.log(headers);
  
    axios.put(apiUrl, {}, { headers: headers })
    .then(response => {
      console.log('Respuesta de la API: ', response.data);
    })
    .catch(error => {
      console.error('Error al enviar o recibir la solicitud: ', error);
    });
  }
  
  const handleChange = (e) => {
    setRating(e.value);
   // console.log({rating});
    console.log(`Ahora debería hacer la media y comunicarse con la API, pero le ha dado por decir que falla el token CSRF`);
    // Ahora envío la calificación a la API con el id requerido
    console.log(`Se ha clicado la estrella ${e.value}`);
    onRatingChange(e.value);
  };

  return (
    //<div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
    //  <Rating value={rating} onChange={handleChange} cancel={false} />
    //</div>
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <Rating value={rating} onChange={handleChange} cancel={false} />
    </div>
  );
}

export default Resultados;
