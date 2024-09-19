from flask import Flask

from controllers.player_controller import player_blueprint
from controllers.team_fantasy_controller import team_blueprint

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(player_blueprint, url_prefix="/api/players")
    app.register_blueprint(team_blueprint, url_prefix="/api/teams")
    app.run(debug=True)




#  global claculate ppg SOS