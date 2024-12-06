from openai import OpenAI

class DataGenerator:
    def __init__(self, openai_client):
        self.openai_client = openai_client
    
    def generate(self, ordem):
        prompt = f"""
        Você é um assistente de criação de objetos JSON. 
        Seu foco é entender a instrução fornecida por um chefe delimitada pela tag <ordem>. 
        Você deve gerar um título, identificar a tarefa solicitada e identificar para quem foi a ordem. 
        Ao final você deve criar um objeto JSON com os atributos 'titulo', 'descricao' e 'responsavel'.
        Retorne somente json em texto plano. 
        Forneça a resposta sem usar delimitadores de código como ``` ou \n``` no início ou no final.
        <ordem>
        {ordem}
        </ordem>
        """
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    { "role": "user", "content": prompt }
                ]
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Erro ao gerar o JSON: {e}")
            return None