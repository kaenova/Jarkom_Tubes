#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Node


class Router1(Node):
    def config(self, **params):
        super(Router1, self).config(**params)
        self.cmd("sysctl net.ipv4.ip_forward=1")
        self.cmd("ip addr add 192.168.0.1/24 brd + dev r0-eth0")
        self.cmd("ip addr add 192.168.100.1/24 brd + dev r0-eth1")
        self.cmd("ip addr add 192.168.100.2/24 brd + dev r0-eth2")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(Router1, self).terminate()


class Router2(Node):
    def config(self, **params):
        super(Router2, self).config(**params)
        self.cmd("sysctl net.ipv4.ip_forward=1")
        self.cmd("ip addr add 192.168.0.2/24 brd + dev r0-eth0")
        self.cmd("ip addr add 192.168.100.5/24 brd + dev r0-eth1")
        self.cmd("ip addr add 192.168.100.6/24 brd + dev r0-eth2")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(Router2, self).terminate()


class Router3(Node):
    def config(self, **params):
        super(Router3, self).config(**params)
        self.cmd("sysctl net.ipv4.ip_forward=1")
        self.cmd("ip addr add 192.168.1.1/24 brd + dev r0-eth0")
        self.cmd("ip addr add 192.168.100.3/24 brd + dev r0-eth1")
        self.cmd("ip addr add 192.168.100.4/24 brd + dev r0-eth2")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(Router3, self).terminate()


class Router4(Node):
    def config(self, **params):
        super(Router4, self).config(**params)
        self.cmd("sysctl net.ipv4.ip_forward=1")
        self.cmd("ip addr add 192.168.1.2/24 brd + dev r0-eth0")
        self.cmd("ip addr add 192.168.100.7/24 brd + dev r0-eth1")
        self.cmd("ip addr add 192.168.100.8/24 brd + dev r0-eth2")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(Router4, self).terminate()


# Jangan lupa selesaikan ini!
class PC1(Node):
    def config(self, **params):
        super(Router4, self).config(**params)
        self.cmd("sysctl net.ipv4.ip_forward=1")
        self.cmd("ip addr add 192.168.0.3/24 brd + dev r0-eth0")
        self.cmd("ip addr add 192.168.0.4/24 brd + dev r0-eth1")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(Router4, self).terminate()


class PC2(Node):
    def config(self, **params):
        super(Router4, self).config(**params)
        self.cmd("sysctl net.ipv4.ip_forward=1")
        self.cmd("ip addr add 192.168.1.3/24 brd + dev r0-eth0")
        self.cmd("ip addr add 192.168.1.4/24 brd + dev r0-eth1")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(Router4, self).terminate()


def myNet():
    net = Mininet(build=False, ipBase="192.168.0.0/23")
    net.start()
    print("Creating Router")
    # Checkpoint! 03-05-2021 00:14,
    # Belum selesai Ngebuat Host berdasarkan kelas2nya
    # Ikuti contoh dari ./module_example/gachiemhiep.py
    # Setelah buat host router, buat host computer dengan kelas PC1 dan PC2
    r1 = net.addHost("r1", cls=Router1, defaultRoute=None)
    r2 = net.addHost("r2", cls=Router2, defaultRoute=None)
    r3 = net.addHost("r3", cls=Router3, defaultRoute=None)
    r4 = net.addHost("r4", cls=Router4, defaultRoute=None)

    print("Creating Router")
    c1 = net.addHost("c1", cls=PC1, defaultRoute=None)
    c2 = net.addHost("c2", cls=PC2, defaultRoute=None)

    print("Adding Link")
    # PC1 with router
    net.addLink(c1, r1, intfName1="r0-eth0", intfName2="r0-eth0")
    net.addLink(c1, r2, intfName1="r0-eth1", intfName2="r0-eth0")
    # PC2 with router
    net.addLink(c2, r3, intfName1="r0-eth0", intfName2="r0-eth0")
    net.addLink(c2, r4, intfName1="r0-eth1", intfName2="r0-eth0")


if __name__ == "__init__":
    # global net
    print("Initializing Mininet")
    Mininet.init()
    myNet()
