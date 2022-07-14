import archive


def main():
    versions = archive.get_version_list()
    for item in versions:
        print(item.version + ">" + item.date_time)


if __name__ == '__main__':
    main()
