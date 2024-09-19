from repository.team_repository import create_team, get_team_id, get_players_by_team_id1, get_team_by_id1
from repository.team_player_repository import create_player_fantasy, insert_players_if_valid
from repository.player_repository import get_player_by_id_name
from dto.Error_dto import PlayerFantasyErrorDto, TeamErrorDto
from flask import Blueprint, jsonify, request
from service.team_service import get_players_by_position, delete_team_service, get_team_details_service

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
        player = get_player_by_id_name(player_name)
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

    list(map(lambda player: create_player_fantasy(team_id, player), players))

    return jsonify(TeamErrorDto(message=f"Team and players added successfully, team_id: {team_id}")), 201


@team_blueprint.route("/players", methods=["GET"])
def get_players_by_position_controller():
    position = request.args.get("position")
    season = request.args.get("season")

    if not position:
        return jsonify({"error": "Position is required"}), 400
    players = get_players_by_position(position, season)

    if not players:
        return jsonify({"error": "No players found for the given position and season"}), 404

    return jsonify(players), 200


@team_blueprint.route("/<int:team_id>", methods=["DELETE"])
def delete_team_controller(team_id):
    deleted_team_id = delete_team_service(team_id)
    print(deleted_team_id)
    if not deleted_team_id:
        return jsonify({"error": f"Team with ID {team_id} not found"}), 404

    return jsonify({"message": f"Team {team_id} and its references deleted successfully"}), 200



@team_blueprint.route("/details/<int:team_id>", methods=["GET"])
def get_team_details_controller(team_id):
    team_details = get_team_details_service(team_id)
    print(team_details)
    if not team_details:
        return jsonify({"error": f"Team with ID {team_id} not found"}), 404

    return jsonify({
        "team_name": team_details["team"]["team_name"],
        "players": team_details["players"]
    }), 200



@team_blueprint.route("/compare", methods=["GET"])
def compare_teams():
    team_ids = [team_id for team_id in request.args.values()]

    if len(team_ids) < 2:
        return jsonify(TeamErrorDto(error="You must compare at least 2 teams")), 400

    teams_data = []

    for team_id in team_ids:

        team = get_team_by_id1(team_id)
        if not team:
            return jsonify(TeamErrorDto(error=f"Team with ID {team_id} not found")), 404

        players = get_players_by_team_id1(team_id)

        if not players:
            return jsonify(TeamErrorDto(error=f"No players found for team ID {team_id}")), 404

        total_points = sum(player['points'] for player in players)
        two_percent_avg = sum(player['two_percent'] for player in players) / len(players)
        three_percent_avg = sum(player['three_percent'] for player in players) / len(players)
        atr_avg = sum(player['atr'] for player in players) / len(players)
        ppg_ratio_avg = sum(player['ppg_ratio'] for player in players) / len(players)

        teams_data.append({
            "team": team["team_name"],
            "points": total_points,
            "twoPercent": two_percent_avg,
            "threePercent": three_percent_avg,
            "ATR": atr_avg,
            "PPG Ratio": ppg_ratio_avg
        })

    sorted_teams = sorted(teams_data, key=lambda t: t["PPG Ratio"], reverse=True)

    return jsonify(sorted_teams), 200

