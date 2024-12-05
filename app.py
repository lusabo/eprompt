import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from openai import OpenAI
from order_validator import OrderValidator
from data_generator import DataGenerator
from json_validator import JsonValidator

app = Flask(__name__)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
validator = OrderValidator()
json_validator = JsonValidator()
data_generator = DataGenerator(client)

@app.route('/transcribe-audio', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "Nenhum arquivo de áudio foi enviado."}), 400
    
    audio_file = request.files['audio']
    valid_extensions = ('.mp3', '.wav', '.m4a')
    if not audio_file.filename.endswith(valid_extensions):
        return jsonify({"error": f"Formato de áudio inválido. Apenas {', '.join(valid_extensions)} são permitidos."}), 400

    temp_file = f"temp_{audio_file.filename}"
    audio_file.save(temp_file)

    try:
        with open(temp_file, "rb") as audio_data:
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_data)
            
        if not transcription.text:
            return jsonify({"error": "Não foi possível transcrever o áudio."}), 500
        
        if not validator.is_valid(transcription.text):
            return jsonify({"error": "O pedido não parece uma ordem."}), 400
        
        if not json_validator.isValid(transcription.text):
            return jsonify({"error": "O JSON retornado pela LLM não é válido."}), 400
        
        task_json = data_generator.generate(transcription.text)

        return jsonify({"transcribed_text": transcription.text, "json": task_json})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        os.remove(temp_file)

if __name__ == '__main__':
    app.run(debug=True)