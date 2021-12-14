import dcsbridge.__main__
import sys


if __name__ == "__main__":
    try:
        dcsbridge.__main__.main(sys.argv[1:])
    except Exception:
        raise
