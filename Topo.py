from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import Host, Node
#for ospfd and for ripd
import os
CURRENT_PATH = os.getcwd()

import datetime


#mendeklarasikan kelas MyTopo dengan parameter Topo
class MyTopo1dan3(Topo):
    #mendeklarasikan def/fungsi untuk membangun topologi
    def __init__(self, **opts):
        Topo.__init__( self, **opts)
        #Add host and switch
        linkopt = {'delay' : '5ms', 'loss' : 0}
        r1 =self.addHost("r1", cls=Node)
        r2 =self.addHost("r2", cls=Node)
        r3 =self.addHost("r3", cls=Node)
        r4 =self.addHost("r4", cls=Node)

        c1 = self.addHost("c1", cls=Node)
        c2 = self.addHost("c2", cls=Node)

        self.addLink(c1, r1, bw=1, **linkopt)
        self.addLink(c1, r2, bw=1, **linkopt)
        ## C2 to Router
        self.addLink(c2, r3, bw=1, **linkopt)
        self.addLink(c2, r4, bw=1, **linkopt)
        ## Router to Router
        self.addLink(r1, r3, bw=0.5, **linkopt)
        self.addLink(r1, r4, bw=1, **linkopt)
        self.addLink(r2, r3, bw=1, **linkopt)
        self.addLink(r2, r4, bw=0.5, **linkopt)
  
class MyTopo2(Topo):
    #mendeklarasikan def/fungsi untuk membangun topologi
    def __init__(self, **opts):
        Topo.__init__( self, **opts)
        #Add host and switch
        linkopt = {'delay' : '5ms', 'loss' : 0}
        r1 =self.addHost("r1", cls=Node)
        r2 =self.addHost("r2", cls=Node)
        r3 =self.addHost("r3", cls=Node)
        r4 =self.addHost("r4", cls=Node)

        c1 = self.addHost("c1", cls=Node)
        c2 = self.addHost("c2", cls=Node)

        self.addLink(c1, r1, bw=1, **linkopt)
        self.addLink(c1, r2, bw=1, **linkopt)
        ## C2 to Router
        self.addLink(c2, r3, bw=1, **linkopt)
        self.addLink(c2, r4, bw=1, **linkopt)
        ## Router to Router
        self.addLink(r1, r3, bw=0.5, **linkopt)
        self.addLink(r2, r3, bw=1, **linkopt)
        self.addLink(r2, r4, bw=0.5, **linkopt)

def runTopo2dan3():
    #get Current Time for Logging
    current = datetime.datetime.now()
    currDateStr = str(current.date())
    currTimeStr = "{:%H:%M:%S}".format(current)
    os.mkdir("{}/logs/{}_{}".format(CURRENT_PATH, currDateStr, currTimeStr))
    logs_path = "{}/logs/{}_{}/".format(CURRENT_PATH,currDateStr, currTimeStr)
    
    info("***Clearing switch and nodes \n")
    os.system('mn -c')
    topo = MyTopo1dan3()
    link = TCLink
    host = CPULimitedHost
    net = Mininet(topo=topo, link=link, controller = None ,host = Host) 
    net.start()
    c1, c2, r1, r2, r3 ,r4 = net.get('c1','c2', 'r1','r2','r3','r4')

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
    r1.cmd("sysctl net.ipv4.ip_forward=1")
    # Manual Routing
    # ke 192.168.1.0
    r1.cmd("ip route add 192.168.1.0/24 via 192.168.100.6 dev r1-eth2 onlink")
    # ke 192.168.2.0
    r1.cmd("ip route add 192.168.2.0/24 via 192.168.100.6 dev r1-eth2 onlink")
    # ke 192.168.3.0
    r1.cmd("ip route add 192.168.3.0/24 via 192.168.100.2 dev r1-eth1 onlink")
    
    r2.cmd("ifconfig r2-eth0 192.168.1.1/24")
    r2.cmd("ifconfig r2-eth1 192.168.100.9/30")
    r2.cmd("ifconfig r2-eth2 192.168.100.13/30")
    r2.cmd("sysctl net.ipv4.ip_forward=1")
    # Manual routing
    # ke 192.168.0.0
    r2.cmd("ip route add 192.168.0.0/24 via 192.168.100.10 dev r2-eth1 onlink")
    # ke 192.168.2.0
    r2.cmd("ip route add 192.168.2.0/24 via 192.168.100.10 dev r2-eth1 onlink")
    # ke 192.168.3.0
    r2.cmd("ip route add 192.168.3.0/24 via 192.168.100.14 dev r2-eth2 onlink")

    r3.cmd("ifconfig r3-eth0 192.168.2.1/24")
    r3.cmd("ifconfig r3-eth1 192.168.100.2/30")
    r3.cmd("ifconfig r3-eth2 192.168.100.10/30")
    r3.cmd("sysctl net.ipv4.ip_forward=1")
    # Manual routing
    # ke 192.168.0.0
    r3.cmd("ip route add 192.168.0.0/24 via 192.168.100.1 dev r3-eth1 onlink")
    # ke 192.168.1.0
    r3.cmd("ip route add 192.168.1.0/24 via 192.168.100.9 dev r3-eth2 onlink")
    # ke 192.168.3.0
    r3.cmd("ip route add 192.168.3.0/24 via 192.168.100.9 dev r3-eth2 onlink")

    r4.cmd("ifconfig r4-eth0 192.168.3.1/24")
    r4.cmd("ifconfig r4-eth1 192.168.100.6/30")
    r4.cmd("ifconfig r4-eth2 192.168.100.14/30")
    r4.cmd("sysctl net.ipv4.ip_forward=1")
    ## Manual routing
    # ke 192.168.0.0
    r4.cmd("ip route add 192.168.0.0/24 via 192.168.100.5 dev r4-eth1 onlink")
    # ke 192.168.1.0
    r4.cmd("ip route add 192.168.1.0/24 via 192.168.100.13 dev r4-eth2 onlink")
    # ke 192.168.2.0
    r4.cmd("ip route add 192.168.2.0/24 via 192.168.100.5 dev r4-eth1 onlink")

    # set Computer 2 as iperf server
    c2.cmdPrint('echo "Kaenova Mahendra Auditama \n C2 - runTopo2dan3-c2 at {}" > {}/runTopo2dan3-c2-iperf.txt && iperf -s --interval 1 >> {}/runTopo2dan3-c2-iperf.txt &'.format(f"{currDateStr} {currTimeStr}",logs_path,logs_path))
    # set Computer 1 as iperf client
    c1.cmdPrint('echo "Kaenova Mahendra Auditama \n C1 - runTopo2dan3-c1 at {}" > {}/runTopo2dan3-c1-iperf.txt && nohup iperf -c 192.168.2.2 --interval 1 --time 30 >> {}/runTopo2dan3-c1-iperf.txt &'.format(f"{currDateStr} {currTimeStr}",logs_path, logs_path))
    info('\n')

    #net.pingAll()
    CLI(net)
    net.stop()
        
if __name__ == '__main__':
    setLogLevel('info')
    runTopo2dan3()
 


# # set ospf untuk c1
# r1.cmdPrint("zebra -f {}/conf/zebra-{}.conf -d".format(currentpath, r1.name))
# r1.cmdPrint("ripd -f {}/conf/ripd-{}.conf -d".format(currentpath,r1.name))
# r1.waitOutput()