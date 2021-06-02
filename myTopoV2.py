# TO DO
# 1. Selesaikan konfigurasi ip address pada semua Node
# 2. Selesaikan konfigurasi routing statis pada router
# 3. Buat if else statement untuk setiap goal
# 4. Install MPTCP

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Node


# Creating Topology
net = Mininet()

# Adding all nodes
r1 = net.addHost("r1", cls=Node)
r2 = net.addHost("r2", cls=Node)
r3 = net.addHost("r3", cls=Node)
r4 = net.addHost("r4", cls=Node)

c1 = net.addHost("c1", cls=Node)
c2 = net.addHost("c2", cls=Node)

## C1 to Router
net.addLink(c1, r1)
net.addLink(c1, r2)
## C2 to Router
net.addLink(c2, r3)
net.addLink(c2, r4)
## Router to Router
net.addLink(r1, r3)
net.addLink(r1, r4)
net.addLink(r2, r3)
net.addLink(r2, r4)

# Konfigurasi IP Address di C1
c1.cmd("ifconfig c1-eth0 192.168.0.3/24")
c1.cmd("ifconfig c1-eth1 192.168.0.4/24")

# Konfigurasi IP Address di C2
c2.cmd("ifconfig c2-eth0 192.168.1.3/24")
c2.cmd("ifconfig c2-eth1 192.168.1.4/24")

CLI(net)

net.stop()
