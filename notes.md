## Topology

<img src="https://media.discordapp.net/attachments/848755541848227850/851095078645923850/unknown.png" width="720">

### Configuration

H0 : [192.168.0.3, 192.168.0.4]  
H1 : [192.168.1.3, 192.168.1.4]  
R1 : [192.168.0.1, 192.168.100.1, 192.168.100.2]  
R2 : [192.168.0.2, 192.168.100.5, 192.168.100.6]  
R3 : [192.168.1.1, 192.168.100.3, 192.168.100.4]  
R4 : [192.168.1.2, 192.168.100.7, 192.168.100.8]

All with subnet /24

## What do i have to build

- [ ] 2 Host
- [ ] 4 Router

### GOAL 1 (TCP and MPTCP)

- [ ] Implement MPTCP from Host A to Host B
      (https://multipath- [ ]tcp.org/pmwiki.php/Users/AptRepository)
- [ ] Generate traffic using iPerf
- [ ] Using Wireshark to analyze
- [ ] See the metrices (Throughput, Packet Loss, and Delay)

### GOAL 2 (Routing)

- [ ] Implement MPTCP from Host A to Host B
- [ ] Link Failure in R1 to R4
- [ ] Routing using RIP dan OSPF
- [ ] See the metrices (Convergence Time, Delay)
- [ ] Analisis durasi Convergence Time dan Delay yang terjadi

### GOAL 3 (MPTCP Analysis)

- [ ] Implement MPTCP from Host A to Host B
- [ ] Generate background traffic using iPerf
- [ ] Capture the traffic using wireshark
- [ ] Analysis MPTCP implementation from captured traffic

### GOAL 4

- [ ] Implement MPTCP from Host A to Host B
- [ ] sets the buffer in the router from 20 - [ ]> 100
- [ ] Caputre how the buffers affect delay time
- [ ] Analize

## Ref's

http://csie.nqu.edu.tw/smallko/sdn/twNics.htm
