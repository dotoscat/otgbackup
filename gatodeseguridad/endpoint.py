from pathlib import Path
from enum import Enum, auto
from shutil import copy2
from sys import exc_info

class _Kind(Enum):
    DONE = auto()
    NO_VALID = auto()
    DESTINATION_NO_EXISTS = auto()

class Result:
    def __init__(self, kind):
        self._errors = []
        self._kind = kind

    def HasErrors(self):
        return True if self._errors else False

    def AddError(self, path, _type, value):
        self._errors.append((path, _type, value))

    def IterErrors(self):
        yield from self._errors

    def IsDone(self):
        return self._kind == _Kind.DONE

    def IsNotValid(self):
        return self._kind == _Kind.NO_VALID

class Endpoint:
    def __init__(self, config, name, path):
        self._config = config
        self._name = name
        self._path = path

    @property
    def Name(self):
        return self._name

    @property
    def Path(self):
        return self._path

    def IsValid(self):
        return self._path != ""

    def __str__(self):
        return "% - %".format(self._name, self._path)

    def Full(self, progress, end=None):
        """
            progress(currentFile, i, totalFiles)
            end()
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

