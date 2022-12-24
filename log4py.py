from logging import getLogger, StreamHandler, Formatter, FileHandler, DEBUG, ERROR, WARNING, INFO
import datetime
import pathlib
import sys
import inspect
from commons import Commons

class Log4py:
    """ログメッセージクラス
    ログ出力を制御する

    Attributes
    ----------
    LOG_LEVEL (dictionary) : ログレベルの
    """

    # ログレベル
    LOG_LEVEL = {'E': ERROR, 'W': WARNING, 'I': INFO, 'D': DEBUG}

    # メッセージを格納するリスト
    err_msg_list = []
    warn_msg_list = []

    def __init__(self, log_folder_path, msg_file_path):
        """初期化

        Args:
            log_folder_path (str): ログ出力先フォルダパス
            msg_file_path (str): メッセージ文言を定義したyamlファイルのパス
        """
        # ログセットアップ
        self._logger = self._setup_logger(log_folder_path)
        # メッセージ定義ファイル読み込み
        self._messages = Commons.load_yaml(msg_file_path)

        # logメッセージクリア
        self.clear_msg_list()
        self.clear_warn_msg_list()

    def msg(self, id, *args):
        """メッセージ生成
         メッセージIDに紐づく文言にパラメータを埋め込み、ログメッセージを生成する
        Args:
            id (str): メッセージID
            *args (str) : メッセージに埋め込むパラメータ

        Returns:
            str : メッセージ文言
        """
        # Noneは空へ変更
        args = [arg or '' for arg in args]
        msg = self._messages[id]
        msg = msg.format(*args)

        return msg

    def debug(self, msg):
        self._logger.log(DEBUG, msg)

    def log(self, id, *args):
        self.__log(id, 2, *args)

    def log_exception(self, err):
        exception_name = err.__class__.__name__
        exception_msg = self.exception_msg(err)
        self.__log('E9000', 2, exception_name, exception_msg)

    def clear_msg_list(self):
        self.err_msg_list = []

    def clear_warn_msg_list(self):
        self.warn_msg_list = []

    def exception_msg(self, err):
        """[summary]

        Args:
            err (Exception): Exception

        Returns:
            str: Exceptionから取得したメッセージ
        """
        tb = sys.exc_info()[2]
        return err.with_traceback(tb)

    def _setup_logger(self, log_folder_path):
        """ログセットアップ

        Args:
            log_folder_path (str): ログ出力先フォルダパス

        Returns:
            [type]: [description]
        """
        # ログファイル名（yyyy-mm-dd）
        dt = datetime.date.today().strftime('%Y-%m-%d')
        # ログ出力ファイルパス
        logfile_path = pathlib.Path(log_folder_path) / '{0}.log'.format(dt)
        # ログメッセージフォーマット
        log_format = '%(asctime)s %(levelname)s %(message)s'

        logger = getLogger(__name__)
        logger.setLevel(DEBUG)
        if not logger.hasHandlers():
            formatter = Formatter(log_format)

            # 出力先＝ストリーム
            stream_handler = StreamHandler()
            stream_handler.setLevel(DEBUG)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

            # 出力先ファイル
            file_handler = FileHandler(logfile_path, encoding='utf-8')
            file_handler.setLevel(DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def __log(self, id, stack_level, *args):
        """ログ出力

        Args:
            id (str): メッセージID
            *args (str) : メッセージに埋め込むパラメータ
        """
        inspect_stack = inspect.stack()[stack_level]
        filename = pathlib.Path(inspect_stack.filename).stem
        function = inspect_stack.function
        lineno = inspect_stack.lineno
        caller = '{} ({}:{}:{}) '.format(id, filename, function, lineno)

        msg = self.msg(id, *args)

        self._logger.log(self.LOG_LEVEL[id[0]], caller + msg)

    def has_error_message(self):
        return 0 < len(self.err_msg_list)

    
