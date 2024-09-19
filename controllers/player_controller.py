from flask import Blueprint, jsonify, request
from repository.player_repository import (
    get_all_players,
    find_player_by_id,
    create_player,
    update_player,
    delete_player
)
from models.PlayerModel import PlayerStats
from dataclasses import asdict
from dto.Error_dto import PlayerErrorDto

player_blueprint = Blueprint("player", __name__)


@player_blueprint.route("/players", methods=["GET"])
def get1_all_players():
    players = get_all_players()
    players_list = list(map(asdict, players))
    return jsonify(players_list), 200


@player_blueprint.route("/player/<int:player_id>", methods=["GET"])
def get_player_by_id(player_id):
    try:
        player = find_player_by_id(player_id)
        if player:
            return jsonify(PlayerErrorDto(body=player)), 200
        else:
            return jsonify(PlayerErrorDto(error="Player not found")), 404
    except Exception as e:
        return jsonify(PlayerErrorDto(error=f"An error occurred: {str(e)}")), 500



@player_blueprint.route("/create", methods=["POST"])
def create_new_player():
    data = request.get_json()
    required_fields = ["player_id", "player_name", "team", "position", "seasons", "points", "games", "two_percent",
                       "three_percent", "atr", "ppg_ratio"]
    if not data or not all(key in data for key in required_fields):
        return jsonify(PlayerErrorDto(error="Missing player data")), 400

    new_player = PlayerStats(
        player_id=data["player_id"],
        player_name=data["player_name"],
        team=data["team"],
        position=data["position"],
        seasons=data["seasons"],
        points=data["points"],
        games=data["games"],
        two_percent=data["two_percent"],
        three_percent=data["three_percent"],
        atr=data["atr"],
        ppg_ratio=data["ppg_ratio"]
    )
    p_id = create_player(new_player)
    return jsonify(PlayerErrorDto(message=f"Player by id {p_id} created successfully", body=new_player)), 201


@player_blueprint.route("/update/<int:player_id>", methods=["PUT"])
def update_existing_player(player_id):
    player_data = request.get_json()
    required_fields = ["player_name", "team", "position", "seasons", "points", "games", "two_percent", "three_percent",
                       "atr", "ppg_ratio"]
    if not player_data or not all(key in player_data for key in required_fields):
        return jsonify(PlayerErrorDto(error="Missing player data")), 400

    existing_player = find_player_by_id(player_id)
    if not existing_player:
        return jsonify(PlayerErrorDto(error="Player not found")), 404

    updated_player = PlayerStats(
        player_id=player_id,
        player_name=player_data["player_name"],
        team=player_data["team"],
        position=player_data["position"],
        seasons=player_data["seasons"],
        points=player_data["points"],
        games=player_data["games"],
        two_percent=player_data["two_percent"],
        three_percent=player_data["three_percent"],
        atr=player_data["atr"],
        ppg_ratio=player_data["ppg_ratio"]
    )
    update_player(player_id, updated_player)
    return jsonify(PlayerErrorDto(message="Player updated successfully", body=updated_player)), 200


@player_blueprint.route("/delete/<int:player_id>", methods=["DELETE"])
def delete_existing_player(player_id):
    existing_player = find_player_by_id(player_id)
    if not existing_player:
        return jsonify(PlayerErrorDto(error="Player not found")), 404

    delete_player(player_id)
    return jsonify(PlayerErrorDto(message="Player deleted successfully")), 200
