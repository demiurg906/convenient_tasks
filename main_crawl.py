from scrapy import cmdline


if __name__ == '__main__':
    cmd_line = f'scrapy crawl problems'
    cmdline.execute(cmd_line.split())
