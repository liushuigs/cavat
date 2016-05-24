from flask import Flask, jsonify, request
from urlparse import urlparse
from models.domain import Domain
from models.article import Article
from models.raw_data import RawData
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


@app.route("/raw_data", methods=['POST'])
def raw_data():
    received = request.json
    data = {}
    o = urlparse(received['url'])
    # get first level domain
    data['domain'] = '.'.join(o.hostname.split('.')[-2:])
    data['url'] = received['url']
    data['html'] = received['source']
    data['http_status'] = 200
    data['parsed_as_entry'] = 0
    data['depth'] = 1
    RawData.create_entry(**data)
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(debug=True)
