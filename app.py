from unicodedata import category
from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
from models import setup_db, Sentence

def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    CORS(app, resources={r"*": {"origins": "*"}})
#    CORS Headers

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
    def update_Sentence(Sentence_id):
        body = request.get_json()
        Sentence = Sentence.query.get(Sentence_id)
        if Sentence is None:
            abort(404)
        if request.method == "PATCH":
            if "rating" in body:
                Sentence.rating = int(body["rating"])
            Sentence.update()
            return jsonify({
                "success": True,
                "Sentence": Sentence.format()
            })
        else:
            return jsonify({
                "success": True,
                "Sentence": Sentence.format()
            })

    @app.route("/sentences/<int:sentence_id>", methods=["DELETE"])
    def delete_Sentence(Sentence_id):
        Sentence = Sentence.query.get(Sentence_id)
        if Sentence is None:
            abort(404)
        Sentence.delete()
        return jsonify({
            "success": True,
            "deleted": Sentence_id
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
    def search_Sentences():
        body = request.get_json()
        if body is None:
            abort(400)
        if "searchTerm" not in body:
            abort(400)
        search_term = body["searchTerm"]
        Sentences = Sentence.query.filter(Sentence.title.ilike(f'%{search_term}%')).all()
        Sentences = [Sentence.format() for Sentence in Sentences]
        return jsonify({
            "success": True,
            "Sentences": Sentences,
            "total_Sentences": len(Sentences)
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

    return app
