from flask import Flask, jsonify
from models.domain import Domain
from models.article import Article
app = Flask(__name__)


@app.route("/")
def hello():
    return "ok!"


@app.route("/domain/all")
def domain_all():
    data = Domain.get_all()
    total = sum(item['article_num'] for item in data)
    data = sorted(data, key=lambda k: k['article_num'], reverse=True)
    return jsonify(article_total=total, data=data)


@app.route("/domain/today")
def domain_today():
    data = Domain.get_all()
    result = []
    total = 0
    for item in data:
        article_new = Article.count(item['domain'], today=True)
        result.append({
            'domain': item['domain'],
            'article_num': article_new
        })
        total += article_new
    result = sorted(result, key=lambda k: k['article_num'], reverse=True)
    return jsonify(article_total=total, data=result)


if __name__ == "__main__":
    app.run(debug=True)
