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
        totalFiles, totalSize = self._config.GetTotalFilesAndSize()
        i = 0
        for aFile in self._config.IterFiles():
            # Copy
            # Check integrity of both files
            i += 1
            if callable(progress):
                progress(aFile, i, totalFiles)
        if callable(end):
            end()

