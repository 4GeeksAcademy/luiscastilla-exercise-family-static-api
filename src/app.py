import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)   

jackson_family = FamilyStructure("Jackson")
jackson_family.agregar_member({
    "id": jackson_family._generarId(),
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
    })
jackson_family.agregar_member({
    "id": jackson_family._generarId(),
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
    })
jackson_family.agregar_member({
    "id": jackson_family._generarId(),
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
    })

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.optener_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.optener_member(member_id)
    if member is None:
        return jsonify({"msg": "Member not found"}), 404
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    if "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"msg": "Invalid data"}), 400
    jackson_family.agregar_member(data)
    return jsonify({"msg": "Member added successfully"}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.eliminar_member(member_id)
    if not result:
        return jsonify({"msg": "Member not found"}), 404
    return jsonify({"done": True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
