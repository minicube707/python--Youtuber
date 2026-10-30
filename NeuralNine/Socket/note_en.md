# Understanding Computer Networks: IP Addresses, LANs, Clients, Servers, Ports, NAT, Routers, Sockets, TCP and UDP

> **Goal:** understand how two programs communicate, whether they are on
> the same network or across the Internet.

## 1. The big picture

When you open a website, several things work together:

1.  Your browser (the **client**) wants to retrieve a page.
2.  It contacts a **server** identified by an IP address.
3.  The communication uses a **transport protocol**, usually TCP or
    sometimes UDP.
4.  The server runs a program that listens on a specific **port**.
5.  Data travels in packets through your local network and possibly
    across several routers on the Internet.
6.  If your network uses a private IP address, your router may perform
    address translation called **NAT**.

Simplified diagram:

``` text
Browser (client)
       |
       | network request
       v
PC / phone -- Wi-Fi or Ethernet -- Router
                                      |
                                      | Internet
                                      v
                              Remote router(s)
                                      |
                                      v
                                 Web server
                                 IP + port
```

## 2. What is an IP address?

An **IP address** (*Internet Protocol address*) is a logical address
assigned to a network interface. It helps identify where an IP packet
should go and allows networks to forward it toward its destination.

A device can have several network interfaces and therefore several IP
addresses: for example, a Wi-Fi address, an Ethernet address, and a
loopback address.

There are two main versions:

-   **IPv4**: a 32-bit address, usually written as four numbers from 0
    to 255 separated by dots. Example: `192.168.1.20`.
-   **IPv6**: a 128-bit address, written as groups of hexadecimal digits
    separated by colons. Example: `2001:db8::20`.

An IP address identifies an interface on a network; it is not
necessarily the permanent identity of a person or device. It can change,
for example through DHCP or when connecting to a different network.

### Local IP address

The term **local IP address** usually refers to the address a device
uses on the network it is currently connected to. For example, your
computer might have `192.168.1.20` on your home Wi-Fi network.

The term can be ambiguous: - it may refer to a private address on the
local network; - it may also refer to `127.0.0.1` (IPv4) or `::1`
(IPv6), the **loopback** address.

Loopback allows a program to communicate with another program on the
same device without using the physical network. `localhost` is the
hostname commonly associated with loopback.

## 3. Private IP addresses and public IP addresses

### Private IP address

A private IP address is intended for use inside private networks, such
as a home, school, or company network. The IPv4 private ranges are:

  CIDR range         Address range
  ------------------ ------------------------------------
  `10.0.0.0/8`       `10.0.0.0` to `10.255.255.255`
  `172.16.0.0/12`    `172.16.0.0` to `172.31.255.255`
  `192.168.0.0/16`   `192.168.0.0` to `192.168.255.255`

These addresses are not routed directly across the public Internet. They
can be reused in many different networks: your home network and your
neighbor's network can both contain a device with the address
`192.168.1.20`.

### Public IP address

A public IP address is globally routable on the Internet. It is usually
assigned to your connection by your Internet Service Provider (ISP), or
to a server by its hosting provider.

In a typical home setup: - your computer has a private address, for
example `192.168.1.20`; - your router has a private address on the
home-network side and a public address on the Internet side.

Important: having a public IP address does not automatically mean that
every device on your network can be reached from the Internet. Firewall
rules and NAT affect incoming connections.

## 4. LAN: Local Area Network

**LAN** stands for *Local Area Network*. It is a group of connected
devices in a limited area, such as a home, office, or computer lab.

Devices can connect through: - Ethernet cables; - Wi-Fi; - or a
combination of both.

Example of a home network:

``` text
                 Internet
                    |
              [Wi-Fi Router]
               /     |      \
            [PC]  [Phone]  [Printer]
          192.168.1.20  .21    .30
```

In this example, the devices share the same local network and can
communicate directly if network settings and firewall rules allow it.

### Subnet mask and CIDR notation

An IP address is usually accompanied by a **subnet mask**, which
indicates which part identifies the network and which part identifies
the interface within that network.

Example: `192.168.1.20/24`.

-   `/24` means that the first 24 bits identify the network prefix.
-   The corresponding IPv4 subnet mask is `255.255.255.0`.
-   The network is `192.168.1.0/24`.
-   Usable host addresses are generally `192.168.1.1` through
    `192.168.1.254` in this typical subnet.

Two devices in the same subnet can usually communicate directly over the
LAN. To reach another network, they send packets to their **default
gateway**, which is often the router.

## 5. The router

A **router** connects multiple IP networks and forwards packets between
them according to its routing table.

At home, an Internet router or modem-router often combines several
functions: - routing between the home network and the Internet; - Wi-Fi
access point; - Ethernet switch; - DHCP server, which assigns IP
configuration; - firewall; - NAT/PAT.

The **default gateway** is the address of the router to which a device
sends packets intended for networks it does not know how to reach
directly.

Example: your PC has `192.168.1.20/24` and wants to contact a server at
`203.0.113.50`. Since that server is not on the local subnet, the PC
sends the packet to its gateway, for example `192.168.1.1`.

## 6. NAT: Network Address Translation

**NAT** stands for *Network Address Translation*. A NAT router changes
certain address information in packets as they pass from one network to
another.

The most common home-network case is **NAT with overload**, also called
**PAT** (*Port Address Translation*) or *NAT overload*.

Example:

``` text
Private network                  Internet
192.168.1.20:51500  ----\
                         \       NAT router
Phone                      --->  198.51.100.8:40001 ---> Server
192.168.1.21:51500  ----/       (public address)
```

The router keeps a translation table so it knows which private device
should receive each reply. It can distinguish multiple connections using
port numbers.

Remember: - NAT allows multiple private devices to share one public IPv4
address; - NAT is not the same thing as a firewall, even though home
routers commonly provide both; - unsolicited incoming connections are
usually blocked or do not have a defined destination device; - a **port
forwarding** rule can send traffic received on a public port to a
specific private device and port.

NAT is not required for IPv6 and should not be considered sufficient
security by itself.

## 7. Clients and servers

The words **client** and **server** describe roles in a communication,
not necessarily two different types of computers.

-   A **client** usually initiates a request for a service: a browser,
    mobile app, email client, and so on.
-   A **server** provides a service and usually waits for requests: a
    web server, file server, game server, and so on.

The same computer can act as a client in one communication and a server
in another.

Web example: 1. The browser is the client. 2. It requests a page from
the web server. 3. The server processes the request. 4. It sends back a
response containing, for example, HTML.

## 8. Ports

An IP address helps packets reach a network interface. But a computer
can run many network programs at the same time. A **port** allows the
operating system to deliver network data to the correct program or
service.

A TCP or UDP port is a number from `0` to `65535`.

Common examples:

    Port Common protocol                      Purpose
  ------ ------------------------------------ ---------
      22 TCP                                  SSH
      53 UDP and TCP                          DNS
      80 TCP                                  HTTP
     443 TCP, or QUIC over UDP                HTTPS
      25 TCP                                  SMTP
     123 UDP                                  NTP
    3389 TCP/UDP depending on configuration   RDP

Ports are commonly divided into ranges: - `0–1023`: system or well-known
ports; - `1024–49151`: registered ports; - `49152–65535`:
dynamic/ephemeral ports, often used by clients.

These are allocation conventions; exact use depends on the operating
system and application.

### IP address + port

A destination is often written like this:

``` text
192.168.1.20:8080
```

This means IPv4 address `192.168.1.20`, port `8080`.

For IPv6, the address is placed in square brackets when a port is added:

``` text
[2001:db8::20]:8080
```

## 9. TCP

**TCP** (*Transmission Control Protocol*) is a connection-oriented
transport protocol. It provides a reliable, ordered byte stream between
two applications.

Before exchanging data, TCP usually establishes a connection with a
three-step handshake:

``` text
Client                         Server
  | ------------ SYN -----------> |
  | <-------- SYN + ACK --------- |
  | ------------ ACK -----------> |
  |                               |
  | <========== data ===========> |
```

TCP provides, among other things: - retransmission of lost data; -
delivery of bytes in order; - error detection; - flow control; -
congestion control.

It is commonly used by SSH and by HTTP/1.1 or HTTP/2 with TLS in typical
deployments.

**Important:** TCP guarantees a byte stream, not the boundaries between
messages sent by an application. If a program sends two messages, the
receiver may get them in several pieces or combined together. The
application must define its own framing method (length field, delimiter,
format, and so on).

## 10. UDP

**UDP** (*User Datagram Protocol*) is a connectionless transport
protocol. It sends independent **datagrams**.

UDP: - does not establish a connection beforehand like TCP; - does not
guarantee delivery, ordering, or protection against duplicates; - has
fewer built-in mechanisms and a simpler structure; - preserves datagram
boundaries for the application.

It is useful when low latency or simplicity matters, or when the
application handles reliability itself.

Examples: - DNS (often UDP, but TCP is also used); - real-time voice and
video; - online games; - QUIC, which is used by HTTP/3 and runs over
UDP.

UDP is not automatically "faster" in every situation. Performance
depends on the network and the application. An application that needs
reliability may have to implement its own mechanisms.

### TCP or UDP?

  -----------------------------------------------------------------------
  Feature                 TCP                     UDP
  ----------------------- ----------------------- -----------------------
  Connection setup        Yes                     No

  Delivery guaranteed by  Yes, using              No
  the protocol            retransmissions         

  Data order guaranteed   Yes                     No

  Data unit seen by the   Byte stream             Datagram
  application                                     

  Typical use cases       Traditional web         DNS, real-time traffic,
                          traffic, SSH, file      QUIC
                          transfers               
  -----------------------------------------------------------------------

## 11. Sockets

A **socket** is a communication endpoint used by a program to send or
receive data through the operating system's networking facilities.

For an Internet socket, you will generally encounter: - an address
family, such as IPv4 or IPv6; - a transport type, such as TCP or UDP; -
a local IP address and local port; - optionally, a remote IP address and
remote port.

A TCP connection is generally identified by the protocol and its two
endpoints (source IP/port and destination IP/port). This allows a server
to handle many simultaneous connections on the same listening port.

### Server socket and client socket

**TCP server side:** 1. create a socket; 2. bind it to an address and
port (`bind`); 3. wait for connections (`listen`); 4. accept a
connection (`accept`); 5. exchange data; 6. close the socket.

**TCP client side:** 1. create a socket; 2. connect to the server's IP
address and port (`connect`); 3. send and receive data; 4. close the
socket.

With UDP, a server can bind a socket to a port (`bind`) and receive
datagrams. A TCP-style connection handshake is not required.

### Concrete example

Suppose: - server: `192.168.1.50`, TCP port `8080`; - client:
`192.168.1.20`, ephemeral port `53000`.

The communication can be represented like this:

``` text
192.168.1.20:53000  <==== TCP ====>  192.168.1.50:8080
       client                            server
```

The server listens on port `8080`. The client's operating system usually
selects a temporary port, here `53000`.

## 12. How everything works together: a complete example

You open `https://example.com` on your computer while connected to your
home Wi-Fi.

1.  **DNS:** your computer asks for the IP address associated with
    `example.com`.
2.  **Client:** your browser acts as the client.
3.  **Private IP:** your computer might have the address `192.168.1.20`.
4.  **Local network:** it checks whether the destination is on its
    subnet. It is not.
5.  **Router:** it therefore sends the packet to its default gateway,
    for example `192.168.1.1`.
6.  **NAT:** the router translates the private source address to its
    public address and keeps a mapping for the reply.
7.  **Transport:** depending on the negotiated connection, the browser
    may use TCP with TLS or QUIC over UDP.
8.  **Port:** HTTPS commonly uses server port `443`.
9.  **Server:** the remote service receives the request and sends back
    data.
10. **Return path:** the router uses its NAT table to forward the
    response to your computer.

Simplified view:

``` text
Computer                            NAT Router                 Web server
192.168.1.20:53000                  198.51.100.8:61000          203.0.113.50:443
       |                                  |                           |
       | -- request to Internet --------> |                           |
       |                                  | --- translated request -> |
       |                                  | <-------- response ------ |
       | <------ translated response ---- |                           |
```

The addresses `198.51.100.0/24` and `203.0.113.0/24` in this diagram are
reserved for documentation. They do not represent real public servers.

## 13. Useful commands for practice

### Windows

``` powershell
ipconfig
ipconfig /all
ping 192.168.1.1
tracert example.com
netstat -ano
```

### Linux

``` bash
ip addr
ip route
ping 192.168.1.1
traceroute example.com
ss -tulpen
```

### macOS

``` bash
ifconfig
netstat -rn
ping 192.168.1.1
traceroute example.com
lsof -i
```

Available commands and options vary by operating system. `ping` tests IP
connectivity using ICMP; it does not directly test whether a specific
TCP port is open. `ss` and `netstat` can show sockets and listening
ports.

## 14. Concepts you should not confuse

  -----------------------------------------------------------------------
  Concept                             What it does
  ----------------------------------- -----------------------------------
  IP address                          Identifies an interface and helps
                                      route IP packets

  MAC address                         Identifies a network interface on
                                      the local network link

  LAN                                 A local network connecting devices

  Router                              Forwards packets between networks

  Default gateway                     Router used for destinations
                                      outside the local subnet

  Private IP address                  Address intended for private
                                      networks

  Public IP address                   Address routable on the Internet

  NAT/PAT                             Translates addresses and often
                                      ports

  Port                                Directs traffic to a service or
                                      socket

  Client                              Program that requests a service

  Server                              Program that provides a service

  TCP                                 Reliable, ordered transport as a
                                      byte stream

  UDP                                 Datagram transport without delivery
                                      guarantees

  Socket                              Software interface for network
                                      communication
  -----------------------------------------------------------------------

## 15. Key takeaways

-   **IP** tells the network where to route a packet.
-   **The port** tells the operating system which service or program
    should receive the data.
-   **TCP or UDP** defines how data is transported.
-   **A socket** is the interface a program uses to communicate.
-   **A LAN** is a local network.
-   **A router** connects networks.
-   **NAT** allows multiple private devices to share a public IPv4
    address in many home networks.
-   **A client** requests a service; **a server** provides it.

A useful way to picture a network communication:

``` text
Transport protocol + source IP:source port
                 |
                 v
        destination IP:destination port
```

Example: `TCP 192.168.1.20:53000 → 203.0.113.50:443`.
