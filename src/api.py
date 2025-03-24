import os
import re
import requests
from uuid import uuid4
from src.tipos import TipoAcao

class StoryGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def gerar_cena_inicial(self, contexto):
        prompt = f"""
        **Criar Cena Inicial:**
        Mundo: {contexto['mundo']}
        Personagem: {contexto['personagem']['nome']} ({contexto['personagem']['classe']})
        Habilidade: {contexto['personagem']['habilidade']}
        Premissa: {contexto['enredo']}

        **Instruções:**
        1. Criar 3 parágrafos narrativos
        2. Estabelecer conflito central
        3. Gerar 3 ações usando APENAS estes tipos:
           [explorar], [dialogo], [combate], [magia], [furtivo]

        **Formato Obrigatório:**
        TÍTULO: [Título Criativo]
        DESCRIÇÃO: |
          [Texto descritivo]
        AÇÕES:
        - [tipo] [Descrição ação 1]
        - [tipo] [Descrição ação 2]
        - [tipo] [Descrição ação 3]
        """
        return self._processar_resposta(self._chamar_api(prompt))

    def gerar_continuacao(self, contexto):
        historico = "\n".join([f"- {c['resumo']}" for c in contexto['historico']])
        
        prompt = f"""
        **Continuar História:**
        Última Ação: {contexto['ultima_acao']['texto']} ({contexto['ultima_acao']['tipo']})
        Histórico Recente:
        {historico}

        **Instruções:**
        1. Continuar de forma coerente
        2. Usar 2-3 parágrafos
        3. Oferecer 3 ações usando tipos pré-definidos

        **Tipos Válidos:**
        explorar | dialogo | combate | magia | furtivo | investigar

        **Exemplo:**
        TÍTULO: Nas Profundezas da Cripta
        DESCRIÇÃO: O ar está denso com mistério...
        AÇÕES:
        - [explorar] Investigar os hieróglifos
        - [magia] Ativar os runas ancestrais
        - [furtivo] Esgueirar-se pela passagem secreta
        """
        return self._processar_resposta(self._chamar_api(prompt))

    def _chamar_api(self, prompt):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": "google/gemma-3-12b-it:free",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 1500
        }
        return requests.post(self.base_url, json=payload, headers=headers).json()

    def _processar_resposta(self, resposta):
        content = resposta.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # Extração de componentes
        titulo = re.search(r'TÍTULO:\s*(.+?)\n', content)
        descricao = re.search(r'DESCRIÇÃO:\s*\|?\s*(.+?)(?=\nAÇÕES:|\Z)', content, re.DOTALL)
        
        # Processar ações com normalização
        acoes = []
        for match in re.finditer(r'- \[(\w+)\] (.+)', content):
            if len(acoes) >= 3:
                break
            tipo_raw = match.group(1).lower()
            texto = match.group(2).strip()
            
            # Normalização de tipos
            tipo = self._mapear_tipo(tipo_raw)
            acoes.append(self._criar_acao(tipo, texto))

        return {
            "id": str(uuid4()),
            "titulo": titulo.group(1).strip() if titulo else "Cena Sem Título",
            "descricao": self._limpar_descricao(descricao.group(1)) if descricao else "A narrativa se desenvolve...",
            "acoes": acoes
        }

    def _mapear_tipo(self, tipo_raw):
        mapeamento = {
            "explore": "explorar",
            "talk": "dialogo",
            "dialogue": "dialogo",
            "fight": "combate",
            "magic": "magia",
            "sneak": "furtivo",
            "investigate": "investigar"
        }
        return mapeamento.get(tipo_raw, tipo_raw)

    def _limpar_descricao(self, texto):
        # Converter quebras de linha em HTML válido para XML
        texto = texto.replace('\n', '<br/>')
        # Remover caracteres problemáticos e normalizar
        texto = texto.replace('|', '').strip()
        # Substituir caracteres especiais
        texto = texto.encode('latin-1', 'ignore').decode('latin-1')
        return texto

    def _criar_acao(self, tipo, texto):
        return {
            "id": str(uuid4()),
            "tipo": TipoAcao(tipo),
            "texto": texto,
            "dica": self._gerar_dica(tipo)
        }

    def _gerar_dica(self, tipo):
        dicas = {
            "explorar": "Revela novos caminhos e segredos",
            "dialogo": "Obtém informações e desenvolve relacionamentos",
            "combate": "Define o rumo dos conflitos através da força",
            "magia": "Usa habilidades sobrenaturais para resolver problemas",
            "furtivo": "Permite evitar confrontos diretos",
            "investigar": "Descobre detalhes ocultos e pistas"
        }
        return dicas.get(tipo, "Ação estratégica")