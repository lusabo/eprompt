import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from openai import OpenAI
from order_validator import OrderValidator
from query_generator import QueryGenerator


app = Flask(__name__)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
validator = OrderValidator()
query_generator = QueryGenerator(client)

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
        
        generated_query = query_generator.generate_query(transcription.text)

        return jsonify({"transcribed_text": transcription.text,"query": generated_query})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        os.remove(temp_file)

if __name__ == '__main__':
    app.run(debug=True)