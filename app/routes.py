from flask import Blueprint, request, jsonify
from openai import OpenAI
import tempfile

import os

bp = Blueprint('routes', __name__)

#client = OpenAI(api_key="")
#speachToken

@bp.route("/api/transcribe", methods=["POST"])
def transcribe():
    try:
        # Recibir archivo de audio
        audio_file = request.files["audio"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name

        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=open(tmp_path, "rb")
        )

        text = transcript.text.strip()

        if not text:
            return jsonify({"error": "No se pudo extraer texto del audio"}), 400

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "transcribe el audio a texto.Extrae las entidades"},
                {"role": "user", "content": text}
            ]
        )

        result = completion.choices[0].message.content.strip()

        return jsonify({"text": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500