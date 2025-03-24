from uuid import uuid4
from src.api import StoryGenerator
from src.tipos import TipoAcao

class JogoAventura:
    def __init__(self, enredo, personagem, mundo):
        self.enredo_base = enredo
        self.personagem = personagem
        self.mundo = mundo
        self.historico = []
        self.story_gen = StoryGenerator()
        self._iniciar_historia()

    def _iniciar_historia(self):
        contexto = self._construir_contexto_inicial()
        primeira_cena = self.story_gen.gerar_cena_inicial(contexto)
        self.historico.append(primeira_cena)

    def _construir_contexto_inicial(self):
        return {
            "mundo": self.mundo,
            "personagem": self.personagem,
            "enredo": self.enredo_base,
            "historico": []
        }

    def processar_acao(self, acao):
        contexto = self._construir_contexto_continuacao(acao)
        nova_cena = self.story_gen.gerar_continuacao(contexto)
        self.historico.append(nova_cena)

    def _construir_contexto_continuacao(self, acao):
        return {
            "mundo": self.mundo,
            "personagem": self.personagem,
            "historico": [self._resumir_cena(c) for c in self.historico[-3:]],
            "ultima_acao": {
                "texto": acao['texto'],
                "tipo": acao['tipo'].tipo
            }
        }

    def _resumir_cena(self, cena):
        return {
            "titulo": cena['titulo'],
            "resumo": cena['descricao'][:150] + "...",
            "acoes_escolhidas": cena.get('acao_escolhida', 'Nenhuma')
        }

    def adicionar_plot_twist(self):
        contexto = self._construir_contexto_continuacao({
            "texto": "Reviravolta do Narrador", 
            "tipo": TipoAcao("especial")
        })
        plot = self.story_gen.gerar_continuacao(contexto)
        self.historico[-1]['descricao'] += f"\n\n⚡ **Reviravolta:** {plot['descricao']}"

    def para_json(self):
        return {
            "mundo": self.mundo,
            "personagem": self.personagem,
            "historico": [
                {
                    "titulo": cena["titulo"],
                    "descricao": cena["descricao"],
                    "acoes": [
                        {
                            "tipo": {
                                "tipo": acao["tipo"].tipo,
                                "icone": acao["tipo"].icon()
                            },
                            "texto": acao["texto"]
                        } for acao in cena.get("acoes", [])
                    ],
                    "acao_escolhida": cena.get("acao_escolhida", None)
                } for cena in self.historico
            ]
        }