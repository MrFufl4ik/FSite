
class MinecraftLogManager:
    def __init__(self, log_file_path : str):
        self._log_file_path: str = log_file_path

    def get_logs(self, last_position=0):
        log_file_path = self._log_file_path
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(last_position)
            new_logs = f.readlines()
            new_position = f.tell()
        return new_logs, new_position