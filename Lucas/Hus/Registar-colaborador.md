# ID Registrar colaborador

# Título

**Como** usuario owner **Quiero** registrar un colaborador **Para** habilitarle las funcionalidades correspondientes

# Regla de negocio

- El mail debe ser único en el sistema

## Criterios de aceptación

- **Escenario 1:** Éxito al registrar colaborador
  **Dado** el mail colaborador@gmail.com el cual no se encuentra registrado previamente
  **Cuando** se ingresa el mail:"colaborador@gmail.com", nombre:"Juan", apellido:"Perez"
  **Entonces** el sistema da de alta un nuevo colaborador e informa que la contraseña fue enviada al mail registrado y lo redirige a iniciar sesión

- **Escenario 2:** Error al registrar colaborador
  **Dado** el mail colaboradorusado@gmail.com el cual ya se encuentra registrado previamente
  **Cuando** se ingresa el mail:"colaboradorusado@gmail.com" y nombre:"Juan", apellido:"Perez"
  **Entonces** el sistema muestra un mensaje de error indicando que el mail ya se encuentra registrado






