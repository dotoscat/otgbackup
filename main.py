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

from typing import TYPE_CHECKING
import otgbackup

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
