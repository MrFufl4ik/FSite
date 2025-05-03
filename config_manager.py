import json
from itertools import count

import consts
import log_manager
from log_manager import log_info, LogInfoType
from server_manager import MinecraftServerManager, MinecraftServer


def get_json(file_path : str) -> dict | None:
    try:
        with open(file_path, 'r') as f: return json.load(f)
    except: return None


def get_servers_data() -> list | None:
    config_data: dict = get_json(consts.CONFIG_FILE)
    servers_data: list | None = config_data.get("minecraft_servers", None)
    return servers_data

def init_server_manager() -> MinecraftServerManager:
    servers_data = get_servers_data()
    if servers_data is None:
        log_info("Dont have the defined servers list... exit", LogInfoType.Error)
        exit(1)

    minecraft_server_manager = MinecraftServerManager()

    for i in range(0, len(servers_data)):
        _server : dict = servers_data[i]
        server_name : str | None = _server.get("server_name", None)
        server_rcon_ip : str | None = _server.get("server_rcon_ip", None)
        server_rcon_port : int | None = _server.get("server_rcon_port", None)
        server_rcon_password : str | None = _server.get("server_rcon_password", None)
        server_log_file_path : str | None = _server.get("server_log_file_path", None)
        if (server_name is None or
            server_rcon_ip is None or
            server_rcon_port is None or
            server_rcon_password is None or
            server_log_file_path is None
        ): log_info(f"Minecraft server: №{i}, not full defined!", LogInfoType.Error); continue

        minecraft_server_manager.add_server(
            MinecraftServer(server_name, server_rcon_ip, server_rcon_port,server_rcon_password, server_log_file_path)
        )
        log_info(f"Minecraft server: №{i}, full defined, and created!", LogInfoType.Correct)

    if minecraft_server_manager.get_servers_length() == 0:
        log_info("Dont have the servers list... exit", LogInfoType.Error)
        exit(1)

    return minecraft_server_manager