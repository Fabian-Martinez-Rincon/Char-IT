class OfertaDetalle:
    def __init__(self, oferta_id,ofrecido, solicitado, fecha, hora, filial, estado):
        self.oferta_id = oferta_id
        self.ofrecido = ofrecido
        self.solicitado = solicitado
        self.fechaIntercambio = fecha
        self.horaIntercambio = hora
        self.filial = filial
        self.estado = estado