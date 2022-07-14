from downloader import Downloader


def main():
    url = "https://lg.losangeles.vpsdime.com/100MB.test"
    target_file = "E://"
    downloader = Downloader(url, target_file)
    downloader.download()


if __name__ == '__main__':
    main()
