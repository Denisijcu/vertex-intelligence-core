from dotenv import load_dotenv
import os
import anthropic

class VIC_AI_Client:
    def __init__(self, model="claude-sonnet-4-20250514"):
        self.model = model
        self.client = anthropic.Anthropic()  # usa ANTHROPIC_API_KEY del env

    def ask_ai(self, prompt, system_prompt="Eres un experto en ciberseguridad ofensiva."):
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error de conexión con Anthropic: {e}"
        
