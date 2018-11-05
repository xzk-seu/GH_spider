from gh_spider import page_spider, proxy_cfg


if __name__ == '__main__':
    d_str = '2011-12-30'
    proxy = proxy_cfg(5)
    page_spider(d_str, 38, proxy)
