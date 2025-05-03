from flask import Flask, render_template, request, jsonify
from mcrcon import MCRcon

import config_manager
from log_manager import log_info, LogInfoType
from server_manager import MinecraftServerManager

minecraft_server_manager : MinecraftServerManager

app = Flask(__name__)

@app.route('/rcon')
def request_rcon():
    return render_template("rcon.html")

@app.route('/rcon_send_cmd', methods=['POST'])
def request_rcon_send_command():
    data = request.get_json()
    server_index: int = int(data.get('server_index', 0))
    server = minecraft_server_manager.get_server(server_index)
    rcon_command : str = data.get('rcon_cmd', None)
    if rcon_command == "":
        log_info("User not defined the minecraft command!", LogInfoType.Error)
        return jsonify({'status': "command_not_defined"})
    log_info(f"Try to run minecraft command: {rcon_command}")
    server.rcon.send_command(rcon_command)
    return jsonify({'status': "ok"})

@app.route('/is_server_defined', methods=['POST'])
def request_server_defined():
    data = request.get_json()
    server_index: int = int(data.get('server_index', 0))
    server = minecraft_server_manager.get_server(server_index)
    if server is None:
        return jsonify({'status': False})
    return jsonify({'status': True})

@app.route('/get_server_title_name', methods=['POST'])
def get_server_title_namep():
    data = request.get_json()
    server_index: int = int(data.get('server_index', 0))
    server = minecraft_server_manager.get_server(server_index)

    return jsonify({'title_name': server.server_name})


@app.route('/get-logs')
def request_get_logs():
    data : dict = request.args
    server_index : int = int(data.get('server_index', 0))

    server = minecraft_server_manager.get_server(server_index)

    last_position = int(request.args.get('last_position', 0))
    new_logs, new_position = server.log_manager.get_logs(last_position)
    return jsonify({
        'logs': new_logs,
        'new_position': new_position
    })

with app.app_context():
    minecraft_server_manager = config_manager.init_server_manager()

if __name__ == '__main__':
    app.run()
