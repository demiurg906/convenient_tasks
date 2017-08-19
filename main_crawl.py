import sys
from scrapy import cmdline


if __name__ == '__main__':
    args = ' '.join(sys.argv[1:])
    cmd_line = f'scrapy crawl problems {args}'
    cmdline.execute(cmd_line.split())
