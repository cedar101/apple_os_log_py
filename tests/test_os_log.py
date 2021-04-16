import json
import time

from loguru import logger
import pytest

from os_log import __version__
from os_log.loguru import Sink, Handler, OperatorLogger, DEFAULT_FORMAT
from _os_log import lib


def test_version():
    assert __version__ == "0.1.0"


def test_constants():
    assert lib.OS_LOG_TYPE_DEFAULT == 0x00
    assert lib.OS_LOG_TYPE_INFO == 0x01
    assert lib.OS_LOG_TYPE_DEBUG == 0x02
    assert lib.OS_LOG_TYPE_ERROR == 0x10
    assert lib.OS_LOG_TYPE_FAULT == 0x11


@pytest.fixture(scope="session", params=[(), ("org.python.macos", "Development")])
def handler(request):
    if not request.param:
        return Handler(Sink())
    subsystem, category = request.param
    return Handler(Sink.create(subsystem, category))


@pytest.fixture(scope="session")
def os_logger(handler):
    operator_logger = OperatorLogger(logger)
    operator_logger += handler
    yield operator_logger
    operator_logger -= next(reversed(operator_logger._core.handlers))


def test_first_line():
    assert 'Filtering' in input()

@pytest.mark.parametrize("level", "DEBUG INFO ERROR CRITICAL".split())
@pytest.mark.parametrize("message",
                         [
                             "This message should go to the Apple OSLog(unified logging system)",
                             "So should this",
                             "And non-ASCII stuff, too, like Øresund and Malmö",
                             "심각한 오류가 발생했습니다!"
                         ])
def test_handler(os_logger, level, message):
    os_logger.log(level, message)
    log_dict = json.loads(input())
    assert message in log_dict['eventMessage']
    os_log_level = ('Fault' if level == 'CRITICAL' else level.capitalize())
    assert os_log_level in log_dict['messageType']
