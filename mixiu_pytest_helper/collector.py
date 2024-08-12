# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     collector.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/03
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import json
import importlib
import subprocess

from mixiu_pytest_helper.dir import get_project_path, delete_file, init_dir
from mixiu_pytest_helper.log import logger


def collect_marks(collect_dir: str) -> list:
    if collect_dir is None:
        collect_dir = get_project_path()
    init_dir(project_path=collect_dir)
    collect_marks = list()
    collect_marks_file = 'collect_marks.json'
    # 使用 subprocess 运行 pytest
    result = subprocess.run(
        ['pytest', '--disable-warnings', '--collect-only', '--verbose', '--json-report',
         '--json-report-file={}'.format(collect_marks_file),
         collect_dir],
        capture_output=True,
        text=True
    )

    # 检查 pytest 是否成功执行
    if result.returncode != 0:
        logger.error(result.stderr)
        return collect_marks

    # 解析 pytest 输出的 JSON 报告
    with open(collect_marks_file, 'r') as f:
        report = json.load(f)

    delete_file(file_path=collect_marks_file)

    for x in report.get("collectors"):
        for y in x.get("result"):
            if y.get("type") == "Function":
                node_id = y.get('nodeid')
                marks = get_decorators(nodeid=node_id)
                if marks:
                    node_id_slice = node_id.split("::")
                    module_name = node_id_slice[0][:-3].replace('/', '.')
                    # module_name = importlib.import_module(module_path.replace('/', '.'))
                    class_name = node_id_slice[1] if len(node_id_slice) == 3 else None
                    function_name = node_id_slice[-1]
                    marks.update(module_name=module_name, class_name=class_name, function_name=function_name)
                    collect_marks.append(marks)
    from pprint import pprint
    pprint(collect_marks)
    return collect_marks


def get_decorators(nodeid: str) -> dict:
    """获取函数的所有装饰器"""
    marks = dict()
    # 分解字符串
    parts = nodeid.split('::')
    # 导入模块
    module = importlib.import_module(parts[0][:-3].replace('/', '.'))
    if len(parts) == 3:
        # 获取类
        cls = getattr(module, parts[1], None)
        func = getattr(cls, parts[2], None) if cls is not None else None
    else:
        cls = None
        func = getattr(module, parts[1], None)
    if func is not None and callable(func):
        if hasattr(func, 'pytestmark'):
            # 获取当前函数的pytestmark属性（如果有）
            pytestmark = getattr(func, 'pytestmark') or list()
            for mark in pytestmark:
                args = getattr(mark, 'args')
                marks[getattr(mark, 'name')] = args[0] if args and isinstance(args, tuple) else None
    return marks
