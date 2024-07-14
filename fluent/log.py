# -*- coding: utf-8 -*-
"""logger处理， 设置logger配置

只有set_logger提供给外部使用

Todo:
    将rotate maxBytes改造成配置文件
"""
import logging
from fluent import _global
get_logger = logging.getLogger

_LOG = None


def set_logger(conf):
    """设置日志, 将内置日志logging.getLogger替换成Logger

    Examples:

        >>> import logging
        >>> logging.info('')
    """
    global _LOG
    logging_conf = conf.get("logging")
    if logging_conf.get('fluent_log', True):
        _LOG = Logger(logging_conf)
        if _LOG.rotate:
            logging.getLogger = _LOG.get_rotating_logger
            _LOG.get_rotating_logger('fluent')
        else:
            logging.getLogger = _LOG.get_logger
            _LOG.get_logger('fluent')


class Logger():
    """日志配置

    支持定制化配置format, level, fileHandler, rotateFileHandler

    Attributes:
        conf: 日志配置
        logging_conf: 用于设置BasicConf的配置

    Methods:
        set_level: 设置日志级别
        set_format: 设置日志format
        set_file: 设置文件， 如果handler是fileHandler或者rotateFileHandler
    """
    DEFAULT_LEVEL = logging.INFO
    DEFAULT_FORMAT = """%(asctime)s - %(processName)s - %(threadName)s - %(filename)s - %(funcName)s - [line:%(lineno)d] - %(levelname)s: %(message)s"""
    DEFAULT_MAX_BYTES = 500  # unit MB
    DEFAULT_BACKUP_COUNT = 10
    _logger = None

    def __init__(self, conf=None):
        """

        Args:
            conf: 配置文件
        """
        if conf:
            self.conf = conf
            self.logging_conf = {}
            self.set_level()
            self.set_format()
            self.set_file()
            self.rotate_handler = None
            self.rotate = self.conf.get('rotate')

    def set_level(self):
        level = self.conf.get("level")
        if level:
            level = getattr(logging, level.upper())
            self.logging_conf["level"] = level
        else:
            self.logging_conf["level"] = self.DEFAULT_LEVEL

    def set_format(self):
        format_ = self.conf.get("format", self.DEFAULT_FORMAT)
        self.logging_conf["format"] = format_

    def set_file(self):
        self.filename = self.conf.get("filename")
        if self.filename:
            self.logging_conf["filename"] = self.filename

    def replace_logging(self):
        logging.debug = self._logger.debug
        logging.info = self._logger.info
        logging.warn = self._logger.warning
        logging.warning = self._logger.warning
        logging.error = self._logger.error
        logging.critical = self._logger.critical
        logging.exception = self._logger.exception

    def get_formater(self):
        format_str = self.logging_conf.get("format")
        if _global.GEVENT:
            from ._gevent import GeventFomartter
            formatter = GeventFomartter(format_str)
        else:
            formatter = logging.Formatter(format_str)
        return formatter

    def get_logger(self, name):
        if not self.rotate and not _global.GEVENT:
            logging.basicConfig(
                **self.logging_conf
            )
            return get_logger(name)
        else:
            if self._logger is not None:
                return self._logger
            logger = get_logger(name)
            logger.name = name
            if self.filename:
                hl = logging.FileHandler(self.filename)
            else:
                hl = logging.StreamHandler()
            hl.setFormatter(self.get_formater())
            logger.addHandler(hl)
            logger.setLevel(self.logging_conf.get("level"))
            self._logger = logger
            self.replace_logging()
            return self._logger

    def get_rotating_logger(self, name=None):
        if self._logger is not None:
            return self._logger
        logger = get_logger(name)
        from logging.handlers import RotatingFileHandler
        if self.rotate:
            MB = 1000 * 1000
            maxBytes = self.conf.get('maxMB', self.DEFAULT_MAX_BYTES) * MB
            backupCount = self.conf.get('backupCount', self.DEFAULT_BACKUP_COUNT)
            rotate_handler = RotatingFileHandler(
                self.filename, mode="a", maxBytes=maxBytes, backupCount=backupCount
            )
            formatter = self.get_formater()
            rotate_handler.setFormatter(formatter)
            logger.propagate = False
            logger.addHandler(rotate_handler)
            logger.setLevel(self.logging_conf.get("level"))
        self._logger = logger
        self.replace_logging()
        return self._logger
