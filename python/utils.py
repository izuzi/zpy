import ctypes
import functools
import inspect
import threading
import time


def do_retry(retry_times=1, delay_seconds=0):
    """
    Decorator for function retry .

    @param retry_times: retry times
    @param delay_seconds: sleep time after per try
    @return: the return value of the called function
    @raise Exception: raises an exception when an error occurred after last time
    """

    def deco(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            _retry_times, _delay_seconds = retry_times, delay_seconds
            _err = None

            while _retry_times > 0:
                try:
                    _err = None
                    return f(*args, **kwargs)
                except Exception as e:
                    _err = e
                    if _delay_seconds > 0:
                        time.sleep(_delay_seconds)
                    _retry_times -= 1

            if _err:
                raise _err
        return wrapper
    return deco


def time_limit(timeout=0):
	"""
    Decorator for function timeout.

    @param timeout: the function will be quit after some seconds
    @return: the return value of the called function
    @raise Exception: raises an exception when timeout or some error occurred
	"""
	
    def deco(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            def _async_raise(tid, exctype):
                """raises the exception, performs cleanup if needed"""
                tid = ctypes.c_long(tid)
                if not inspect.isclass(exctype):
                    exctype = type(exctype)
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
                if res == 0:
                    raise ValueError("invalid thread id")
                elif res != 1:
                    # """if it returns a number greater than one, you're in trouble,
                    # and you should call it again with exc=NULL to revert the effect"""
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                    raise SystemError("PyThreadState_SetAsyncExc failed")

            class TimeLimit(threading.Thread):
                def __init__(self):
                    super(TimeLimit, self).__init__()
                    self.error=None
                    self.result=None

                def run(self):
                    try:
                        self.error=None
                        self.result=f(*args, **kwargs)
                    except Exception as e:
                        self.error = e
                        self.result = None

                def stop(self):
                    try:
                        _async_raise(self.ident, SystemExit)
                    except Exception:
                        pass

            t = TimeLimit()
            t.setDaemon(True)
            t.start()

            if timeout > 0:
                t.join(timeout)
            else:
                t.join()

            if t.isAlive():
                t.stop()
                emsg="function(%s) execute timeout after %d second" % (f.__name__, timeout)
                raise Exception(emsg)

            if t.error is not None:
                raise t.error

            return t.result
        return wrapper
    return deco
