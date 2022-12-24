import re
import yaml
import shutil
from pathlib import Path
import json
import os
import glob
from datetime import datetime as dt

class Commons:
    '''
    共通機能
    '''
    @classmethod
    def load_yaml(cls, path, encord='utf-8'):
        '''
        yamlファイルの読み込み
        '''
        contents = None
        try:
            with open(file=path, mode='r', encoding=encord) as file:
                contents = yaml.safe_load(file)
                return contents
        except Exception as e:
            raise

    @classmethod
    def del_file_inhibited_character(cls, target_str: str):
        '''
        引数.処理対象の文字列(target_str)から、フォルダ・ファイルに使用できない文字(\⁄:*?"><|)を除去する。
        string以外が渡された場合は、何もしない
        '''
        return re.sub(r'[\\/:*?"><|]+', '', target_str) if type(target_str) is str else target_str

    @classmethod
    def zip_compression(cls, src_path: str, dst_path: str):
        '''
        zipを生成する

        Parameters
        ----------
        src_path：圧縮対象のパス
        dst_path：圧縮後のパス
        '''
        try:
            shutil.make_archive(dst_path, 'zip', root_dir=src_path)
        except Exception as e:
            raise

    @classmethod
    def trim_str(self, prm: str):
        '''
        文字列の前後空白をトリム
        ・string以外が渡された場合、何もしない

        Returns
        ----------
        prm: str/None :トリム結果が''の場合、Noneを返却
        '''
        return prm.strip() if type(prm) is str else prm

    @classmethod
    def is_empty_xl_cell(cls, cell) -> bool:
        '''
        xlsxシートのセル値empty判定

        Returns
        ----------
        boolean: Null/空白の場合、Trueを返却
        '''
        return cell.value is None or not str(cell.value).strip()

    @classmethod
    def alpha_to_fullwidth(cls, word) -> str:
        '''
        半角英字を全角英字に変換する
        '''
        HAN_UPPER = re.compile(u"[A-Z]")
        HAN_LOWER = re.compile(u"[a-z]")

        word = HAN_UPPER.sub(lambda m: chr(
            ord("Ａ") + ord(m.group(0)) - ord("A")), word)
        word = HAN_LOWER.sub(lambda m: chr(
            ord("ａ") + ord(m.group(0)) - ord("a")), word)
        return word

    @classmethod
    def unique_list(cls, src_list):
        unique = []
        duplicate = []
        for element in src_list:
            if not element in unique:
                unique.append(element)
            elif not element in duplicate:
                duplicate.append(element)

        return unique, duplicate

    @classmethod
    def load_json_file(cls, file_path, encord='utf-8'):
        contents = None
        try:
            with open(file=file_path, mode='r', encoding=encord) as file:
                contents = json.load(file)
                if not contents:
                    raise Exception
        except Exception:
            raise Exception

        return contents

    @classmethod
    def get_latest_file_name(cls, dir_path):
        result = None
        
        dir_path = dir_path + '.\\'
        if len(os.listdir(dir_path)) == 0:
            return result
        result =  max(
            [dir_path + f for f in os.listdir(dir_path)],
            key=os.path.getctime,
        )

        return result
    @classmethod
    def get_today_file_name(cls, dir_path):
        result = None
        
        file_list = glob.glob(dir_path + "\\*")

        file_today = [file_path for file_path in file_list if dt.today().strftime("%Y%m%d") in str(file_path)]
        
        if len(file_today) == 0:
            raise
        elif len(file_today) > 1:
            raise
        else:
            result =  str(file_today[0])

        return result
