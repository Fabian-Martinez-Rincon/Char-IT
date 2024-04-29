ID Registrar donación en efectivo

Título

**Como** usuario colaborador **Quiero** registrar una donación en efectivo **Para** que quede registrado en el sistema

Regla de negocio
- El monto de la donación debe ser mayor a 0

Criterios de aceptación

- **Escenario 1:** Éxito al registrar donación en efectivo donado por un usuario
  **Dado** una donación en efectivo donado por un usuario con email usuarioefectivo@gmail.com que se encuentra registrado en el sistema
  **Cuando** el usuario colaborador selecciona registrar donación en efectivo e ingresa email:"usuarioefectivo@gmail.com" 
  y monto de la donación: 1000
  **Entonces** el sistema registra la donación en efectivo, se guarda la donación en el historial de donaciones del usuario y se muestra un mensaje de éxito.

- **Escenario 2:** Error al registrar donación en efectivo donado por un usuario por mail no registrado
  **Dado** una donación en efectivo donado por un usuario con email usuarioefectivofalso@gmai.com que no se encuentra registrado en el sistema
  **Cuando** el usuario colaborador selecciona registrar donación en efectivo e ingresa email:"usuarioefectivofalso@gmai.com" y monto de la donación: 1000
  **Entonces** el sistema muestra un mensaje de error indicando que el mail no se encuentra registrado en el sistema

- **Escenario 3:** Error al registrar donación en efectivo donado por un usuario con monto 0
  **Dado** una donación en efectivo donado por un usuario con email usuariocero@gmail.com 
  **Cuando** el usuario colaborador selecciona registrar donación en efectivo e ingresa email:"usuariocero@gmail.com" y monto de la donación: 0
  **Entonces** el sistema muestra un mensaje de error indicando que el monto de la donación debe ser mayor a 0

- **Escenario 4:** Éxito al registrar donación en efectivo donado por una persona no registrada 
  **Dado** una donación en efectivo donado por una persona no registrada en el sistema
  **Cuando** el usuario colaborador selecciona registrar donación en efectivo e ingresa monto de la donación: 1000, nombre del donante: "Pedro", apellido del donante: "Gomez" y email del donante: "pedrogomez@gmail.com" 
  **Entonces** el sistema registra la donación en efectivo y se muestra un mensaje de éxito.

- **Escenario 5:** Error al registrar donación en efectivo donado por una persona no registrada con monto 0
  **Dado** una donación en efectivo donado por una persona no registrada en el sistema
  **Cuando** el usuario colaborador selecciona registrar donación en efectivo e ingresa monto de la donación: 0, nombre del donante: "Pedro", apellido del donante: "Gomez" y email del donante: "pedrogomez@gmail.com"
  **Entonces** el sistema muestra un mensaje de error indicando que el monto de la donación debe ser mayor a 0
