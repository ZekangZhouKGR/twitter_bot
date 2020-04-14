from browsermobproxy import Server,RemoteServer

class RequestLog(object):
    def __init__(self, har_name, blacklist = [], har_options = {'captureHeaders':True,'captureContent':True }):
        import os
        #har_options = {}
        browsermob_exe = os.environ['BROWSERMOB'] if 'BROWSERMOB' in os.environ else 'D:/browsermob-proxy-2.1.4/bin/browsermob-proxy'
        self.server = Server(browsermob_exe)
        self.server.start()
        #raise
        #self.server = RemoteServer(host='111.230.223.37',port=62421)
        self.proxy = self.server.create_proxy({'httpProxy':'111.230.223.37:24342'})
        self.proxy.new_har(har_name,options = har_options)
        for host,code in blacklist:
            self.setBlackList(host, code)

    def setBlackList(self, host, code):
        self.proxy.blacklist(host,code)

    def setOptions(self, options):
        options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))

    def getHar(self):
        return self.proxy.har

    def getEntries(self):
        return self.proxy.har['log']['entries']

    def close(self):
        try:
            if self.server != None:
                self.server.stop()
        except:
            pass
        if self.proxy != None:
            self.proxy.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()