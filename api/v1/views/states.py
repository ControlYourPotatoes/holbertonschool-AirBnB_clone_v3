#!/usr/bin/python3
""" objects that handle all default RestFul API actions for States """
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/api/v1/states', methods=['GET'])
def get_states():
    states = storage.all(State).values()
    state_list = []
    for state in states:
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/states', methods=['POST'])
def post_state():
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = State(**request.json)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app.route('/api/v1/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
