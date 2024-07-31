# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     dir.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import os
import shutil
from airtest_helper.dir import get_project_path as get_exec_path, is_dir, join_path, is_file, is_exists


def find_configuration_path(current_path):
    # 构造配置目录的完整路径
    config_path = join_path([current_path, "configuration"])

    if is_dir(file_path=str(config_path)):
        return current_path

    parent_path = os.path.dirname(current_path)

    # 如果到达根目录则返回 None
    if parent_path == current_path:
        return None

    return find_configuration_path(parent_path)


def get_project_path():
    # 执行文件所在的路径
    exec_path = get_exec_path()
    return find_configuration_path(exec_path) or exec_path


def get_package_path() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def copy_file(src_file_path: str, dst_path: str) -> None:
    if is_file(file_path=src_file_path) is True:
        file_name = os.path.basename(src_file_path)
        dst_file_path = str(join_path([dst_path, file_name]))
        if is_exists(file_name=dst_file_path) is False:
            # 临时将 pytest.ini 复制到当前目录
            shutil.copy(src_file_path, dst_file_path)
