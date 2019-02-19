import json
import logger


class Config:
    _config = None
    _transient = None

    def __init__(self, filename, level=logger.DEFAULT_LOG_LEVEL):
        self._logger = logger.getLogger(name="cfg.%s" % self.__class__.__name__.ljust(logger.DEFAULT_NAME_LENGTH,
                                                                                      ' ')[:logger.DEFAULT_NAME_LENGTH],
                                        level=level)
        self.__load__(filename)
        self._transient = {}

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
        except IOError, e:
            self._logger.info("Couldn't load '{}'".format(filename))
            self._logger.debug("{}".format(e))
            return None

    def dump(self, filename):
        with open(filename, 'w') as settings_file:
            json.dump(self._config, settings_file)

    def get(self, key=None):
        try:
            return self._config[key]
        except KeyError:
            try:
                return self._transient[key]
            except KeyError:
                return None

    def set(self, key, value, transient=False):
        if transient:
            self._transient[key] = value
        else:
            self._config[key] = value

    def pop(self, key):
        self._config.pop(key, None)
