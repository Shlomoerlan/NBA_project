from flask import Blueprint, jsonify, request
from repository.team_repository import create_team, get_team_id
from repository.team_player_repository import create_player_fantasy
from repository.player_repository import get_player_by_name

team_blueprint = Blueprint("team", __name__)


@team_blueprint.route("/create_team", methods=["POST"])
def create_team_with_players():
    data = request.get_json()

    if not data or "name" not in data or "players" not in data or len(data["players"]) != 5:
        return jsonify({"error": "Team must have exactly 5 players"}), 400

    team_name = data["name"]
    player_names = data["players"]

    create_team(team_name)
    team_id = get_team_id(team_name)

    if not team_id:
        return jsonify({"error": "Failed to create team"}), 500

    for player_name in player_names:
        player = get_player_by_name(player_name)

        if not player:
            return jsonify({"error": f"Player {player_name} not found in any season"}), 404

        create_player_fantasy(team_id, player)

    return jsonify({"message": "Team and players added successfully", "team_id": team_id}), 201
