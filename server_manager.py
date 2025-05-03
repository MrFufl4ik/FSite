from minecraft_log_manager import MinecraftLogManager
from rcon_manager import FRcon


class MinecraftServer:
    def __init__(
            self,
            server_name : str,
            server_rcon_ip : str,
            server_rcon_port : int,
            server_rcon_password : str,
            server_log_file_path : str
    ):
        self.server_name : str = server_name
        self.server_rcon_ip : str = server_rcon_ip
        self.server_rcon_port : int = server_rcon_port
        self.server_rcon_password : str = server_rcon_password
        self.server_log_file_path : str = server_log_file_path

        self.rcon : FRcon = FRcon(server_rcon_ip, server_rcon_port, server_rcon_password)
        self.log_manager = MinecraftLogManager(server_log_file_path)


class MinecraftServerManager:
    def __init__(self):
         self._servers : list = []

    def add_server(self, server : MinecraftServer):
        self._servers.append(server)
    def delete_server(self, index : int):
        self._servers.remove(index)
    def get_server(self, index : int) -> MinecraftServer | None:
        server : MinecraftServer | None = None
        try:
            server = self._servers[index]
            return server
        except:
            return None
    def get_servers_length(self) -> int:
        return len(self._servers)
