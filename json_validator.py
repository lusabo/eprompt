from guardrails import guard
from guardrails.hub import ValidJson

class JsonValidator:
    def __init__(self) -> None:
        self.guard = guard.Guard().use(ValidJson, on_fail="exception")
    
    def is_valid(self, json: str) -> bool:
        try:
            self.guard.validate(json)
            return True
        
        except Exception as e:
            print(f"Erro na validação do JSON retornado pela LLM: {e}")
            return False