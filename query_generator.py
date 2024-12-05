from openai import OpenAI

class QueryGenerator:
    def __init__(self, openai_client):
        self.openai_client = openai_client
    
    def generate_query(self, ordem):
        prompt = f"""
        Você é um assistente de criação de queries em SQL. Seu foco é entender a instrução fornecida por um chefe 
        delimitada pela tag <ordem> e criar um comando INSERT utilizando o conteúdo dentro da tag <query> como referência. 
        Retorne somente a query em texto plano. 
        Forneça a resposta sem usar delimitadores de código como ``` ou \n``` no início ou no final.

        <ordem>
        {ordem}
        </ordem>

        <query>
        INSERT INTO tarefa (title, description, responsible) VALUE ('<titulo>', '<descricao>', '<responsavel>')
        </query>
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
            print(f"Erro ao gerar a consulta: {e}")
            return None