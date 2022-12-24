from pathlib import Path
from commons import Commons
from log4py import Log4py


class DIContainer:
    def __init__(self):
        # プロジェクトのパス
        self.project_folder_path = Path(__file__).parent
        # 設定値フォルダのパス
        self.conf_folder_path = self.project_folder_path / "config"

        # ---------------------------------------------------------------
        # 設定ファイル
        # ---------------------------------------------------------------
        config_file_path = self.conf_folder_path / "config.yml"
        self.conf = Commons.load_yaml(config_file_path)

        # ---------------------------------------------------------------
        # ログ
        # ---------------------------------------------------------------
        self.logger = Log4py(self.log_folder_path, self.msg_file_path)

    @property
    def log_folder_path(self):
        return self.project_folder_path / self.conf["LOG_FOLDER"]

    @property
    def msg_file_path(self):
        return self.conf_folder_path / self.conf["LOG_MSG_FILE"]
