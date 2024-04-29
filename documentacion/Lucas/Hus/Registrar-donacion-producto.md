ID Registrar donación de Producto

Título

**Como** usuario colaborador **Quiero** registrar una donación de producto **Para** que quede registrado en el sistema

Regla de negocio

Criterios de aceptación

- **Escenario 1:** Éxito al registrar donación de producto donado por un usuario
  **Dado** una donación de producto donado por un usuario con email usuario1@gmail.com que se encuentra registrado en el sistema
  **Cuando** el usuario colaborador selecciona registrar donación de producto e ingresa email:"usuario1@gmail.com" y selecciona la categoría del producto: "Alimento" y producto: "Arroz"
  **Entonces** el sistema registra la donación de producto, se guarda la donación en el historial de donaciones del usuario y se muestra un mensaje de éxito.

- **Escenario 2:** Error al registrar donación de producto donado por un usuario por mail no registrado
  **Dado** una donación de producto donado por un usuario con email usuariofalso@gmail.com que no se encuentra registrado en el sistema
  **Cuando** el usuario colaborador selecciona registrar donación de producto e ingresa email:"usuariofalso@gmail.com" y selecciona la categoría del producto: "Alimento" y producto: "Arroz"
  **Entonces** el sistema muestra un mensaje de error indicando que el mail no se encuentra registrado en el sistema

- **Escenario 3:** Éxito al registrar donación de producto donado por una persona no registrada
  **Dado** una donación de producto donado por una persona no registrada en el sistema
  **Cuando** el usuario colaborador selecciona registrar donación de producto e ingresa la categoría del producto: "Alimento", producto: "Arroz" y nombre del donante: "Juan", apellido del donante: "Perez", email del donante: "juanperez@gmail.com"
  **Entonces** el sistema registra la donación de producto y se muestra un mensaje de éxito.
