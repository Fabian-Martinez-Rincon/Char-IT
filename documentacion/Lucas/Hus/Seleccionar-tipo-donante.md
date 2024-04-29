# ID Seleccionar tipo donante y donación
# Título

**Como** usuario colaborador **Quiero** seleccionar el tipo de donante y tipo de donación **Para** efectuar el registro de donación

## Criterios de aceptación

- **Escenario 1:** Éxito al seleccionar tipo de donante usuario registrado y tipo de donación de producto
  **Dado** un donante registrado en el sistema
  **Cuando** el usuario colaborador selecciona el tipo de donante "Usuario" y el tipo de donación "Producto"
  **Entonces** el sistema lo redirige a al formulario de registro de donación de producto para usuarios registrados

- **Escenario 2:** Éxito al seleccionar tipo de donante registrado y tipo de donación de dinero
  **Dado** un donante registrado en el sistema
  **Cuando** el usuario colaborador selecciona el tipo de donante "Persona" y el tipo de donación "Dinero"
  **Entonces** el sistema lo redirige a al formulario de registro de donación de dinero para usuarios registrados

- **Escenario 3:** Éxito al seleccionar tipo de donante no registrado y tipo de donación de producto
  **Dado** un donante no registrado en el sistema
  **Cuando** el usuario colaborador selecciona el tipo de donante "Persona" y el tipo de donación "Producto"
  **Entonces** el sistema lo redirige a al formulario de registro de donación de producto para personas no registradas

- **Escenario 4:** Éxito al seleccionar tipo de donante no registrado y tipo de donación de dinero
  **Dado** un donante no registrado en el sistema
  **Cuando** el usuario colaborador selecciona el tipo de donante "Persona" y el tipo de donación "Dinero"
  **Entonces** el sistema lo redirige a al formulario de registro de donación de dinero para personas no registradas
  