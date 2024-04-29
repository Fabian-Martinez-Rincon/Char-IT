 ID: Rechazar oferta
 
 Título

**Como** usuario general **Quiero** Rechazar la oferta **Para** buscar otra oferta que me interese

Reglas de negocio

- La descripción debe tener entre 10 y 280 caracteres

 
 Criterios de aceptación

- **Escenario 1:** Éxito al Rechazar oferta
  **Dado** una oferta y una descripción de rechazo de 200 caracteres
  **Cuando** el usuario general selecciona rechazar oferta y escribe la descripción de rechazo de 200 caracteres
  **Entonces** el sistema muestra un mensaje que la oferta fue rechazada, cambia el estado de la oferta a rechazada y almacena la descripción del rechazo.

- **Escenario 2:** Error al Rechazar oferta sin descripción
  **Dado** una oferta
  **Cuando** el usuario general selecciona rechazar oferta y no escribe la descripción de el rechazo
  **Entonces** el sistema muestra un mensaje de error indicando que la descripción del rechazo es obligatoria.

- **Escenario 3:** Error al Rechazar oferta con descripción menor a 10 caracteres
  **Dado** una oferta y una descripción de rechazo con 9 caracteres
  **Cuando** el usuario general selecciona rechazar oferta y escribe la descripción de rechazo de 9 caracteres
  **Entonces** el sistema muestra un mensaje de error indicando que la descripción del rechazo no puede ser menor a 10 caracteres

- **Escenario 4:** Error al Rechazar oferta con descripción mayor a 280 caracteres
  **Dado** una oferta y una descripción de rechazo con 281 caracteres
  **Cuando** el usuario general selecciona rechazar oferta y escribe la descripción de rechazo de 281 caracteres
  **Entonces** el sistema muestra un mensaje de error indicando que la descripción del rechazo no puede ser mayor a 280 caracteres
