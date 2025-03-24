class TipoAcao:
    def __init__(self, tipo):
        self.tipo = tipo.lower()  # Normaliza para minúsculas

    def icon(self):
        icons = {
            "explorar": "🔍",
            "dialogo": "💬",
            "combate": "⚔️",
            "magia": "✨",
            "furtivo": "👤",
            "investigar": "🔎",
            "viajar": "🧭",
            "negociar": "🤝",
            "coletar": "🎒",
            "especial": "🌟",
            "default": "❓"
        }
        return icons.get(self.tipo, icons['default'])
    
    def to_dict(self):
        return {
            "tipo": self.tipo,
            "icone": self.icon(),
            "descricao": self._descricao_tipo()
        }
    
    def _descricao_tipo(self):
        descricoes = {
            "explorar": "Investigar ambiente e descobrir segredos",
            "dialogo": "Conversar com personagens para obter informações",
            "combate": "Enfrentar desafios através de confronto direto",
            "magia": "Utilizar habilidades mágicas ou especiais",
            "furtivo": "Agir de maneira discreta e estratégica",
            "investigar": "Examinar detalhes específicos do cenário",
            "viajar": "Mover-se para novos locais",
            "negociar": "Resolver situações através de diplomacia",
            "coletar": "Adquirir recursos importantes",
            "default": "Ação indefinida"
        }
        return descricoes.get(self.tipo, descricoes['default'])