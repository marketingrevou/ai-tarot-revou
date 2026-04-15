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

    prompt = f"""Kamu adalah pembaca tarot AI yang bijak dan personal. Penanya adalah seorang {profession}.

Kartu yang terpilih:
{card_lines}

Tulis 5 blok teks dalam bahasa Indonesia yang hangat, mendalam, dan spesifik untuk bidang {profession}. Pisahkan tiap blok dengan satu baris kosong.

Blok 1 (masa lalu, kartu {c0['name']}): Tulis 2-3 kalimat bacaan yang relevan dan personal untuk seorang {profession}. Langsung di baris berikutnya (tanpa baris kosong): Ingat: [satu kalimat pesan atau pelajaran terpenting dari kartu ini]

Blok 2 (masa kini, kartu {c1['name']}): Tulis 2-3 kalimat bacaan yang relevan dan insightful untuk seorang {profession}. Langsung di baris berikutnya: Ingat: [satu kalimat saran konkret yang bisa langsung diterapkan]

Blok 3 (masa depan, kartu {c2['name']}): Tulis 2-3 kalimat bacaan yang inspiratif dan actionable untuk seorang {profession}. Langsung di baris berikutnya: Ingat: [satu kalimat motivasi atau ajakan bertindak yang kuat]

Blok 4 (sintesis): 2 kalimat yang merangkum bagaimana ketiga kartu saling terhubung sebagai satu perjalanan karir yang bermakna bagi seorang {profession}.

Blok 5 (aksi nyata): Tulis TEPAT 3 langkah konkret dan spesifik yang bisa dilakukan minggu ini oleh seorang {profession}, berdasarkan pesan ketiga kartu. Satu kalimat per langkah, pisahkan tiap langkah dengan satu baris (bukan baris kosong). Langkah harus praktis, spesifik, dan langsung bisa dilakukan.

PENTING: Jangan tulis label "Blok", header, judul, nomor, atau markdown apapun. Langsung mulai teks blok pertama."""

    client = anthropic.Anthropic(api_key=api_key)

    def generate():
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=1200,
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
