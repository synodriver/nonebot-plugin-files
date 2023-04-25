# -*- coding: utf-8 -*-
import abc


class BaseHandler(abc.ABC):
    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    async def __call__(self, file_url: str, file_name: str, current_path: str):
        """
        handle files
        :param file_url:
        :param file_name:
        :param current_path: original path
        :return:
        """

    @abc.abstractmethod
    async def close(self):
        """

        :return:
        """
