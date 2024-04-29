ID: Listar ofertas recibidas

Título

**Como** usuario general **Quiero** ver el listado de mis ofertas recibidas **Para** consultar su estado

Reglas de negocio

- El listado puede estar vació

Criterios de aceptación

- **Escenario 1:** Éxito al listar listado de ofertas recibidas
  **Dado** un listado con ofertas recibidas
  **Cuando** el usuario general selecciona listar ofertas recibidas
  **Entonces** el sistema muestra el listado de ofertas recibidas, cada oferta con su respectiva información general

- **Escenario 2:** Éxito al listar listado de ofertas recibidas vació
  **Dado** un listado vació de ofertas recibidas
  **Cuando** el usuario general selecciona listar ofertas recibidas
  **Entonces** el sistema muestra un mensaje indicando que no hay ofertas recibidas
