from flask import Blueprint, jsonify, request
from models import User, Character, Location, Phrase, db

api = Blueprint("api", __name__)


@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"Error": "Not found"}), 404
    return jsonify(user.serialize_complete()), 201


@api.route('/users/<int:id>/favorites', methods=['GET'])
def get_favorites(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    characters_fav = [character.serialize()
                      for character in user.characters_like]
    locations_fav = [location.serialize() for location in user.locations_like]
    return jsonify({
        "characters": characters_fav,
        "locations": locations_fav
    }), 200


@api.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    requierd_fields = ["username", "firstname",
                       "lastname", "email", "password"]
    missing = [field for field in requierd_fields if field not in data]
    if missing:
        return jsonify({"Error": f"does not exist {missing}"}), 400
    new_user = User(
        username=data["username"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200


@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'Error': 'User not found'}), 404

    # Comprobacion adicional para ver que no este siendo usado el username

    new_username = data.get('username')

    if new_username and new_username != user.username:
        check = User.query.filter_by(username=new_username).first()
        if check:
            return jsonify({'Error': 'the username already exists'})

    new_email = data.get('email')

    if new_email and new_email != user.username:
        check = User.query.filter_by(username=new_username).first()
        if check:
            return jsonify({'Error': 'the username already exists'})

    user.username = data.get('username', user.username)
    user.firstname = data.get('firstname', user.firstname)
    user.lastname = data.get('lastname', user.lastname)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)

    db.session.commit()
    return jsonify(user.serialize()), 200


@api.route('/phrase', methods=['POST'])
def add_phrase():
    data = request.get_json()

    if not data.get('text') or not data.get('character_id'):
        return jsonify({'Error': 'Faltan datos'}), 400

    character = Character.query.get(data['character_id'])
    if not character:
        return jsonify({"Error": "Character not found"}), 404

    new_phrase = Phrase(
        text=data['text'],
        character_id=data['character_id']
    )
    db.session.add(new_phrase)
    db.session.commit()
    return jsonify(new_phrase.serialize()), 201


@api.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    response = [character.serialize() for character in characters]
    return jsonify(response), 200


@api.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get(id)
    if not character:
        return jsonify({"Error": "Not found"}), 404
    return jsonify(character.serialize_complete()), 201


@api.route('/users/<int:user_id>/characters/<int:character_id>', methods=['POST'])
def add_character_like(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user or not character:
        return jsonify({'Error': 'User or character not found'}), 404
    if character in user.characters_like:
        return jsonify({"msg": "This character is already a favorite."}), 400

    user.characters_like.append(character)
    db.session.commit()

    return jsonify(user.serialize_complete()), 200


@api.route('/users/<int:user_id>/characters/<int:character_id>', methods=['DELETE'])
def remove_character_likes(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user or not character:
        return jsonify({'Error': 'User or character not found'}), 404
    if character in user.characters_like:
        user.characters_like.remove(character)

    db.session.commit()
    return jsonify({"msg": "Character deleted succesfully"}), 200


@api.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    response = [location.serialize() for location in locations]
    return jsonify(response), 200


@api.route('/locations/<int:id>', methods=['GET'])
def get_location(id):
    location = Location.query.get(id)
    if not location:
        return jsonify({"Error": "Not found"}), 404
    return jsonify(location.serialize()), 201


@api.route('/users/<int:user_id>/locations/<int:location_id>', methods=['POST'])
def add_locations_like(user_id, location_id):
    user = User.query.get(user_id)
    location = Location.query.get(location_id)

    if not user or not location:
        return jsonify({'Error': 'User or location not found'}), 404
    if location in user.characters_like:
        return jsonify({"msg": "This location is already a favorite"}), 400

    user.locations_like.append(location)
    db.session.commit()

    return jsonify(user.serialize()), 200


@api.route('/users/<int:user_id>/locations/<int:location_id>', methods=['DELETE'])
def remove_location_likes(user_id, location_id):
    user = User.query.get(user_id)
    location = Location.query.get(location_id)

    if not user or not location:
        return jsonify({'Error': 'User or location not found'}), 404
    if location in user.locations_like:
        user.locations_like.remove(location)

    db.session.commit()
    return jsonify(user.serialize_complete()), 200
