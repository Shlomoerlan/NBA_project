from repository.player_repository import create_players_table, insert_players_to_db
from api.players_api import fetch_player_data


api_url2024 = "http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season=2024&&pageSize=1000"
api_url2023 = "http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season=2023&&pageSize=1000"
api_url2022 = "http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season=2022&&pageSize=1000"

# players_list2024 = fetch_player_data(api_url2024)
# players_list2023 = fetch_player_data(api_url2023)
# players_list2022 = fetch_player_data(api_url2022)
#
# create_players_table()
# insert_players_to_db(players_list2022)
# insert_players_to_db(players_list2023)
# insert_players_to_db(players_list2024)