# ID: Comentar publicación

# Título

**Como** usuario general **Quiero** comentar una publicación **Para** interactuar con otro usuario

## Reglas de negocio

- El texto del comentario debe tener entre 1 y 280 caracteres

## Criterios de aceptación

- **Escenario 1:** Éxito al comentar publicación
  **Dado** una publicación y un texto de comentario con 230 caracteres
  **Cuando** el usuario general selecciona comentar publicación e ingresa el texto de 230 caracteres
  **Entonces** el sistema muestra el comentario en la publicación y notifica al autor de la publicación

- **Escenario 2:** Error al comentar publicación con texto vacío
  **Dado** una publicación y sin texto de comentario
  **Cuando** el usuario general selecciona comentar publicación y no ingresa el texto
  **Entonces** el sistema muestra un mensaje de error indicando que el texto del comentario es obligatorio

- **Escenario 3:** Error al comentar publicación con texto mayor a 280 caracteres
  **Dado** una publicación y un texto de comentario con 281 caracteres
  **Cuando** el usuario general selecciona comentar publicación e ingresa el texto de 281 caracteres
  **Entonces** el sistema muestra un mensaje de error indicando que el texto del comentario no puede ser mayor a 280 caracteres
