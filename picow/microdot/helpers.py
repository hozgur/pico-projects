_isPico = True
try:
    from machine import Pin, SPI
except ImportError:
    _isPico = False


def isPico():
    return _isPico

def getFreeMemory():
    if _isPico:
        import gc
        return gc.mem_free()
    else:
        import psutil
        return psutil.virtual_memory().free

def getFreeDiskSpace():
    if _isPico:
        import os
        return os.statvfs('/').free
    else:
        import shutil
        return shutil.disk_usage('/').free