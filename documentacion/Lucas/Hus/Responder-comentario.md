ID: Responder comentario

Título

**Como** usuario general **Quiero** responder un comentario **Para** interactuar con otro usuario

Reglas de negocio

- El texto de respuesta debe tener entre 1 y 280 caracteres

## Criterios de aceptación

- **Escenario 1:** Éxito al responder comentario
  **Dado** una comentario en una publicación mia y un texto de respuesta con 230 caracteres
  **Cuando** el usuario general selecciona responder comentario e ingresa el texto con 230 caracteres
  **Entonces** el sistema muestra la respuesta debajo del comentario y notifica al autor del comentario

- **Escenario 2:** Error al responder comentario con texto vacío
  **Dado** una comentario en una publicación mia y sin texto de respuesta
  **Cuando** el usuario general selecciona responder comentario y no ingresa el texto
  **Entonces** el sistema muestra un mensaje de error indicando que el texto de la respuesta es obligatorio

- **Escenario 3:** Error al responder comentario con texto mayor a 280 caracteres
  **Dado** una comentario en una publicación mia y un texto de respuesta con 281 caracteres
  **Cuando** el usuario general selecciona responder comentario e ingresa el texto con 281 caracteres
  **Entonces** el sistema muestra un mensaje de error indicando que el texto de la respuesta no puede ser mayor a 280 caracteres
