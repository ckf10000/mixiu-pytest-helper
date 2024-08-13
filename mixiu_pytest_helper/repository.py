# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     repository.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import typing as t

from apollo_proxy.client import ApolloClient
from mixiu_pytest_helper.context import apollo, auth_client
from mixiu_pytest_helper.infrastructure import RedisClientManager


class MiddlewareRepository(object):

    @classmethod
    def get_devices(cls, apollo: ApolloClient = apollo, namespace: str = "application") -> list:
        return apollo.get_value(key="device_ids", namespace=namespace) or list()

    @classmethod
    def get_api_user_uuid(cls, apollo: ApolloClient = apollo, namespace: str = "test-data-api") -> int:
        user_uuid = apollo.get_value(key="user_uuid", namespace=namespace)
        return int(user_uuid) if isinstance(user_uuid, str) and user_uuid.isdigit() else 0

    @classmethod
    def get_test_data(cls, key: str, namespace: str, apollo: ApolloClient = apollo) -> t.Any:
        return apollo.get_value(key=key, namespace=namespace)

    @classmethod
    def get_test_datas(cls, namespace: str, apollo: ApolloClient = apollo) -> dict:
        test_datas = apollo.get_all_values(namespace=namespace)
        return test_datas if isinstance(test_datas, dict) else dict()

    @classmethod
    def get_login_user_token(cls, uuid: int, redis: RedisClientManager = auth_client) -> str:
        return redis.get_redis_data(key="POPO:USER:TOKEN:CACHE::{}".format(uuid))
