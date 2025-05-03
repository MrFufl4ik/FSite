from mcrcon import MCRcon

from log_manager import log_info, LogInfoType


class FRcon:
    def __init__(self, ip : str, port : int, password: str):
        self._rcon : MCRcon | None = None
        try:
            self._rcon = MCRcon(ip, password, port=port)
            self._rcon.connect()
            log_info("Connection enabled!", LogInfoType.Correct)
        except Exception as E:
            print(E)
            log_info("Connection closed", LogInfoType.Error)

    def __del__(self):
        self._rcon.disconnect()

    def send_command(self, minecraft_command : str) -> bool:
        try:
            response_data = self._rcon.command(minecraft_command)
            response_data = response_data.replace("\n", "")
            log_info(response_data, LogInfoType.ResponseStatus)
            log_info("Minecraft command executed!", LogInfoType.Correct)
            return True
        except Exception as E:
            print(E)
            log_info("Minecraft command error :(", LogInfoType.Error)
            return False
