import gatodeseguridad

def main():
    print("gatodeseguridad")
    config = gatodeseguridad.config.Config("config.ini")
    for path in config.IterFiles():
        print(path, type(path))
    total, size = config.GetTotalFilesAndSize()
    print(total, size)

if __name__ == "__main__":
    main()
