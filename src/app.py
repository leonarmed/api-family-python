"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

members = [
    {
        'first_name': "John",
        'age': 33,
        'lucky_numbers': [7, 13, 22]
    },
    {
        'first_name': "Jane",
        'age': 35,
        'lucky_numbers': [10, 14, 3]
    },
    {
        'first_name': "Jimmy",
        'age': 5,
        'lucky_numbers': [1]
    },
]

for member in members:
    jackson_family.add_member(member)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    member = request.json
    new_member = {
        "first_name": member['first_name'],
        "age": member['age'],
        "id": member['id'],
        "lucky_numbers": member['lucky_numbers'],
    }
    jackson_family.add_member(new_member)

    return jsonify(), 200

@app.route('/member/<int:id>', methods=['GET', 'DELETE'])
def get_member(id):
    if request.method == 'GET':
        member = jackson_family.get_member(id)
        if member is not None:
            print(member,"/////////")
            return jsonify({
                "first_name": member['first_name'],
                "id": member['id'],
                "age": member['age'],
                "lucky_numbers": member['lucky_numbers'],
            }), 200
        return jsonify({}), 200
    elif request.method == 'DELETE':
        new_members = jackson_family.delete_member(id)
        limit_member = []
        for member in new_members:
            if len(limit_member) < 4:
                print("Len:", len(limit_member))
                limit_member.append(member)
        return jsonify({"done":True, "data": limit_member}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
