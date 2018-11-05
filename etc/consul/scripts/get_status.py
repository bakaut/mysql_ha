import json,socket,time,sys

#Постучатся по двум сокету к други мерверам. Первый кто ответить использовать
#Список онлайн серверов из consul
try:

    cl = dba.get_cluster('clusterDev')
    cl_status = cl.status()
except Exception:
    shell.connect('root@192.168.1.48:3306', '7,Agf5Cupp0E,')
    cl = dba.get_cluster('clusterDev')
    cl_status = cl.status()

try:

    cl = dba.get_cluster('clusterDev')
    cl_status = cl.status()
except Exception:
    shell.connect('root@192.168.1.46:3306', '7,Agf5Cupp0E,')
    cl = dba.get_cluster('clusterDev')
    cl_status = cl.status()


local_ip = socket.gethostbyname(socket.gethostname())

for hosts in cl.status().items()[1][1]['topology'].values():

    if 'MISSING' in hosts['status'] and  local_ip in hosts['address']:
        try:
            print "Node missing, try readd " + hosts['address']
            #cl.rejoin_instance(hosts['address'])
            cl.add_instance(hosts['address'])
            #time.sleep(10)

            #if hosts['status'] == 'ONLINE':
            #    print "Rejoin " + hosts['address']  + " success"
            #else:
            #    print "Rejoin " + hosts['address']  + " failed"
            #time.sleep(30)
            print "Rejoin " + hosts['address']  + " success"
            sys.exit(1)

        except Exception:
               try:
                  print "Try to  rejoin " + hosts['address']
                  #cl.remove_instance(hosts['address'])
                  #cl.add_instance(hosts['address'])
                  cl.rejoin_instance(hosts['address'])
                  print "Rejoin instance " + hosts['address']  + " success"
                  sys.exit(1)
               except Exception:
                  #cl.rescan() # forse? how yes delete
                  #cl.add_instance(hosts['address'])
                  print "Rejoin " + hosts['address']  + " failed"
                  sys.exit(2)

cl = dba.get_cluster('clusterDev')
cl_status = cl.status()

for hosts in cl.status().items()[1][1]['topology'].values():

    if  hosts['mode'] == 'R/W' and hosts['status'] == 'ONLINE' and local_ip in hosts['address']:
         primary = hosts['address'].split(':')
         primary_ip = primary[0]
         print "This is master " + primary_ip
         sys.exit(0)
    if hosts['mode'] == 'R/O' and hosts['status'] == 'ONLINE' and local_ip in hosts['address']:
         secondary = hosts['address'].split(':')
         secondary_ip = secondary[0]
         print "This is slave " + secondary_ip
         sys.exit(0)
