class OfertaDetalle:
    def __init__(self, oferta_id,ofrecido, solicitado, fecha, hora, filial, estado, descripcion,ofrecido_email, solicitado_email):
        self.oferta_id = oferta_id
        self.ofrecido = ofrecido
        self.solicitado = solicitado
        self.fechaIntercambio = fecha
        self.horaIntercambio = hora
        self.filial = filial
        self.estado = estado
        self.descripcion = descripcion
        self.solicitado_email = solicitado_email
        self.ofrecido_email = ofrecido_email
