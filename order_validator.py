import guardrails as guard

class OrderValidator:
    def __init__(self):
        self.guard = guard.Guard()
    
    def is_valid(self, text: str) -> bool:
        """
        Verifica se o texto configura uma ordem de um chefe para um funcionário.
        
        Args:
            text (str): Texto a ser validado
        
        Returns:
            bool: True se for uma ordem válida, False caso contrário
        """
        prompt = f"""
        Verifique a seguir se o texto delimitado por ```` se configura uma ordem de um chefe para um determinado funcionário. 
        A resposta deve se resumir a "True" em caso afirmativo e a "False" em caso negativo.

        ````
        {text}
        ````
        """

        try:
            result = self.guard(
                messages=[{"role": "system", "content": prompt}],
                model="gpt-4o-mini"
            )
            
            return result.raw_llm_output.lower() == "true"
        
        except Exception as e:
            print(f"Erro na validação: {e}")
            return False