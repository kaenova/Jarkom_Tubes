#!/usr/bin/python

# to run it do "sudo python myTopo.py"

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet

from mininet.node import RemoteController, OVSSwitch

from mininet.net import Mininet
from mininet.node import Node
from mininet.topo import Topo


class Router1(Node):
    def config(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=1")
        self.cmdPrint("ip addr add 192.168.0.1/24 brd + dev r0-eth0")
        self.cmdPrint("ip addr add 192.168.100.1/24 brd + dev r0-eth1")
        self.cmdPrint("ip addr add 192.168.100.2/24 brd + dev r0-eth2")

    def terminate(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=0")


class Router2(Node):
    def config(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=1")
        self.cmdPrint("ip addr add 192.168.0.2/24 brd + dev r0-eth0")
        self.cmdPrint("ip addr add 192.168.100.5/24 brd + dev r0-eth1")
        self.cmdPrint("ip addr add 192.168.100.6/24 brd + dev r0-eth2")

    def terminate(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=0")


class Router3(Node):
    def config(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=1")
        self.cmdPrint("ip addr add 192.168.1.1/24 brd + dev r0-eth0")
        self.cmdPrint("ip addr add 192.168.100.3/24 brd + dev r0-eth1")
        self.cmdPrint("ip addr add 192.168.100.4/24 brd + dev r0-eth2")

    def terminate(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=0")


class Router4(Node):
    def config(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=1")
        self.cmdPrint("ip addr add 192.168.1.2/24 brd + dev r0-eth0")
        self.cmdPrint("ip addr add 192.168.100.7/24 brd + dev r0-eth1")
        self.cmdPrint("ip addr add 192.168.100.8/24 brd + dev r0-eth2")

    def terminate(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=0")
        super(Router4, self).terminate()


# Jangan lupa selesaikan ini!
class PC1(Node):
    def config(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=1")
        self.cmdPrint("ip addr add 192.168.0.3/24 brd + dev r0-eth0")
        self.cmdPrint("ip addr add 192.168.0.4/24 brd + dev r0-eth1")

    def terminate(self):
        self.cmdPrint("sysctl net.ipv4.ip_forward=0")


class FinalTopo(Topo):
    "Topology for Final Projects"

    def build(self):
        # Creating Router hosts
        r1 = self.addNode("r1", cls=Node)
        r2 = self.addNode("r2", cls=Node)
        r3 = self.addNode("r3", cls=Node)
        r4 = self.addNode("r4", cls=Node)

        # Creating PC hosts
        c1 = self.addNode("c1", cls=Node)
        c2 = self.addNode("c2", cls=Node)

        # Adding Links
        ## C1 to Router
        self.addLink(c1, r1)
        self.addLink(c1, r2)
        ## C2 to Router
        self.addLink(c2, r3)
        self.addLink(c2, r4)
        ## Router to Router
        self.addLink(r1, r3)
        self.addLink(r1, r4)
        self.addLink(r2, r3)
        self.addLink(r2, r4)

        # Settings IP address


def runFinalTopo():
    topo = FinalTopo()

    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip="127.0.0.1"),
        switch=OVSSwitch,
        autoSetMacs=True,
    )

    net.start()
    CLI(net)
    # command.default(line="c1 ifconfig c1-eth0 192.168.0.3 netmask 255.255.255.0")

    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    runFinalTopo()

topos = {"tugas": FinalTopo}


# def myNet():
#     net = Mininet(build=False, ipBase="192.168.0.0/23")
#     net.start()
#     print("Creating Router")
#     # Checkpoint! 03-05-2021 00:14,
#     # Belum selesai Ngebuat Host berdasarkan kelas2nya
#     # Ikuti contoh dari ./module_example/gachiemhiep.py
#     # Setelah buat host router, buat host computer dengan kelas PC1 dan PC2

#     print("Creating Router")
#     c1 = net.addHost("c1", cls=PC1, defaultRoute=None)
#     c2 = net.addHost("c2", cls=PC2, defaultRoute=None)

#     print("Adding Link")
#     # PC1 with router
#     net.addLink(c1, r1, intfName1="r0-eth0", intfName2="r0-eth0")
#     net.addLink(c1, r2, intfName1="r0-eth1", intfName2="r0-eth0")
#     # PC2 with router
#     net.addLink(c2, r3, intfName1="r0-eth0", intfName2="r0-eth0")
#     net.addLink(c2, r4, intfName1="r0-eth1", intfName2="r0-eth0")


# if __name__ == "__init__":
#     # global net
#     print("Initializing Mininet")
#     Mininet.init()
#     myNet()
