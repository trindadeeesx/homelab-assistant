import os

import requests


class LLMHandler:
    def __init__(self, api_key=None, model="google/gemma-3-27b-it"):
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        self.model = model
        self.url = "https://integrate.api.nvidia.com/v1/chat/completions"

    def generate_code(self, prompt: str, lang: str) -> str:
        """
        Gera um snippet de código a partir do prompt fornecido.
        language: python, bash, javascript, c++
        """

        if not self.api_key:
            return "API key da NVIDIA não configurada."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

        full_prompt = f"Escreva um snippet em {lang} que faça o seguinte:\n{prompt}. Seja breve. Apenas o código"

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": full_prompt}],
            "max_tokens": 512,
            "temperature": 0.2,
            "top_p": 0.7,
            "stream": False,
        }

        try:
            resp = requests.post(self.url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

            # a resposta do modelo normalmente vem em data['choices'][0]['message']['content']
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content.strip() or "A LLM não retornou nenhum código."
        except Exception as e:
            return f"Erro ao gerar código: {e}"
