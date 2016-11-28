# -*- coding: utf-8 -*-
from selenium import webdriver
from browsermobproxy import Server
from urllib.parse import urlparse
from javascript_functions import JSCodeEmbedder

# ==============
# SETTINGS
from settings import path_to_brpwserproxy, path_to_phantomjs

URL_TO_PARSE = "https://kudago.com/spb/event/spektakl-podrostok-mdt/"


def get_service_args(proxy_url):
    return [
        '--proxy={}'.format(proxy_url),
        '--ignore-ssl-errors=true',
        '--load-images=false'
    ]


# ==============

# SETTING FOR THE PROXY (in order to avoid ads)

server = Server(path=path_to_brpwserproxy)
server.start()
proxy = server.create_proxy()
# proxy.blacklist("https?://.*(kudago.com)+.*", 200)

parsed_url = urlparse(URL_TO_PARSE)
# proxy.whitelist("(.+{}.*|.+maps.+)".format(parsed_url.hostname), 200)

# ==============

# proxy.new_har("req", options={'captureHeaders': True,'captureContent':True})
proxy.new_har()
driver = webdriver.PhantomJS(executable_path=path_to_phantomjs,
                             service_args=get_service_args(proxy.proxy))

js_emb = JSCodeEmbedder()

driver.get(URL_TO_PARSE)

har = proxy.har

for ent in proxy.har['log']['entries']:
    print(ent['request']['url'])
    print(ent['response']['content'])
    print('\n')

driver.save_screenshot('screen.png')
driver.execute_script(js_emb.get_xpath_by_xy, 100, 100)

# ==============
# FINISH

proxy.close()
driver.quit()

pass
