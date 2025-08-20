from flask import request, jsonify, Flask
from groq import Groq
import json
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
@app.route('/webhook',methods=['POST'])
def resume():
    dados = request.get_json()
    if not dados or 'videoId' not in dados:
        return jsonify({"error": "O campo 'videoId' é obrigatório no corpo do JSON."}), 400
    idd = dados['videoId']
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    ytt_api = YouTubeTranscriptApi()
    s=ytt_api.fetch(idd)
    list_t = []
    for item in s:
        list_t.append(item.text)
    full_s = " ".join(list_t)
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
        {
            "role": "System",
            "content": "Você é um assistente especialista em criar resumos concisos de vídeos. Sempre faça o resumo em tópicos",
        },
        {
            "role": "user",
            "content": f"Resume this transcription of a video {full_s}",
        },
        ]
    )
    resumo_final = completion.choices[0].message.content
    resultado_em_dict = {
        "ID":idd,
        "text":resumo_final
    }
    return jsonify(resultado_em_dict)
    

if __name__ == '__main__':
    app.run(debug=True)






