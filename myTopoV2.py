#!/usr/bin/python

# TO DO
# 1. Selesaikan konfigurasi ip address pada semua Node
# 2. Selesaikan konfigurasi routing statis pada router
# 3. Buat if else statement untuk setiap goal
# 4. Install MPTCP

# To ping use "{host name} ping -I {interface name} {destination}"

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Host, Node
from mininet.log import setLogLevel


# Creating Topology
setLogLevel("info")
net = Mininet()

# Adding all nodes
print("Creating all nodes")
r1 = net.addHost("r1", cls=Node)
r2 = net.addHost("r2", cls=Node)
r3 = net.addHost("r3", cls=Node)
r4 = net.addHost("r4", cls=Node)

c1 = net.addHost("c1", cls=Node)
c2 = net.addHost("c2", cls=Node)

## C1 to Router
net.addLink(c1, r1, bw=1)
net.addLink(c1, r2, bw=1)
## C2 to Router
net.addLink(c2, r3, bw=1)
net.addLink(c2, r4, bw=1)
## Router to Router
net.addLink(r1, r3, bw=0.5)
net.addLink(r1, r4, bw=1)
net.addLink(r2, r3, bw=1)
net.addLink(r2, r4, bw=0.5)

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
r1.cmd("sysctl net.ipv4.ip_forward=1")
# Manual routing
# ke 192.168.1.0
r1.cmd("ip route add 192.168.1.0/24 via 192.168.100.6 dev r1-eth2 onlink")
# ke 192.168.2.0
r1.cmd("ip route add 192.168.2.0/24 via 192.168.100.6 dev r1-eth2 onlink")
# ke 192.168.3.0
r1.cmd("ip route add 192.168.3.0/24 via 192.168.100.2 dev r1-eth1 onlink")


# Konfigurasi IP Address di R2
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


# Konfigurasi IP Address di R3
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


# Konfigurasi IP Address di R4
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


CLI(net)

net.stop()
