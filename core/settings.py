import json
import logger


class Config:
    _config = None

    def __init__(self, filename, level=logger.DEFAULT_LOG_LEVEL):
        self._logger = logger.getLogger(name="cfg.%s" % self.__class__.__name__.ljust(logger.DEFAULT_NAME_LENGTH,
                                                                                      ' ')[:logger.DEFAULT_NAME_LENGTH],
                                        level=level)
        self.__load__(filename)

    def __load__(self, filename):
        """

        :param filename:
        :return: The config or None if something went wrong
        """
        try:
            with open(filename, 'r') as settings_file:
                self._config = json.load(settings_file)
                self._logger.debug("Loaded config '{}'".format(filename))
        except IOError:
            self._logger.error("Couldn't load '{}'".format(filename))
            self._config = {}

    def merge(self, filename):
        """

        :param filename:
        :return: The config or None if something went wrong
        """
        try:
            with open(filename, 'r') as settings_file:
                self._config.update(json.load(settings_file))
            return self._config
        except IOError:
            return None

    def get(self, key=None):
        try:
            return self._config[key]
        except KeyError:
            return None

    def set(self, key, value):
        self._config[key] = value
