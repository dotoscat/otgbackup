# Copyright 2021 Óscar Triano García

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

   # http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import configparser
from pathlib import Path
from typing import Generator
from .endpoint import Endpoint

class Config:
    def __init__(self, configPath: str):
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

    def IterFiles(self) -> Generator[Path, None, None]:
        for path in self._pathsList:
            yield from _walker(path, self._excludePathsList)

    def GetTotalFilesAndSize(self) -> tuple[int, int]:
        nFiles = 0
        size = 0
        for path in self._pathsList:
            for aFile in _walker(path, self._excludePathsList):
                nFiles += 1
                size += aFile.stat().st_size
        return nFiles, size

    def GetEndpoints(self) -> list[Endpoint]:
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

    def GetEndpoint(self, section: str) -> Endpoint:
        path = self._config.get(section, "Path", fallback="")
        return Endpoint(self, section, path)

def _walker(path: Path, excludePathList: list[Path]) -> Generator[Path, None, None]:
    if not path.exists():
        return
    for aPath in path.iterdir():
        if aPath in excludePathList:
            continue
        elif aPath.is_dir():
            yield from _walker(aPath, excludePathList)
        else:
            yield aPath
