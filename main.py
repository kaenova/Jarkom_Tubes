from logging import log
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import Host, Node

from os import system
import os

import time

CURRENT_PATH = os.getcwd()

import datetime

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

# ref code 1
# Membuat Topologi untuk CLO1, CLO2, CLO3
class MyTopo(Topo):
    #mendeklarasikan def/fungsi untuk membangsun topologi
    def __init__(self, **opts):
        Topo.__init__( self, **opts)
        #Add host and switch
        linkopt = {'delay' : '0ms', 'loss' : 0}
        r1 =self.addHost("r1", cls=LinuxRouter)
        r2 =self.addHost("r2", cls=LinuxRouter)
        r3 =self.addHost("r3", cls=LinuxRouter)
        r4 =self.addHost("r4", cls=LinuxRouter)

        c1 = self.addHost("c1", cls=Host)
        c2 = self.addHost("c2", cls=Host)

        self.addLink(c1, r1, bw=1, cls=TCLink, **linkopt)
        self.addLink(c1, r2, bw=1, cls=TCLink, **linkopt)
        ## C2 to Router
        self.addLink(c2, r3, bw=1, cls=TCLink, **linkopt)
        self.addLink(c2, r4, bw=1, cls=TCLink, **linkopt)
        ## Router to Router
        self.addLink(r1, r3, bw=0.5, cls=TCLink, **linkopt)
        self.addLink(r1, r4, bw=1, cls=TCLink, **linkopt)
        self.addLink(r2, r3, bw=1, cls=TCLink, **linkopt)
        self.addLink(r2, r4, bw=0.5, cls=TCLink, **linkopt)
  
# ref code 5
# Membuat Topologi  
class MyTopoWithBuffer(Topo):
    #mendeklarasikan def/fungsi untuk membangsun topologi
    def __init__(self, max_queue, **opts):
        Topo.__init__( self, **opts)
        #Add host and switch
        print("MAX QUEUE: ", max_queue)
        linkopt = {'delay' : '0ms', 'loss' : 0}
        r1 =self.addHost("r1", cls=LinuxRouter)
        r2 =self.addHost("r2", cls=LinuxRouter)
        r3 =self.addHost("r3", cls=LinuxRouter)
        r4 =self.addHost("r4", cls=LinuxRouter)

        c1 = self.addHost("c1", cls=Host)
        c2 = self.addHost("c2", cls=Host)

        self.addLink(c1, r1, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        self.addLink(c1, r2, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        self.addLink(c2, r3, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        self.addLink(c2, r4, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        self.addLink(r1, r3, max_queue_size=max_queue, use_htb=True, bw=0.5, cls=TCLink, **linkopt)
        self.addLink(r1, r4, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        self.addLink(r2, r3, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        self.addLink(r2, r4, max_queue_size=max_queue, use_htb=True, bw=0.5, cls=TCLink, **linkopt)
        
        # self.addLink(c1, r1, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        # self.addLink(c1, r2, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        # ## C2 to Router
        # self.addLink(c2, r3, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        # self.addLink(c2, r4, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        # ## Router to Router
        # self.addLink(r1, r3, max_queue_size=max_queue, use_htb=True, bw=0.5, cls=TCLink, **linkopt)
        # self.addLink(r1, r4, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        # self.addLink(r2, r3, max_queue_size=max_queue, use_htb=True, bw=1, cls=TCLink, **linkopt)
        # self.addLink(r2, r4, max_queue_size=max_queue, use_htb=True, bw=0.5, cls=TCLink, **linkopt)

# CLO 1 (Konfigurasi Jaringan)                    
def runCLO1():
    #get Current Time for Logging
    current = datetime.datetime.now()
    currDateStr = str(current.date())
    currTimeStr = "{:%H:%M:%S}".format(current)
    os.mkdir("{}/logs/{}_{}".format(CURRENT_PATH, currDateStr, currTimeStr))
    logs_path = "{}/logs/{}_{}/".format(CURRENT_PATH,currDateStr, currTimeStr)
    
    info("***Clearing switch and nodes \n")
    os.system('mn -c')
    print("\n")
    topo = MyTopo()
    link = TCLink
    host = CPULimitedHost
    net = Mininet(topo=topo, link=link ,host = Host) 
    net.start()
    c1, c2, r1, r2, r3 ,r4 = net.get('c1','c2', 'r1','r2','r3','r4')

    # ref code 2
    # Konfigurasi IP Address di C1
    c1.cmd("ifconfig c1-eth0 192.168.0.2/24")
    c1.cmd("route add default gw 192.168.0.1 c1-eth0")
    c1.cmd("ifconfig c1-eth1 192.168.1.2/24")
    c1.cmd("route add default gw 192.168.1.1 c1-eth1")
    
    # Konfigurasi IP Address di C2
    c2.cmd("ifconfig c2-eth0 192.168.2.2/24")
    c2.cmd("route add default gw 192.168.2.1 c2-eth0")
    c2.cmd("ifconfig c2-eth1 192.168.3.2/24")
    c2.cmd("route add default gw 192.168.3.1 c2-eth1")

    # Konfigurasi IP Address di R1
    r1.cmd("ifconfig r1-eth0 192.168.0.1/24")
    r1.cmd("ifconfig r1-eth1 192.168.100.1/30")
    r1.cmd("ifconfig r1-eth2 192.168.100.5/30")
    
    # Konfigurasi IP Address di R2
    r2.cmd("ifconfig r2-eth0 192.168.1.1/24")
    r2.cmd("ifconfig r2-eth1 192.168.100.9/30")
    r2.cmd("ifconfig r2-eth2 192.168.100.13/30")
    
    # Konfigurasi IP Address di R3
    r3.cmd("ifconfig r3-eth0 192.168.2.1/24")
    r3.cmd("ifconfig r3-eth1 192.168.100.2/30")
    r3.cmd("ifconfig r3-eth2 192.168.100.10/30")
    
    # Konfigurasi IP Address di R4
    r4.cmd("ifconfig r4-eth0 192.168.3.1/24")
    r4.cmd("ifconfig r4-eth1 192.168.100.6/30")
    r4.cmd("ifconfig r4-eth2 192.168.100.14/30")

    logs_file = logs_path+"runCLO1-networkCheck.txt"
    # Pinging same networks
    print("Printing logfile in ({})".format(logs_file))
    print("Please wait while processing")
    
    c1.cmd('echo "Kaenova Mahendra Auditama \n runCLO1 \n Check Network Connectivity" >> {}'.format(logs_file))
    c1.cmd('echo "\n\n======= Reachable =======" >> {}'.format(logs_file))
    print("R1 - R3 (Area 1)")
    r1.cmd('echo "\n\nR1 - R3 (Area 1)" >> {} && ping -c 3 192.168.100.2 >> {}'.format(logs_file, logs_file)) 
    print("R1 - R4 (Area 2)")
    r1.cmd('echo "\n\nR1 - R4 (Area 2)" >> {} && ping -c 3 192.168.100.6 >> {}'.format(logs_file, logs_file)) 
    print("R2 - R3 (Area 3)")
    r2.cmd('echo "\n\nR2 - R3 (Area 3)" >> {} && ping -c 3 192.168.100.10 >> {}'.format(logs_file, logs_file)) 
    print("R2 - R4 (Area 4)")
    r2.cmd('echo "\n\nR2 - R4 (Area 4)" >> {} && ping -c 3 192.168.100.14 >> {}'.format(logs_file, logs_file))
    print("C1 - R1 (Area 5)")
    c1.cmd('echo "\n\nC1 - R1 (Area 5)" >> {} && ping -c 3 192.168.0.1 >> {}'.format(logs_file, logs_file))
    print("C1 - R2 (Area 6)")
    c1.cmd('"echo "\n\nC1 - R2 (Area 6)" >> {} && ping -c 3 192.168.1.1 >> {}'.format(logs_file, logs_file)) 
    print("C2 - R3 (Area 7)")
    c2.cmd('echo "\n\nC2 - R3 (Area 7)" >> {} && ping -c 3 192.168.2.1 >> {}'.format(logs_file, logs_file))
    print("C2 - R4 (Area 8)")
    c2.cmd('echo "\n\nC2 - R4 (Area 8)" >> {} && ping -c 3 192.168.3.1 >> {}'.format(logs_file, logs_file)) 
    
    # Unreacable
    c1.cmd('echo "\n\n======= Unreachable =======" >> {}'.format(logs_file))
    print("C1 - C2")
    c1.cmd('echo "\n\nC1 - C2" >> {} && ping -c 3 192.168.2.2 >> {}'.format(logs_file, logs_file)) 
    print("C1 - R4")
    c1.cmd('echo "\n\nC1 - R4" >> {} && ping -c 3 192.168.3.1 >> {}'.format(logs_file, logs_file)) 
    
    print("log file has been created at {}".format(logs_file))
    
    CLI(net)
    net.stop()

# CLO 2 (Static Routing)
def runCLO2():
    
    info("***Clearing switch and nodes \n")
    os.system('mn -c')
    print("\n")
    topo = MyTopo()
    link = TCLink
    host = CPULimitedHost
    net = Mininet(topo=topo, link=link ,host = Host) 
    net.start()
    c1, c2, r1, r2, r3 ,r4 = net.get('c1','c2', 'r1','r2','r3','r4')

    # ref code 3
    # Konfigurasi C1
    c1.cmd("ifconfig c1-eth0 192.168.0.2/24")
    c1.cmd("ifconfig c1-eth1 192.168.1.2/24")
    c1.cmd("ip rule add from 192.168.0.2 table 1")
    c1.cmd("ip rule add from 192.168.1.2 table 2")
    c1.cmd("ip route add default via 192.168.0.1 dev c1-eth0 table 1")
    c1.cmd("ip route add default via 192.168.1.1 dev c1-eth1 table 2")
    c1.cmd("ip route add 192.168.0.0/24 dev c1-eth0 scope link table 1")
    c1.cmd("ip route add 192.168.1.0/24 dev c1-eth1 scope link table 2")
    c1.cmd("ip route add default scope global nexthop via 192.168.0.1 dev c1-eth0")
    c1.cmd("ip route add default scope global nexthop via 192.168.1.1 dev c1-eth1")
    c1.cmd("route add default gw 192.168.1.1 dev c1-eth1")
    c1.cmd("route add default gw 192.168.0.1 dev c1-eth0")
    
    # Konfigurasi C2
    c2.cmd("ifconfig c2-eth0 192.168.2.2/24")
    c2.cmd("ifconfig c2-eth1 192.168.3.2/24")
    c2.cmd("ip rule add from 192.168.2.2 table 1")
    c2.cmd("ip rule add from 192.168.3.2 table 2")
    c2.cmd("ip route add default via 192.168.2.1 dev c2-eth0 table 1")
    c2.cmd("ip route add default via 192.168.3.1 dev c2-eth1 table 2")
    c2.cmd("ip route add 192.168.2.0/24 dev c2-eth0 scope link table 1")
    c2.cmd("ip route add 192.168.3.0/24 dev c2-eth1 scope link table 2")
    c2.cmd("ip route add default scope global nexthop via 192.168.3.1 dev c2-eth1")
    c2.cmd("ip route add default scope global nexthop via 192.168.2.1 dev c2-eth0")
    c2.cmd("route add default gw 192.168.3.1 dev c2-eth1")
    c2.cmd("route add default gw 192.168.2.1 dev c2-eth0")
    

    # Konfigurasi R1
    r1.cmd("ifconfig r1-eth0 192.168.0.1/24")
    r1.cmd("ifconfig r1-eth1 192.168.100.1/30")
    r1.cmd("ifconfig r1-eth2 192.168.100.5/30")
    r1.cmd("sysctl net.ipv4.ip_forward=1")
    # Routing R1
    r1.cmd("route add -net 192.168.2.0/24 gw 192.168.100.2")
    r1.cmd("route add -net 192.168.3.0/24 gw 192.168.100.6")
    r1.cmd("route add -net 192.168.1.0/24 gw 192.168.100.6")
    r1.cmd("route add -net 192.168.100.8/30 gw 192.168.100.2")
    r1.cmd("route add -net 192.168.100.12/30 gw 192.168.100.6")

    # Konfigurasi R3
    r3.cmd("ifconfig r3-eth0 192.168.2.1/24")
    r3.cmd("ifconfig r3-eth1 192.168.100.2/30")
    r3.cmd("ifconfig r3-eth2 192.168.100.10/30")
    r3.cmd("sysctl net.ipv4.ip_forward=1")
    # Routing R3
    r3.cmd("route add -net 192.168.0.0/24 gw 192.168.100.1")
    r3.cmd("route add -net 192.168.1.0/24 gw 192.168.100.9")
    r3.cmd("route add -net 192.168.3.0/24 gw 192.168.100.9")
    r3.cmd("route add -net 192.168.100.4/30 gw 192.168.100.1")
    r3.cmd("route add -net 192.168.100.12/30 gw 192.168.100.9")
    
    # Konfigurasi R2
    r2.cmd("ifconfig r2-eth0 192.168.1.1/24")
    r2.cmd("ifconfig r2-eth1 192.168.100.9/30")
    r2.cmd("ifconfig r2-eth2 192.168.100.13/30")
    r2.cmd("sysctl net.ipv4.ip_forward=1")
    # Routing R2
    r2.cmd("route add -net 192.168.0.0/24 gw 192.168.100.10")
    r2.cmd("route add -net 192.168.2.0/24 gw 192.168.100.10")
    r2.cmd("route add -net 192.168.3.0/24 gw 192.168.100.14")
    r2.cmd("route add -net 192.168.100.4/30 gw 192.168.100.14")
    r2.cmd("route add -net 192.168.100.0/39 gw 192.168.100.10")

    # Konfigurasi R4
    r4.cmd("ifconfig r4-eth0 192.168.3.1/24")
    r4.cmd("ifconfig r4-eth1 192.168.100.6/30")
    r4.cmd("ifconfig r4-eth2 192.168.100.14/30")
    r4.cmd("sysctl net.ipv4.ip_forward=1")
    # Routing R4
    r4.cmd("route add -net 192.168.0.0/24 gw 192.168.100.5")
    r4.cmd("route add -net 192.168.1.0/24 gw 192.168.100.13")
    r4.cmd("route add -net 192.168.2.0/24 gw 192.168.100.5")
    r4.cmd("route add -net 192.168.100.8/30 gw 192.168.100.13")
    r4.cmd("route add -net 192.168.100.0/30 gw 192.168.100.5")

    print("Routing has been initialize, no log file created")
    CLI(net)
    net.stop()
    
# CLO 3 (TCP)
def runCLO3():
    #get Current Time for Logging
    current = datetime.datetime.now()
    currDateStr = str(current.date())
    currTimeStr = "{:%H:%M:%S}".format(current)
    os.mkdir("{}/logs/{}_{}".format(CURRENT_PATH, currDateStr, currTimeStr))
    logs_path = "{}/logs/{}_{}/".format(CURRENT_PATH,currDateStr, currTimeStr)
    
    info("***Clearing switch and nodes \n")
    os.system('mn -c')
    print("\n")
    topo = MyTopo()
    link = TCLink
    host = CPULimitedHost
    net = Mininet(topo=topo, link=link ,host = Host) 
    net.start()
    c1, c2, r1, r2, r3 ,r4 = net.get('c1','c2', 'r1','r2','r3','r4')

    # Konfigurasi C1
    c1.cmd("ifconfig c1-eth0 192.168.0.2/24")
    c1.cmd("ifconfig c1-eth1 192.168.1.2/24")
    c1.cmd("ip rule add from 192.168.0.2 table 1")
    c1.cmd("ip rule add from 192.168.1.2 table 2")
    c1.cmd("ip route add default via 192.168.0.1 dev c1-eth0 table 1")
    c1.cmd("ip route add default via 192.168.1.1 dev c1-eth1 table 2")
    c1.cmd("ip route add 192.168.0.0/24 dev c1-eth0 scope link table 1")
    c1.cmd("ip route add 192.168.1.0/24 dev c1-eth1 scope link table 2")
    c1.cmd("ip route add default scope global nexthop via 192.168.0.1 dev c1-eth0")
    c1.cmd("ip route add default scope global nexthop via 192.168.1.1 dev c1-eth1")
    c1.cmd("route add default gw 192.168.1.1 dev c1-eth1")
    c1.cmd("route add default gw 192.168.0.1 dev c1-eth0")
    
    # Konfigurasi C2
    c2.cmd("ifconfig c2-eth0 192.168.2.2/24")
    # c2.cmd("route add default gw 192.168.2.1 c2-eth0")
    c2.cmd("ifconfig c2-eth1 192.168.3.2/24")
    # c2.cmd("route add default gw 192.168.3.1 c2-eth1")
    c2.cmd("ip rule add from 192.168.2.2 table 1")
    c2.cmd("ip rule add from 192.168.3.2 table 2")
    c2.cmd("ip route add default via 192.168.2.1 dev c2-eth0 table 1")
    c2.cmd("ip route add default via 192.168.3.1 dev c2-eth1 table 2")
    c2.cmd("ip route add 192.168.2.0/24 dev c2-eth0 scope link table 1")
    c2.cmd("ip route add 192.168.3.0/24 dev c2-eth1 scope link table 2")
    c2.cmd("ip route add default scope global nexthop via 192.168.3.1 dev c2-eth1")
    c2.cmd("ip route add default scope global nexthop via 192.168.2.1 dev c2-eth0")
    c2.cmd("route add default gw 192.168.3.1 dev c2-eth1")
    c2.cmd("route add default gw 192.168.2.1 dev c2-eth0")
    

    # Konfigurasi R1
    r1.cmd("ifconfig r1-eth0 192.168.0.1/24")
    r1.cmd("ifconfig r1-eth1 192.168.100.1/30")
    r1.cmd("ifconfig r1-eth2 192.168.100.5/30")
    r1.cmd("sysctl net.ipv4.ip_forward=1")
    r1.cmd("route add -net 192.168.2.0/24 gw 192.168.100.2")
    r1.cmd("route add -net 192.168.3.0/24 gw 192.168.100.6")
    r1.cmd("route add -net 192.168.1.0/24 gw 192.168.100.6")
    r1.cmd("route add -net 192.168.100.8/30 gw 192.168.100.2")
    r1.cmd("route add -net 192.168.100.12/30 gw 192.168.100.6")

    # Konfigurasi R3
    r3.cmd("ifconfig r3-eth0 192.168.2.1/24")
    r3.cmd("ifconfig r3-eth1 192.168.100.2/30")
    r3.cmd("ifconfig r3-eth2 192.168.100.10/30")
    r3.cmd("sysctl net.ipv4.ip_forward=1")
    r3.cmd("route add -net 192.168.0.0/24 gw 192.168.100.1")
    r3.cmd("route add -net 192.168.1.0/24 gw 192.168.100.9")
    r3.cmd("route add -net 192.168.3.0/24 gw 192.168.100.9")
    r3.cmd("route add -net 192.168.100.4/30 gw 192.168.100.1")
    r3.cmd("route add -net 192.168.100.12/30 gw 192.168.100.9")
    
    # Konfigurasi R2
    r2.cmd("ifconfig r2-eth0 192.168.1.1/24")
    r2.cmd("ifconfig r2-eth1 192.168.100.9/30")
    r2.cmd("ifconfig r2-eth2 192.168.100.13/30")
    r2.cmd("sysctl net.ipv4.ip_forward=1")
    r2.cmd("route add -net 192.168.0.0/24 gw 192.168.100.10")
    r2.cmd("route add -net 192.168.2.0/24 gw 192.168.100.10")
    r2.cmd("route add -net 192.168.3.0/24 gw 192.168.100.14")
    r2.cmd("route add -net 192.168.100.4/30 gw 192.168.100.14")
    r2.cmd("route add -net 192.168.100.0/39 gw 192.168.100.10")

    # Konfigurasi R4
    r4.cmd("ifconfig r4-eth0 192.168.3.1/24")
    r4.cmd("ifconfig r4-eth1 192.168.100.6/30")
    r4.cmd("ifconfig r4-eth2 192.168.100.14/30")
    r4.cmd("sysctl net.ipv4.ip_forward=1")
    r4.cmd("route add -net 192.168.0.0/24 gw 192.168.100.5")
    r4.cmd("route add -net 192.168.1.0/24 gw 192.168.100.13")
    r4.cmd("route add -net 192.168.2.0/24 gw 192.168.100.5")
    r4.cmd("route add -net 192.168.100.8/30 gw 192.168.100.13")
    r4.cmd("route add -net 192.168.100.0/30 gw 192.168.100.5")

    # ref code 4
    # Server iperf C2
    c2.cmd("iperf -s &")
    # Setting up tcpdump
    c2.cmd("nohup tcpdump -c 10 -i c2-eth0 -w {}/tcpdump.pcap tcp&".format(logs_path))
    time.sleep(1)
    # iperfing
    c1.cmd("iperf -t 5 -c 192.168.2.2 &")
    print("currently generating traffic, please wait for 5 second")
    time.sleep(5)
    c1.cmdPrint("tcpdump -r {}/tcpdump.pcap".format(logs_path))
    
    print("\nTcp dump file (.pcap) has been created at {}/tcpdump.pcap".format(logs_path))
    CLI(net)
    net.stop()
        
# CLO 4 (Buffer Size)
def runCLO4():
    #get Current Time for Logging
    current = datetime.datetime.now()
    currDateStr = str(current.date())
    currTimeStr = "{:%H:%M:%S}".format(current)
    os.mkdir("{}/logs/{}_{}".format(CURRENT_PATH, currDateStr, currTimeStr))
    logs_path = "{}/logs/{}_{}/".format(CURRENT_PATH,currDateStr, currTimeStr)
    
    buffer_size = int(input("Masukkan buffer size (bilangan bulat): "))
    
    info("***Clearing switch and nodes \n")
    os.system('mn -c')
    print("\n")
    topo = MyTopoWithBuffer(buffer_size)
    link = TCLink
    host = CPULimitedHost
    net = Mininet(topo=topo, link=link ,host = Host) 
    net.start()
    c1, c2, r1, r2, r3 ,r4 = net.get('c1','c2', 'r1','r2','r3','r4')

    # Konfigurasi C1
    c1.cmd("ifconfig c1-eth0 192.168.0.2/24")
    c1.cmd("ifconfig c1-eth1 192.168.1.2/24")
    c1.cmd("ip rule add from 192.168.0.2 table 1")
    c1.cmd("ip rule add from 192.168.1.2 table 2")
    c1.cmd("ip route add default via 192.168.0.1 dev c1-eth0 table 1")
    c1.cmd("ip route add default via 192.168.1.1 dev c1-eth1 table 2")
    c1.cmd("ip route add 192.168.0.0/24 dev c1-eth0 scope link table 1")
    c1.cmd("ip route add 192.168.1.0/24 dev c1-eth1 scope link table 2")
    c1.cmd("ip route add default scope global nexthop via 192.168.0.1 dev c1-eth0")
    c1.cmd("ip route add default scope global nexthop via 192.168.1.1 dev c1-eth1")
    c1.cmd("route add default gw 192.168.1.1 dev c1-eth1")
    c1.cmd("route add default gw 192.168.0.1 dev c1-eth0")
    
    # Konfigurasi C2
    c2.cmd("ifconfig c2-eth0 192.168.2.2/24")
    c2.cmd("ifconfig c2-eth1 192.168.3.2/24")
    c2.cmd("ip rule add from 192.168.2.2 table 1")
    c2.cmd("ip rule add from 192.168.3.2 table 2")
    c2.cmd("ip route add default via 192.168.2.1 dev c2-eth0 table 1")
    c2.cmd("ip route add default via 192.168.3.1 dev c2-eth1 table 2")
    c2.cmd("ip route add 192.168.2.0/24 dev c2-eth0 scope link table 1")
    c2.cmd("ip route add 192.168.3.0/24 dev c2-eth1 scope link table 2")
    c2.cmd("ip route add default scope global nexthop via 192.168.3.1 dev c2-eth1")
    c2.cmd("ip route add default scope global nexthop via 192.168.2.1 dev c2-eth0")
    c2.cmd("route add default gw 192.168.3.1 dev c2-eth1")
    c2.cmd("route add default gw 192.168.2.1 dev c2-eth0")
    

    # Konfigurasi R1
    r1.cmd("ifconfig r1-eth0 192.168.0.1/24")
    r1.cmd("ifconfig r1-eth1 192.168.100.1/30")
    r1.cmd("ifconfig r1-eth2 192.168.100.5/30")
    r1.cmd("sysctl net.ipv4.ip_forward=1")
    r1.cmd("route add -net 192.168.2.0/24 gw 192.168.100.2")
    r1.cmd("route add -net 192.168.3.0/24 gw 192.168.100.6")
    r1.cmd("route add -net 192.168.1.0/24 gw 192.168.100.6")
    r1.cmd("route add -net 192.168.100.8/30 gw 192.168.100.2")
    r1.cmd("route add -net 192.168.100.12/30 gw 192.168.100.6")

    # Konfigurasi R3
    r3.cmd("ifconfig r3-eth0 192.168.2.1/24")
    r3.cmd("ifconfig r3-eth1 192.168.100.2/30")
    r3.cmd("ifconfig r3-eth2 192.168.100.10/30")
    r3.cmd("sysctl net.ipv4.ip_forward=1")
    r3.cmd("route add -net 192.168.0.0/24 gw 192.168.100.1")
    r3.cmd("route add -net 192.168.1.0/24 gw 192.168.100.9")
    r3.cmd("route add -net 192.168.3.0/24 gw 192.168.100.9")
    r3.cmd("route add -net 192.168.100.4/30 gw 192.168.100.1")
    r3.cmd("route add -net 192.168.100.12/30 gw 192.168.100.9")
    
    # Konfigurasi R2
    r2.cmd("ifconfig r2-eth0 192.168.1.1/24")
    r2.cmd("ifconfig r2-eth1 192.168.100.9/30")
    r2.cmd("ifconfig r2-eth2 192.168.100.13/30")
    r2.cmd("sysctl net.ipv4.ip_forward=1")
    r2.cmd("route add -net 192.168.0.0/24 gw 192.168.100.10")
    r2.cmd("route add -net 192.168.2.0/24 gw 192.168.100.10")
    r2.cmd("route add -net 192.168.3.0/24 gw 192.168.100.14")
    r2.cmd("route add -net 192.168.100.4/30 gw 192.168.100.14")
    r2.cmd("route add -net 192.168.100.0/39 gw 192.168.100.10")

    # Konfigurasi R4
    r4.cmd("ifconfig r4-eth0 192.168.3.1/24")
    r4.cmd("ifconfig r4-eth1 192.168.100.6/30")
    r4.cmd("ifconfig r4-eth2 192.168.100.14/30")
    r4.cmd("sysctl net.ipv4.ip_forward=1")
    r4.cmd("route add -net 192.168.0.0/24 gw 192.168.100.5")
    r4.cmd("route add -net 192.168.1.0/24 gw 192.168.100.13")
    r4.cmd("route add -net 192.168.2.0/24 gw 192.168.100.5")
    r4.cmd("route add -net 192.168.100.8/30 gw 192.168.100.13")
    r4.cmd("route add -net 192.168.100.0/30 gw 192.168.100.5")
    
    # ref code 6
    # Setting up traffic
    c2.cmd("iperf -s &")
    c1.cmd("iperf -t 30 -B 192.168.0.2 -c 192.168.2.2 &")
    c1.cmd("iperf -t 30 -B 192.168.1.2 -c 192.168.2.2 &")
    
    # set Computer 1 as iperf client
    c1.cmd('echo "Kaenova Mahendra Auditama \n C1 - runCLO4-c1 at {} \n with buffer {}" > {}/runCLO4-c1-{}-iperf.txt && ping -I c1-eth1 192.168.2.2 >> {}/runCLO4-c1-{}-iperf.txt && echo "\n Finish" >> {}/runCLO4-c1-{}-iperf.txt &'.format(f"{currDateStr} {currTimeStr}",buffer_size, logs_path, buffer_size, logs_path, buffer_size, logs_path, buffer_size))
    info('\n')
    print("Currently generating ping log file in the background")
    print("log file is created at {}".format(logs_path))
    
    CLI(net)
    net.stop()
        
        
if __name__ == '__main__':
    setLogLevel('info')
    check_input = True
    
    system("cls" if os.name == "nt" else "clear")
    while check_input:
        print("Tugas Besar Jaringan Komputer")
        print("Kaenova Mahendra Auditama | 1301190324 | IF-43-02")
        print("Pilihan: ")
        print("1. CLO1 (Pinging same network)")
        print("2. CLO2 (Routing)")
        print("3. CLO3 (TCP Analysis)")
        print("4. CLO4 (Buffer)")
        pilihan = input("Masukkan nomor CLO yang diinginkan: ")
        if pilihan == "1" or pilihan == "2" or pilihan == "3" or pilihan == "4":
            check_input = False
        
    print("================== Initializing ==================")
        
    if pilihan == "1":
        runCLO1()
    elif pilihan == "2":
        runCLO2()
    elif pilihan == "3":
        runCLO3()
    elif pilihan == "4":
        runCLO4()
    else:
        raise ValueError("Input {} tidak tersedia".format(pilihan))
