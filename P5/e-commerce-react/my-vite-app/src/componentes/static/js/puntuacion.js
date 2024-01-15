document.addEventListener('DOMContentLoaded', () => {
    const elementosConEstrellas = document.querySelectorAll('.p-4.flex.items-start');

    let isAuthenticated = document.body.getAttribute("data-is-authenticated")  === "true";  // Devuelve un string, y aquí quiero manejar un booleano

    elementosConEstrellas.forEach((elemento) => {
        elemento.innerHTML = '';
        const numeroEstrellaClicada = 3;  // Por defecto 3 estrellas

        for (let i = 0; i < 5; i++) {
            const estrella = document.createElement('span');
            estrella.classList.add('fa', 'fa-star', 'fa-3x');

            // recogerRatingDelServidor()   -----> Necesito saber de qué producto obtener puntuación

            estrella.classList.toggle('checked', i < numeroEstrellaClicada);    // Siempre meto 3 estrellas, y si estoy autenticado, cuando clicke en una se cambian

            if (isAuthenticated) {
                estrella.addEventListener('click', () => {
                    let numeroEstrellaClicada = i + 1;

                    const estrellas = elemento.querySelectorAll('.fa-star');
                    estrellas.forEach((estrella, j) => {
                        estrella.classList.toggle('checked', j < numeroEstrellaClicada);
                    });

                //    console.log(`Estrella clicada: ${numeroEstrellaClicada}`);
                    let productId = estrella.closest('.flex').dataset.id;
                    // ¡El id del producto se recibe bien!
                  //  console.log(`El id del producto clickado es ${productId}`)

                    // Puedes enviar la calificación al servidor aquí si es necesario
                    enviarCalificacionHaciaAPI(productId,numeroEstrellaClicada);
                });
            }

            elemento.appendChild(estrella);
        }
    });

    function enviarCalificacionHaciaAPI(id, calificacion) {
        const apiUrl = `http://localhost:8000/api/puntuar?id=${id}&calificacion=${calificacion}`;

        const headers = {
            Authorization: `Bearer token_dai`,
            'X-CSRFToken': obtenerCSRFToken()
        };

        axios.put(apiUrl, {}, { headers })
            .then(response => {
                console.log('Respuesta de la API:', response.data);
                let averagePuntuationElement = document.getElementById(`average_puntuation_${id}`);
                let votesElement = document.getElementById(`votes_${id}`);

                // Modificar el contenido de los elementos HTML con la nueva información
                averagePuntuationElement.textContent = `Average Puntuation: ${response.data.rate}`;
                votesElement.textContent = `Votes: ${response.data.count}`;
            })
            .catch(error => {
                console.error('Error al enviar o recibir la solicitud:', error);
            });
    }

    function obtenerCSRFToken() {
        const cookieValue = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          .split('=')[1];
      
        return cookieValue;
      }
    
});
