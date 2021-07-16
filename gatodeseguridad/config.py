import configparser
from pathlib import Path
from .endpoint import Endpoint

class Config:
    def __init__(self, configPath):
        self._config = configparser.ConfigParser()
        config = self._config
        config.read_file(open(configPath))
        if not config.has_section("LOCAL"):
            raise Exception("config file does not have 'LOCAL' section")
        paths = config.get("LOCAL", "Paths", fallback="")
        if paths:
            pathsList = [Path(path) for path in paths.split(";")]
        else:
            raise Exception("'Paths' is empty in LOCAL 'section'")
        excludePaths = config.get("LOCAL", "ExcludePaths", fallback="")
        excludePathsList = [Path(path) for path in excludePaths.split(";")]
        self._pathsList = pathsList
        self._excludePathsList = excludePathsList

    def IterFiles(self):
        for path in self._pathsList:
            yield from _walker(path, self._excludePathsList)

    def GetTotalFilesAndSize(self):
        nFiles = 0
        size = 0
        for path in self._pathsList:
            for aFile in _walker(path, self._excludePathsList):
                nFiles += 1
                size += aFile.stat().st_size
        return nFiles, size

    def GetEndpoints(self):
        # return self._config.sections()
        endpoints = []
        for section in self._config.sections():
            if section == "LOCAL":
                continue
            path = self._config.get(section, "Path", fallback="")
            if not path:
                continue
            endpoint = Endpoint(self, section, path)
            endpoints.append(endpoint)
        return endpoints

    def GetEndpoint(self, section):
        path = self._config.get(section, "Path", fallback="")
        return Endpoint(self, section, path)

def _walker(path, excludePathList):
    if not path.exists():
        return
    for aPath in path.iterdir():
        if aPath in excludePathList:
            continue
        elif aPath.is_dir():
            yield from _walker(aPath, excludePathList)
        else:
            yield aPath
