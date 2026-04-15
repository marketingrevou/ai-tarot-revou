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


@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("images", filename)


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

    c0, c1, c2 = cards[0], cards[1], cards[2]

    prompt = f"""Kamu adalah pembaca tarot AI yang bijak. Penanya adalah seorang {profession}.

Kartu yang terpilih:
{card_lines}

Tulis 4 blok singkat dalam bahasa Indonesia yang personal dan relevan, khusus untuk seorang {profession} di era AI. Pisahkan tiap blok dengan satu baris kosong.

Blok 1 (kartu {c0['name']}): 2 kalimat — fondasi atau kekuatan yang sudah dimiliki seorang {profession} untuk menghadapi era AI, berdasarkan kartu ini.

Blok 2 (kartu {c1['name']}): 2 kalimat — kesempatan nyata dan tantangan terbesar seorang {profession} di era AI saat ini, berdasarkan kartu ini.

Blok 3 (kartu {c2['name']}): 2 kalimat — potensi besar dan masa depan yang bisa dicapai seorang {profession} jika memanfaatkan AI dengan benar, berdasarkan kartu ini.

Blok 4 (langkah nyata): Tepat satu kalimat — satu langkah konkret dan spesifik yang bisa dilakukan minggu ini oleh seorang {profession} untuk mulai memanfaatkan AI, berdasarkan ketiga kartu di atas.

PENTING: Jangan tulis label "Blok", header, judul, nomor, atau markdown. Langsung mulai teks blok pertama."""

    client = anthropic.Anthropic(api_key=api_key)

    def generate():
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
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
