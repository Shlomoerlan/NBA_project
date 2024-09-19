from flask import Blueprint, jsonify, request
from repository.team_repository import create_team, get_team_id
from repository.team_player_repository import create_player_fantasy, insert_players_if_valid
from repository.player_repository import get_player_by_name
from dto.Error_dto import PlayerFantasyErrorDto, TeamErrorDto

team_blueprint = Blueprint("team", __name__)


@team_blueprint.route("/create_team", methods=["POST"])
def create_team_with_players():
    data = request.get_json()

    if not data or "name" not in data or "players" not in data or len(data["players"]) != 5:
        return jsonify(TeamErrorDto(error="Team must have exactly 5 players")), 400

    team_name = data["name"]
    player_names = data["players"]

    players = []

    for player_name in player_names:
        player = get_player_by_name(player_name)
        if not player:
            return jsonify(PlayerFantasyErrorDto(error=f"Player {player_name} not found in any season")), 404
        players.append(player)

    validation_result = insert_players_if_valid(players)
    if "error" in validation_result:
        return jsonify(validation_result), 400

    create_team(team_name)
    team_id = get_team_id(team_name)

    if not team_id:
        return jsonify(TeamErrorDto(error="Failed to create team")), 500

    for player in players:
        create_player_fantasy(team_id, player)

    return jsonify(TeamErrorDto(message=f"Team and players added successfully, team_id: {team_id}")), 201
