import types
from typing import Any, Union, Callable, Optional, NamedTuple

from _os_log import lib
import loguru
import wrapt

OS_LOG_LEVELS = {
    "DEFAULT": lib.OS_LOG_TYPE_DEFAULT, "TRACE": lib.OS_LOG_TYPE_DEFAULT,
    "INFO": lib.OS_LOG_TYPE_INFO,
    "DEBUG": lib.OS_LOG_TYPE_DEBUG,
    "ERROR": lib.OS_LOG_TYPE_ERROR,
    "FAULT": lib.OS_LOG_TYPE_FAULT, "CRITICAL": lib.OS_LOG_TYPE_FAULT
}


class Sink:
    def __init__(self, log_obj=lib.OS_LOG_DEFAULT):
        self.log_obj = log_obj

    @classmethod
    def create(cls, subsystem: str, category: str):
        return cls(lib.os_log_create(subsystem.encode('utf-8'),
                                     category.encode('utf-8')))

    def write(self, message):
        record = message.record
        lib._os_log_with_type(self.log_obj, OS_LOG_LEVELS[record["level"].name],
                              message.encode('utf-8'))

    def stop(self):
        if self.log_obj is not lib.OS_LOG_DEFAULT:
            lib.os_release(self.log_obj)


DEFAULT_FORMAT = '{name}:{function}:{line} - {message}'


class LoggerMain(wrapt.ObjectProxy):
    def __init__(self, subsystem:str='', category: str=''):
        super().__init__(loguru.logger)
        sink = Sink.create(subsystem, category) if subsystem or category else Sink()
        self.__wrapped__.add(sink, format=DEFAULT_FORMAT)


class Handler(NamedTuple):
    sink: Any
    level: Union[int, str, None] = 'DEBUG'
    format: Union[str, Callable, None] = DEFAULT_FORMAT
    filter: Union[Callable, str, dict, None] = None
    colorize: Optional[bool] = None
    serialize: Optional[bool] = False
    backtrace: Optional[bool] = True
    diagnose: Optional[bool] = True
    enqueue: Optional[bool] = False
    catch: Optional[bool] = True


class OperatorLogger(wrapt.ObjectProxy):
    def __init__(self, wrapped=loguru.logger):
        super().__init__(wrapped)

    def __iadd__(self, handler: Handler):
        self.add(**handler._asdict())
        return self

    def __isub__(self, handler_id: int):
        self.remove(handler_id)
        return self


class OpLoggerMain(OperatorLogger):
    def __init__(self, subsystem:str='', category: str=''):
        super().__init__(OperatorLogger())
        handler = Handler(Sink.create(subsystem, category) if subsystem or category else Sink())
        self.__wrapped__ += handler


if __name__ == '__main__':
    import fire
    fire.Fire(LoggerMain)

