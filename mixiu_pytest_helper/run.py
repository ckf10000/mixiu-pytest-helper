# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     run.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import sys
import pytest
import logging.config
from distributed_logging.parse_yaml import ProjectConfig
from airtest_helper.dir import join_path, create_directory
from mixiu_pytest_helper.dir import get_project_path, copy_file, get_package_path


def run_tests(script_path: str = None):
    project_path = get_project_path()
    package_path = get_package_path()
    config_path = str(join_path([project_path, "configuration"]))
    config_template = str(join_path([package_path, "pytest.ini"]))
    logging_template = str(join_path([package_path, "logging.yaml"]))
    copy_file(src_file_path=config_template, dst_path=project_path)
    create_directory(dir_path=config_path)
    copy_file(src_file_path=logging_template, dst_path=config_path)
    config = ProjectConfig(project_home=get_project_path()).get_object()
    logging_plus = getattr(config, "logging")
    logging.config.dictConfig(logging_plus)
    allure_dir = join_path([project_path, "allure-results"])
    pytest_args = ['--strict-markers', '--tb=short', '-v', '-ra', '-q', '-s', '--alluredir={}'.format(allure_dir)]
    if script_path is not None:
        if script_path == "__main__":
            script_path = sys.argv[0]
        pytest_args.append(script_path)
    pytest.main(pytest_args)
