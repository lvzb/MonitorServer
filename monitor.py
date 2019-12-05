# -*- coding=utf-8 -*-
import psutil
import json
import pymongo
import datetime

class Host():
    def __init__(self):
        self.partition = []
        self.proccess = []
        self.name = "127.0.0.1"

    def disk(self):
        part = psutil.disk_partitions()
        for item in part:
            diskUsage = psutil.disk_usage(item.mountpoint)
            disk_dic = {"mountpoint":item.mountpoint,"total":diskUsage.total,"free":diskUsage.free,"percent":diskUsage.percent,"used":diskUsage.used}
            self.partition.append(disk_dic)

    def nginxProcess(self):
        for proc in psutil.process_iter():
            if proc.name()=='nginx':
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name','exe','cmdline'])
                except Exception, e:
                    pass
                else:
                    self.proccess.append(pinfo)


    def javaProcess(self):
        for proc in psutil.process_iter():
            if proc.name()=='java':
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name','exe','cmdline'])
                except Exception, e:
                    pass
                else:
                    self.proccess.append(pinfo)


if __name__ == '__main__':
    host = Host()
    host.name = "192.168.1.20";
    host.disk()
    host.javaProcess()
    host.nginxProcess()
    memory = psutil.virtual_memory()
    mem_dic = {"total":memory.total,"used":memory.used,"free":memory.free,"percent":memory.percent}
    conn = pymongo.MongoClient('127.0.0.1',27017)
    db_auth = conn.admin
    db_auth.authenticate("root", "mytest123")
    db = conn.ossdb
    data = {"name":host.name,"cpu":psutil.cpu_percent(0),"mem":mem_dic,"disk":host.partition,"process":host.proccess,"date": datetime.datetime.now()}
    db.host.save(data)