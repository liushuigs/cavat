from flask import Flask, jsonify
from models.domain import Domain
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/domain/all")
def domain_all():
    data = Domain.get_all()
    total = sum(item['article_num'] for item in data)
    return jsonify(article_total=total, data=data)


@app.route("/domain/today")
def domain_today():
    return "domain.today"


if __name__ == "__main__":
    app.run(debug=True)
