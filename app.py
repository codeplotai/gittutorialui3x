from flask import Flask, render_template, request, jsonify
from rag import ask_rag3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "POST":q
        data = request.json
        question = data["message"]
        answer = ask_rag(question)
        return jsonify({"answer": answer})
    else:
        return "Send a POST request."

if __name__ == "__main__":
    app.run(port=5028
            , debug=True)