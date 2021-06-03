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
c1.cmd("ifconfig c1-eth0 192.168.0.3/24")
c1.cmd("route add default gw 192.168.0.1 c1-eth0")
c1.cmd("ifconfig c1-eth1 192.168.0.4/24")
c1.cmd("route add default gw 192.168.0.2 c1-eth1")

# Konfigurasi IP Address di C2
c2.cmd("ifconfig c2-eth0 192.168.1.3/24")

c2.cmd("ifconfig c2-eth1 192.168.1.4/24")

# Konfigurasi IP Address di R1
r1.cmd("ifconfig r1-eth0 192.168.0.1/24")
r1.cmd("ifconfig r1-eth1 192.168.100.1/24")
r1.cmd("ifconfig r1-eth2 192.168.100.2/24")
r1.cmd("sysctl net.ipv4.ip_forward=1")

# Konfigurasi IP Address di R2
r2.cmd("ifconfig r2-eth0 192.168.0.2/24")
r2.cmd("ifconfig r2-eth1 192.168.100.6/24")
r2.cmd("ifconfig r2-eth2 192.168.100.5/24")
r2.cmd("sysctl net.ipv4.ip_forward=1")

# Konfigurasi IP Address di R3
r3.cmd("ifconfig r3-eth0 192.168.1.1/24")
r3.cmd("ifconfig r3-eth1 192.168.100.3/24")
r3.cmd("ifconfig r3-eth2 192.168.100.4/24")
r3.cmd("sysctl net.ipv4.ip_forward=1")

# Konfigurasi IP Address di R4
r4.cmd("ifconfig r4-eth0 192.168.1.2/24")
r4.cmd("ifconfig r4-eth1 192.168.100.8/24")
r4.cmd("ifconfig r4-eth2 192.168.100.7/24")
r4.cmd("sysctl net.ipv4.ip_forward=1")


CLI(net)

net.stop()
