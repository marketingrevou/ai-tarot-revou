import os
import json
from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
import anthropic

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__, static_folder=".")

# ── Serve the SPA ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# ── AI Reading endpoint (streaming) ─────────────────────────────────────────
@app.route("/api/reading", methods=["POST"])
def reading():
    data       = request.get_json()
    profession = data.get("profession", "professional").strip() or "professional"
    cards      = data.get("cards", [])

    if len(cards) < 3:
        return jsonify({"error": "3 cards are required"}), 400

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY environment variable is not set"}), 500

    card_lines = "\n".join(f"- {c['position']}: {c['name']}" for c in cards)

    prompt = f"""Kamu adalah pembaca tarot AI yang bijak dan berwibawa. Penanya bekerja sebagai: {profession}.

Kartu yang terpilih:
{card_lines}

Tulis TEPAT 3 paragraf dalam bahasa Indonesia yang hangat, mudah dipahami, sopan, dan profesional. Setiap paragraf membahas satu kartu sesuai urutannya (masa lalu, masa kini, masa depan). Pisahkan tiap paragraf dengan satu baris kosong. JANGAN tulis header, judul, nomor, bullet point, atau tanda markdown apapun. Langsung mulai dengan isi paragraf pertama."""

    client = anthropic.Anthropic(api_key=api_key)

    def generate():
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=350,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    print("\nAI Tarot server starting...")
    print("Open http://localhost:5000 in your browser\n")
    app.run(debug=False, port=5000, threaded=True)
