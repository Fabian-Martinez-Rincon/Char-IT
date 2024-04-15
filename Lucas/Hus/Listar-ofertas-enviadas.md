# ID: Listar ofertas enviadas

# Título

**Como** usuario general **Quiero** ver el listado de mis ofertas enviadas **Para** consultar su estado

## Reglas de negocio

- El listado puede estar vació

## Criterios de aceptación

- **Escenario 1:** Éxito al listar listado de ofertas enviadas
  **Dado** un listado con ofertas enviadas
  **Cuando** el usuario general selecciona listar ofertas enviadas
  **Entonces** el sistema muestra el listado de ofertas enviadas, cada oferta con su respectiva información general
  
- **Escenario 2:** Éxito al listar listado de ofertas enviadas vació
  **Dado** un listado vació de ofertas enviadas
  **Cuando** el usuario general selecciona listar ofertas enviadas
  **Entonces** el sistema muestra un mensaje indicando que no hay ofertas enviadas
