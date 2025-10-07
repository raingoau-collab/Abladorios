from flask import Flask, request, jsonify
from transformers import AutoProcessor, AutoModel
import torch
import tempfile

app = Flask(__name__)

# Load model and processor once at startup
processor = AutoProcessor.from_pretrained("fixie-ai/ultravox-v0_5-llama-3_2-1b", trust_remote_code=True)
model = AutoModel.from_pretrained(
    "fixie-ai/ultravox-v0_5-llama-3_2-1b",
    trust_remote_code=True,
    torch_dtype="auto"
)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio_file.save(tmp.name)
        inputs = processor(audio=tmp.name, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=256)
        text = processor.batch_decode(outputs, skip_special_tokens=True)[0]

    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
