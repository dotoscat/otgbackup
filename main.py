from typing import TYPE_CHECKING
import gatodeseguridad

if TYPE_CHECKING:
    from pathlib import Path

def main() -> None:
    print("gatodeseguridad")
    config = gatodeseguridad.config.Config("config.ini")
    # for path in config.IterFiles():
    #    print(path, type(path))
    #total, size = config.GetTotalFilesAndSize()
    #print(total, size)
    usb = config.GetEndpoint("USB")
    if usb.IsValid():
        def progress(file: Path, i: int , totalFiles: int) -> None:
            print("progress", i, totalFiles)
        def end() -> None:
            print("End!!")
        result = usb.Full(progress, end)
        for error in result.IterErrors():
            print(error, error[2])
    # print(str(config.GetEndpoints()[0]))

if __name__ == "__main__":
    main()
