import configparser
from pathlib import Path

class Config:
    def __init__(self, configPath):
        config = configparser.ConfigParser()
        config.read_file(open(configPath))
        if not config.has_section("LOCAL"):
            raise Exception("config file does not have 'LOCAL' section")
        paths = config.get("LOCAL", "Paths", fallback="")
        if paths:
            pathsList = [Path(path) for path in paths.split(";")]
        else:
            raise Exception("'Paths' is empty in LOCAL 'section'")
        excludePaths = config.get("LOCAL", "ExcludePaths", fallback="")
        if excludePaths:
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
