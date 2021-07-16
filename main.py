import gatodeseguridad

def main():
    print("gatodeseguridad")
    config = gatodeseguridad.config.Config("config.ini")
    # for path in config.IterFiles():
    #    print(path, type(path))
    #total, size = config.GetTotalFilesAndSize()
    #print(total, size)
    usb = config.GetEndpoint("USB")
    if usb.IsValid():
        def progress(file, i, totalFiles):
            print("progress", i, totalFiles)
        def end():
            print("End!!")
        usb.Full(progress, end)
    # print(str(config.GetEndpoints()[0]))

if __name__ == "__main__":
    main()
