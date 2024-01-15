import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';


function BarraBusqueda({setProductos, categorias}) {
  const [searchTerm, setSearchTerm] = useState(''); //Usar elevación de estado con una variable propia para la cadena de texto

  const handleChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleCategorySearch = (cat) => {
    if (cat=="mens clothing"){
      cat = "men's clothing";
    }
    if(cat=="womens clothing"){
      cat = "women's clothing";
    }
    console.log(cat)
    // URL de la API para llamar a una función que devuelva la lista de productos por categoría
    let apiUrl = `http://localhost:8000/api/productosCategoria?categoria=${cat}`;
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

  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Buscando:', searchTerm);

    let apiUrl = `http://localhost:8000/api/productosCadena?cadena=${searchTerm}`;

    const headers = {
        Authorization: `Bearer token_dai`,
        'X-CSRFToken': obtenerCSRFToken()
    };
    console.log(headers);
    axios.get(apiUrl, {headers: headers})
    .then(response => {
      console.log('Respuesta de la API: ',response.data);
      setProductos(response.data);
    })
    .catch(error => {
      console.error('Error al enviar o recibir la solicitud: ',error);
    })
        
  };

  function obtenerCSRFToken() {
    const cookieValue = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      .split('=')[1];
  
    return cookieValue;
  }

  return (
    <Navbar expand="lg" bg="primary" data-bs-theme="light" fixed="top">
      <Container fluid>
        <Navbar.Brand href="./" style={{ color: 'white' }}>E-commerce</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll">
          <Nav className="me-auto my-2 my-lg-0" style={{ maxHeight: '100px' }} navbarScroll>
          </Nav>
          <Nav className="ms-auto" navbarScroll>
            <NavDropdown title={<span style={{ color: 'white' }}>Categories</span>} id="navbarScrollingDropdown">
              {categorias.map((categoria, index) => (
                <React.Fragment key={index}>
                  <NavDropdown.Item onClick={() => handleCategorySearch(categoria.category)}>
                    {categoria.category}
                  </NavDropdown.Item>
                  <NavDropdown.Divider />
                </React.Fragment>
              ))}
            </NavDropdown>
          </Nav>
          <Form className="d-flex" onSubmit={handleSubmit}>
            <Form.Control
              type="search"
              placeholder="Search"
              className="me-2"
              aria-label="Search"
              value={searchTerm}
              onChange={handleChange}
            />
            <Button variant="outline-success" type="submit" style={{ backgroundColor: 'green', color: 'white' }}>Search</Button>
          </Form>
          <Nav.Link href="#action2" style={{ color: 'white' }}>Log In</Nav.Link>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default BarraBusqueda;