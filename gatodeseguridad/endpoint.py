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

from pathlib import Path
from enum import Enum, auto
from shutil import copy2
from sys import exc_info
from typing import Generator, Callable, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from . import config
    import pathlib

class _Kind(Enum):
    DONE = auto()
    NO_VALID = auto()
    DESTINATION_NO_EXISTS = auto()

class Result:
    _errors: list[tuple[str, Type[Exception], Exception]] = []
    _kind: _Kind

    def __init__(self, kind: _Kind) -> None:
        # self._errors = []
        self._kind = kind

    def HasErrors(self) -> bool:
        return True if self._errors else False

    def AddError(self, path: str, _type: Type[Exception], value: Exception) -> None:
        self._errors.append((path, _type, value))

    def IterErrors(self) -> Generator[tuple[str, Type[Exception], Exception], None, None]:
        yield from self._errors

    def IsDone(self) -> bool:
        return self._kind == _Kind.DONE

    def IsNotValid(self) -> bool:
        return self._kind == _Kind.NO_VALID

    def DestinationNoExists(self) -> bool:
        return self._kind == _Kind.DESTINATION_NO_EXISTS

class Endpoint:
    _config: 'config.Config'
    _name: str
    _path: str

    def __init__(self, config: 'config.Config', name: str, path: str) -> None:
        self._config = config
        self._name = name
        self._path = path

    @property
    def Name(self) -> str:
        return self._name

    @property
    def Path(self) -> str:
        return self._path

    def IsValid(self) -> bool:
        return self._path != ""

    def __str__(self) -> str:
        return "%{0} - %{1}".format(self._name, self._path)

    def Full(self,
        progress: Callable[['pathlib.Path', int, int], None],
        end: Optional[Callable[[], None]] = None) -> Result:
        """
            Something
        """
        if not self.IsValid():
            return Result(_Kind.NO_VALID)
        path = Path(self._path).joinpath("full")
        if not path.exists():
            print("destination path does not exist")
            try:
                path.mkdir(parents=True, exist_ok=True)
            except FileNotFoundError as FNF:
                result = Result(_Kind.DESTINATION_NO_EXISTS)
                result.AddError(path.as_posix(), FileNotFoundError, FNF)
                return result
        result = Result(_Kind.DONE)
        drive = path.drive[0] if path.drive else '' # just the letter
        totalFiles, totalSize = self._config.GetTotalFilesAndSize()
        i = 0
        for aFile in self._config.IterFiles():
            # Copy
            # Check integrity of both files
            i += 1
            print(path, aFile)
            if drive:
                parts = aFile.parts[1:]
            else:
                parts = aFile.parts
            destination = path.joinpath(drive, *parts)
            destinationParent = destination.parent
            try:
                if not destinationParent.exists():
                    destinationParent.mkdir(parents=True, exist_ok=True)
                print(path, ", copy from: ", aFile, " ;to: ", destination)
                copy2(aFile, destination)
            except:
                result.AddError(aFile.as_posix(), *(exc_info()[:2]))
            finally:
                if callable(progress):
                    progress(aFile, i, totalFiles)
        if callable(end):
            end()
        return result

