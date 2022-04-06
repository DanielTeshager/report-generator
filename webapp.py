from unicodedata import category
from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
from models import setup_db, Sentence


app = Flask(__name__)
#CORS allow origin from www.leadyaa.com only
CORS(app, resources={r"*": {"origins": "https://endearing-cendol-1d8350.netlify.app"}})
setup_db(app)

@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response

@app.route("/sentences")
def get_Sentences():
    Sentences = Sentence.query.order_by(Sentence.id).all()
    total_Sentences = len(Sentences)
    if not Sentences:
        abort(404)
    Sentences = [Sentence.format() for Sentence in Sentences]

    return jsonify({
        "success": True,
        "Sentences": Sentences,
        "total_Sentences": total_Sentences
    })

@app.route("/sentences/<int:sentence_id>", methods=["PATCH","GET"])
def update_Sentence(sentence_id):
    body = request.get_json()
    sentence = Sentence.query.get(sentence_id)
    if sentence is None:
        abort(404)
    if request.method == "PATCH":
        if "rating" in body:
            sentence.rating = int(body["rating"])
        sentence.update()
        return jsonify({
            "success": True,
            "Sentence": sentence.format()
        })
    else:
        return jsonify({
            "success": True,
            "Sentence": Sentence.format()
        })

@app.route("/sentences/<int:sentence_id>", methods=["DELETE"])
def delete_Sentence(sentence_id):
    sentence = Sentence.query.get(sentence_id)
    if sentence is None:
        abort(404)
    sentence.delete()
    return jsonify({
        "success": True,
        "deleted": sentence_id
    })


@app.route("/sentences", methods=["POST"])
def create_Sentence():
    body = request.get_json()
    print('body', body)

    if body is None:
        abort(400)

    if "title" not in body or "category" not in body:
        abort(400)

    sentence = Sentence(title=body["title"], category=body["category"])
    print(sentence)
    # insert into db

    sentence.insert()
    return jsonify({
        "success": True,
        "created": sentence.id,
        "Sentences": [sentence.format()],
        "total_Sentences": Sentence.query.count()
    })

@app.route('/sentences/search', methods=['POST'])
def search_sentences():
    body = request.get_json()
    if body is None:
        abort(400)
    if "searchTerm" not in body:
        abort(400)
    search_term = body["searchTerm"]
    sentences = Sentence.query.filter(Sentence.title.ilike(f'%{search_term}%')).all()
    sentences = [sentence.format() for sentence in sentences]
    return jsonify({
        "success": True,
        "Sentences": sentences,
        "total_Sentences": len(sentences)
    })
    
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


if __name__ == "__main__":
    app.run(debug=True)