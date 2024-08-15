# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-pytest-helper
# FileName:     base_test.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/07/31
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import pytest
from mixiu_pytest_helper.annotation import logger
from mixiu_pytest_helper.context import lock_client
from airtest_helper.core import DeviceProxy, DeviceApi
from mixiu_pytest_helper.repository import MiddlewareRepository
from mixiu_app_helper.api.page.popup.gift import UiDailyCheckInApi
from mixiu_pytest_helper.conftest import get_idle_device, get_phone_device_lock_key


class SetupClass(object):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def init_setup(cls):
        logger.info("开始初始化自动化测试环境...")


class UiDataSetupClass(SetupClass):
    test_data: dict = dict()
    config_namespace = "test-data-ui"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def data_setup(cls, request: pytest.FixtureRequest, init_setup: pytest.Function):
        request.cls.test_data = MiddlewareRepository.get_test_datas(namespace=cls.config_namespace)
        logger.info("step1: 获取apollo配置的UI测试【预期数据】成功")


class DeviceSetupClass(UiDataSetupClass):
    device: DeviceProxy = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def device_setup(cls, data_setup: pytest.Function):
        # 此处的 setup 只会在每个测试类开始时调用一次
        cls.device = get_idle_device(redis_api=lock_client)
        if cls.device is None:
            logger.error("step2: 绑定移动终端设备失败，当前没有空闲设备，或者网络连接不正常")
        else:
            logger.info("step2: 绑定移动终端成功---> {}".format(cls.device.device_id))
        yield
        if cls.device:
            lock_key = get_phone_device_lock_key(device_ip=cls.device.device_id)
            lock_client.set_redis_data(key=lock_key, value="idle", ex=86400)


class AppSetupClass(DeviceSetupClass):
    app_name: str = 'null'
    device_api: DeviceApi = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def app_setup(cls, device_setup: pytest.Function):
        cls.device_api = DeviceApi(device=cls.device)
        cls.app_name = cls.test_data.get('app_name')
        # logger.info("开始唤醒设备")
        # device_api.wake()  真机的可能处于息屏状态，因此需要唤醒，模拟机的话，可以忽略此步骤
        logger.info("step3: 开始启动APP---> {}".format(cls.app_name))
        cls.device_api.restart_app(app_name=cls.app_name)


class BeforeUiTest(AppSetupClass):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def before_test_setup(cls, app_setup: pytest.Function):
        popui_api = UiDailyCheckInApi(device=cls.device)
        signup_button = popui_api.get_signup_button()
        # 可能存在签到的弹窗
        if signup_button:
            logger.info("step4*: 检测到【每日签到】弹窗，关闭弹窗并退出直播室")
            popui_api.touch_signup_button()
            logger.info("step4.1*: 已签到")
            popui_api.touch_signup_submit_button()
            popui_api.touch_live_leave_enter()
            popui_api.touch_close_room_button()
            logger.info("step4.2*: 已退出直播间")


class ApiSetupClass(SetupClass):
    domain: str = None
    protocol: str = None
    login_user_uuid: int = None

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def domain_setup(cls, request: pytest.FixtureRequest, init_setup: pytest.Function):
        request.cls.domain = MiddlewareRepository.get_api_domain()
        request.cls.protocol = MiddlewareRepository.get_api_protocol()
        logger.info("step1: 获取待测试环境: <{}>".format(request.cls.domain))
        request.cls.api_uuid = MiddlewareRepository.get_api_user_uuid()
        api_token = MiddlewareRepository.get_login_user_token(uuid=request.cls.api_uuid)
        request.cls.api_token = api_token.replace('"', '') if api_token else api_token
        logger.info("step2: 获取待测试用户uuid: <{}>，token: <{}>".format(request.cls.api_uuid, request.cls.api_token))


class AndroidApiCommonSetupClass(ApiSetupClass):
    test_data_common: dict = dict()
    common_namespace = "test-data-api-android-common"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def common_data_setup(cls, request: pytest.FixtureRequest, domain_setup: pytest.Function):
        request.cls.test_data_common = MiddlewareRepository.get_test_datas(namespace=cls.common_namespace)
        logger.info("step3: 获取apollo配置的Android API common参数完成")


class IOSApiCommonSetupClass(ApiSetupClass):
    test_data_common: dict = dict()
    common_namespace = "test-data-api-ios-common"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def common_data_setup(cls, request: pytest.FixtureRequest, domain_setup: pytest.Function):
        request.cls.test_data_common = MiddlewareRepository.get_test_datas(namespace=cls.common_namespace)
        logger.info("step3: 获取apollo配置的iOS API common参数完成")


class AndroidApiDataSetupClass(AndroidApiCommonSetupClass):
    test_data_api: dict = dict()
    api_namespace = "test-data-api-android"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def http_api_setup(cls, request: pytest.FixtureRequest, common_data_setup: pytest.Function):
        request.cls.test_data_api = MiddlewareRepository.get_test_datas(namespace=cls.api_namespace)
        logger.info("step4: 获取apollo配置的Android API请求参数完成")


class IOSApiDataSetupClass(AndroidApiCommonSetupClass):
    test_data_api: dict = dict()
    api_namespace = "test-data-api-ios"

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def http_api_setup(cls, request: pytest.FixtureRequest, common_data_setup: pytest.Function):
        request.cls.test_data_api = MiddlewareRepository.get_test_datas(namespace=cls.api_namespace)
        logger.info("step4: 获取apollo配置的iOS API请求参数完成")


class BeforeAndroidApiTest(AndroidApiDataSetupClass):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def before_test_setup(cls, request: pytest.FixtureRequest, http_api_setup: pytest.Function):
        pass


class BeforeIOSApiTest(AndroidApiDataSetupClass):

    @classmethod
    @pytest.fixture(scope="class", autouse=True)
    def before_test_setup(cls, request: pytest.FixtureRequest, http_api_setup: pytest.Function):
        pass
