import archive


def main():
    result_list = archive.get_version_list()
    for e in result_list:
        print(e.version + "---" + e.datetime)


if __name__ == '__main__':
    main()
