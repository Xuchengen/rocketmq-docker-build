import concurrent.futures


class Context(object):
    """
    上下文类
    """

    # 线程池
    executor = concurrent.futures.ThreadPoolExecutor()
