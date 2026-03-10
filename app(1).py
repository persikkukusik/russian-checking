from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# load everything once on startup into memory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("loading dictionary...")
with open(os.path.join(BASE_DIR, "russian_words.txt"), encoding="utf-8") as f:
    WORDS = set(line.strip() for line in f if line.strip())
print(f"loaded {len(WORDS)} words")

print("loading swear roots...")
with open(os.path.join(BASE_DIR, "swear_roots.txt"), encoding="utf-8") as f:
    SWEAR_ROOTS = [line.strip() for line in f if line.strip()]
print(f"loaded {len(SWEAR_ROOTS)} swear roots")


@app.route("/validate", methods=["GET"])
def validate():
    word = request.args.get("word", "").strip().lower()

    if not word:
        return jsonify({"error": "no word provided"}), 400

    exists = word in WORDS
    appropriate = not any(root in word for root in SWEAR_ROOTS)

    return jsonify({
        "exists": exists,
        "appropriate": appropriate
    })


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "words_loaded": len(WORDS)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
