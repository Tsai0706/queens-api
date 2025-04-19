from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # ✅ 啟用跨來源請求支援（CORS）

def check_conflict(x_num, seq):
    seq = [seq[i] + x_num * i for i in range(len(seq))]
    n_of_conflict = 0

    for i in range(x_num):
        for j in range(x_num):
            x = seq[i]
            y = seq[j]
            if i != j and ((x - y) % x_num == 0 or x // x_num == y // x_num):
                n_of_conflict += 1

            right = (x_num - 1) - (x % x_num)
            up = x // x_num
            left = x % x_num
            down = (x_num - 1) - up

            if i != j and (x - y) % (x_num - 1) == 0:
                index1 = min(right, up)
                index2 = min(left, down)
                for k in range(index1):
                    if x - (x_num - 1) * (k + 1) == y:
                        n_of_conflict += 1
                for k in range(index2):
                    if x + (x_num - 1) * (k + 1) == y:
                        n_of_conflict += 1

            if i != j and (x - y) % (x_num + 1) == 0:
                index1 = min(left, up)
                index2 = min(right, down)
                for k in range(index1):
                    if x - (x_num + 1) * (k + 1) == y:
                        n_of_conflict += 1
                for k in range(index2):
                    if x + (x_num + 1) * (k + 1) == y:
                        n_of_conflict += 1

    return n_of_conflict // 2

@app.route("/check_queens", methods=["POST"])
def check_queens():
    data = request.get_json()
    x_num = data.get("x_num")
    seq = data.get("seq")

    if not isinstance(x_num, int) or not isinstance(seq, list):
        return jsonify({"error": "請提供正確的 x_num（整數）與 seq（整數陣列）"}), 400

    conflict = check_conflict(x_num, seq)
    return jsonify({"conflict": conflict})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)