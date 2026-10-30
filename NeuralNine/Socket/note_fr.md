# Comprendre les réseaux : adresses IP, LAN, clients, serveurs, ports, NAT, routeurs, sockets, TCP et UDP

> **Objectif :** comprendre comment deux programmes, sur un même réseau
> ou à travers Internet, arrivent à communiquer.

## 1. La vue d'ensemble

Quand tu ouvres un site web, plusieurs éléments travaillent ensemble :

1.  Ton navigateur (le **client**) veut obtenir une page.
2.  Il contacte un **serveur** identifié par une adresse IP.
3.  La communication utilise un **protocole de transport**, généralement
    TCP ou parfois UDP.
4.  Le serveur héberge un programme qui écoute sur un **port** précis.
5.  Les données circulent dans des paquets à travers ton réseau local,
    puis éventuellement plusieurs routeurs sur Internet.
6.  Si ton réseau utilise une adresse privée, ton routeur peut effectuer
    une traduction d'adresses appelée **NAT**.

Schéma simplifié :

``` text
Navigateur (client)
       |
       | requête réseau
       v
PC / téléphone -- Wi-Fi ou Ethernet -- Routeur
                                         |
                                         | Internet
                                         v
                                  Routeur(s) distant(s)
                                         |
                                         v
                                  Serveur web
                                  IP + port
```

## 2. Une adresse IP, c'est quoi ?

Une **adresse IP** (*Internet Protocol*) est une adresse logique
attribuée à une interface réseau. Elle permet d'identifier la
destination d'un paquet IP et de l'acheminer vers elle.

Une machine peut avoir plusieurs interfaces réseau et donc plusieurs
adresses IP : par exemple une adresse Wi-Fi, une adresse Ethernet et une
adresse de boucle locale.

Il existe deux grandes versions :

-   **IPv4** : adresse sur 32 bits, généralement écrite sous la forme de
    quatre nombres de 0 à 255, séparés par des points. Exemple :
    `192.168.1.20`.
-   **IPv6** : adresse sur 128 bits, écrite en groupes hexadécimaux
    séparés par des deux-points. Exemple : `2001:db8::20`.

Une adresse IP identifie une interface dans un réseau ; elle n'est pas
nécessairement l'identité permanente d'une personne ou d'un appareil.
Elle peut changer, notamment avec DHCP ou lors d'un changement de
réseau.

### Adresse IP locale (local IP)

L'expression **adresse IP locale** désigne généralement l'adresse
utilisée par un appareil sur le réseau auquel il est connecté. Par
exemple, ton ordinateur peut avoir `192.168.1.20` sur le Wi-Fi de la
maison.

Le terme est parfois utilisé de façon ambiguë : - il peut désigner une
adresse privée du réseau local ; - il peut aussi désigner `127.0.0.1`
(IPv4) ou `::1` (IPv6), l'adresse de **boucle locale** (*loopback*).

La boucle locale permet à un programme de communiquer avec un autre
programme sur le même appareil, sans passer par le réseau physique.
`localhost` est le nom habituellement associé à cette boucle locale.

## 3. Adresse privée et adresse publique

### Adresse IP privée (private IP)

Une adresse privée est destinée à être utilisée à l'intérieur de réseaux
privés, comme un réseau domestique, scolaire ou d'entreprise. Les plages
IPv4 privées sont :

  Plage CIDR         Plage d'adresses
  ------------------ -----------------------------------
  `10.0.0.0/8`       `10.0.0.0` à `10.255.255.255`
  `172.16.0.0/12`    `172.16.0.0` à `172.31.255.255`
  `192.168.0.0/16`   `192.168.0.0` à `192.168.255.255`

Ces adresses ne sont pas routées directement sur l'Internet public.
Elles peuvent être réutilisées dans de nombreux réseaux différents : ton
réseau et celui de ton voisin peuvent tous les deux contenir un appareil
`192.168.1.20`.

### Adresse IP publique (public IP)

Une adresse publique est une adresse globalement routable sur Internet.
Elle est généralement attribuée à ta connexion par ton fournisseur
d'accès à Internet (FAI), ou à un serveur par son hébergeur.

Dans une installation domestique classique : - ton ordinateur possède
une adresse privée, par exemple `192.168.1.20` ; - ton routeur possède
une adresse privée côté maison et une adresse publique côté Internet.

Attention : une adresse publique ne signifie pas automatiquement que
tous les appareils de ton réseau sont accessibles depuis Internet. Le
pare-feu et le NAT contrôlent les communications entrantes.

## 4. Le LAN : réseau local

**LAN** signifie *Local Area Network*, ou réseau local. C'est un
ensemble d'appareils reliés dans une zone limitée : maison, bureau,
salle informatique, etc.

Les appareils peuvent être connectés : - par câble Ethernet ; - par
Wi-Fi ; - par un mélange des deux.

Exemple de réseau domestique :

``` text
                 Internet
                    |
              [Routeur Wi-Fi]
               /     |      \
          [PC]   [Téléphone] [Imprimante]
        192.168.1.20  .21       .30
```

Dans cet exemple, les appareils partagent le même réseau local et
peuvent communiquer directement si les règles réseau et le pare-feu le
permettent.

### Masque de sous-réseau et notation CIDR

Une adresse IP est généralement accompagnée d'un **masque** qui indique
quelle partie identifie le réseau et quelle partie identifie
l'interface.

Exemple : `192.168.1.20/24`.

-   `/24` signifie que les 24 premiers bits désignent le préfixe réseau.
-   Le masque IPv4 correspondant est `255.255.255.0`.
-   Le réseau est `192.168.1.0/24`.
-   Les adresses d'hôtes utilisables sont généralement `192.168.1.1` à
    `192.168.1.254` dans ce sous-réseau classique.

Deux appareils dans le même sous-réseau peuvent généralement échanger
directement sur le LAN. Pour joindre un autre réseau, ils envoient leurs
paquets à leur **passerelle par défaut**, souvent le routeur.

## 5. Le routeur (router)

Un **routeur** relie plusieurs réseaux IP et fait suivre les paquets de
l'un vers l'autre en fonction de sa table de routage.

À la maison, la box Internet combine souvent plusieurs fonctions : -
routeur entre le réseau domestique et Internet ; - point d'accès Wi-Fi
; - commutateur Ethernet (switch) ; - serveur DHCP, qui distribue des
paramètres IP ; - pare-feu ; - fonction NAT/PAT.

La **passerelle par défaut** est l'adresse du routeur à laquelle un
appareil envoie les paquets destinés à des réseaux qu'il ne connaît pas
directement.

Exemple : ton PC `192.168.1.20/24` veut contacter un serveur
`203.0.113.50`. Comme ce serveur n'est pas dans son sous-réseau local,
le PC transmet le paquet à sa passerelle, par exemple `192.168.1.1`.

## 6. NAT : traduction d'adresses réseau

**NAT** signifie *Network Address Translation*. Un routeur NAT modifie
certaines informations d'adresse dans les paquets lorsqu'ils passent
d'un réseau à un autre.

Dans un réseau domestique, le cas le plus courant est le **NAT avec
surcharge**, aussi appelé **PAT** (*Port Address Translation*) ou *NAT
overload*.

Exemple :

``` text
PC privé                         Internet
192.168.1.20:51500  ----\
                         \       Routeur NAT
Téléphone                  --->  198.51.100.8:40001 ---> Serveur
192.168.1.21:51500  ----/       (adresse publique)
```

Le routeur conserve une table de correspondance pour savoir à quel
appareil privé renvoyer les réponses. Il peut distinguer plusieurs
connexions grâce aux ports.

À retenir : - le NAT permet à plusieurs appareils privés de partager une
adresse IPv4 publique ; - le NAT n'est pas la même chose qu'un pare-feu,
même si les routeurs domestiques associent souvent les deux ; - une
connexion entrante non sollicitée est généralement bloquée ou ne sait
pas vers quel appareil être envoyée ; - une règle de **redirection de
port** (*port forwarding*) peut envoyer le trafic reçu sur un port
public vers un appareil et un port privés précis.

Le NAT n'est pas obligatoire pour IPv6 et n'est pas une mesure de
sécurité suffisante à lui seul.

## 7. Client et serveur

Les mots **client** et **serveur** décrivent des rôles dans une
communication, pas nécessairement deux types de machines.

-   Un **client** initie généralement une demande de service :
    navigateur, application mobile, client de messagerie, etc.
-   Un **serveur** fournit un service et attend généralement des
    demandes : serveur web, serveur de fichiers, serveur de jeu, etc.

Un même ordinateur peut être client dans une communication et serveur
dans une autre.

Exemple web : 1. Le navigateur est le client. 2. Il demande une page au
serveur web. 3. Le serveur traite la demande. 4. Il renvoie une réponse
contenant, par exemple, du HTML.

## 8. Les ports

Une adresse IP permet d'atteindre une interface réseau. Mais un
ordinateur peut exécuter beaucoup de programmes réseau en même temps. Le
**port** permet au système d'exploitation d'orienter les données vers le
bon programme ou service.

Un port TCP ou UDP est un nombre compris entre `0` et `65535`.

Exemples courants :

    Port Protocole courant             Utilisation
  ------ ----------------------------- -------------
      22 TCP                           SSH
      53 UDP et TCP                    DNS
      80 TCP                           HTTP
     443 TCP, ou QUIC sur UDP          HTTPS
      25 TCP                           SMTP
     123 UDP                           NTP
    3389 TCP/UDP selon configuration   RDP

Les ports sont souvent répartis en catégories : - `0–1023` : ports
système ou bien connus ; - `1024–49151` : ports enregistrés ; -
`49152–65535` : ports dynamiques/éphémères, souvent utilisés côté
client.

Ces catégories sont des conventions d'attribution ; les détails
dépendent du système et de l'usage.

### Adresse IP + port

On écrit souvent une destination sous la forme :

``` text
192.168.1.20:8080
```

Cela signifie : adresse IPv4 `192.168.1.20`, port `8080`.

Pour IPv6, on met l'adresse entre crochets lorsqu'on ajoute un port :

``` text
[2001:db8::20]:8080
```

## 9. TCP

**TCP** (*Transmission Control Protocol*) est un protocole de transport
orienté connexion. Il fournit un flux d'octets fiable et ordonné entre
deux applications.

Avant d'échanger les données, TCP établit généralement une connexion
avec une poignée de main en trois étapes (*three-way handshake*) :

``` text
Client                         Serveur
  | ---------- SYN -----------> |
  | <------ SYN + ACK --------- |
  | ---------- ACK -----------> |
  |                             |
  | <======= données =========> |
```

TCP apporte notamment : - la retransmission de données perdues ; - la
remise en ordre des octets ; - la détection d'erreurs ; - le contrôle de
flux ; - le contrôle de congestion.

On l'utilise notamment pour SSH et pour HTTP/1.1 ou HTTP/2 avec TLS dans
les déploiements habituels.

**Important :** TCP garantit un flux d'octets, pas la conservation des
frontières entre les messages envoyés par l'application. Si un programme
envoie deux messages, l'autre côté peut les recevoir en plusieurs
morceaux ou regroupés. Le programme doit définir son propre cadrage
(longueur, séparateur, format, etc.).

## 10. UDP

**UDP** (*User Datagram Protocol*) est un protocole de transport sans
connexion. Il envoie des **datagrammes** indépendants.

UDP : - ne fait pas de connexion préalable comme TCP ; - ne garantit ni
la livraison, ni l'ordre, ni l'absence de doublons ; - ajoute peu de
mécanismes et a donc une structure simple ; - conserve les frontières
des datagrammes pour l'application.

Il est utile quand la faible latence ou la simplicité compte, ou quand
l'application gère elle-même la fiabilité.

Exemples d'utilisation : - DNS (souvent UDP, mais TCP est aussi utilisé)
; - voix et vidéo en temps réel ; - jeux en ligne ; - QUIC, utilisé
notamment par HTTP/3, qui fonctionne au-dessus d'UDP.

UDP n'est pas automatiquement « plus rapide » dans toutes les situations
: cela dépend du réseau et de l'application. Une application qui a
besoin de fiabilité peut devoir ajouter ses propres mécanismes.

### TCP ou UDP ?

  -----------------------------------------------------------------------
  Caractéristique         TCP                     UDP
  ----------------------- ----------------------- -----------------------
  Connexion préalable     Oui                     Non

  Livraison garantie par  Oui, avec               Non
  le protocole            retransmissions         

  Ordre des données       Oui                     Non
  garanti                                         

  Unité vue par           Flux d'octets           Datagrammes
  l'application                                   

  Cas d'usage typique     Web classique, SSH,     DNS, temps réel, QUIC
                          transfert de fichiers   
  -----------------------------------------------------------------------

## 11. Les sockets

Une **socket** est un point de communication utilisé par un programme
pour envoyer ou recevoir des données via les mécanismes réseau du
système d'exploitation.

Pour une socket Internet, on rencontre généralement : - une famille
d'adresses, par exemple IPv4 ou IPv6 ; - un type de transport, par
exemple TCP ou UDP ; - une adresse IP locale et un port local ; -
éventuellement une adresse IP distante et un port distant.

Une connexion TCP est généralement identifiée par le protocole et les
deux extrémités (IP/port source et IP/port destination). Ainsi, un
serveur peut gérer de nombreuses connexions simultanées sur le même port
d'écoute.

### Socket serveur et socket client

**Côté serveur TCP :** 1. créer une socket ; 2. l'associer à une adresse
et un port (`bind`) ; 3. se mettre en attente de connexions (`listen`) ;
4. accepter une connexion (`accept`) ; 5. échanger des données ; 6.
fermer la socket.

**Côté client TCP :** 1. créer une socket ; 2. se connecter à l'adresse
IP et au port du serveur (`connect`) ; 3. envoyer et recevoir des
données ; 4. fermer la socket.

Pour UDP, un serveur peut associer une socket à un port (`bind`) et
recevoir des datagrammes ; il n'est pas nécessaire d'établir une
connexion TCP.

### Exemple concret

Supposons : - le serveur : `192.168.1.50`, port TCP `8080` ; - le client
: `192.168.1.20`, port éphémère `53000`.

La communication peut être représentée ainsi :

``` text
192.168.1.20:53000  <==== TCP ====>  192.168.1.50:8080
       client                         serveur
```

Le serveur écoute sur le port `8080`. Le système d'exploitation du
client choisit généralement un port temporaire, ici `53000`.

## 12. Comment tout fonctionne ensemble : exemple complet

Tu ouvres `https://example.com` depuis ton ordinateur connecté au Wi-Fi
de la maison.

1.  **DNS :** ton ordinateur demande l'adresse IP correspondant au nom
    `example.com`.
2.  **Client :** ton navigateur joue le rôle de client.
3.  **IP privée :** ton ordinateur peut avoir `192.168.1.20`.
4.  **Réseau local :** il vérifie si la destination est dans son
    sous-réseau. Elle ne l'est pas.
5.  **Routeur :** il envoie donc le paquet à sa passerelle par défaut,
    par exemple `192.168.1.1`.
6.  **NAT :** le routeur traduit l'adresse source privée en son adresse
    publique et garde une correspondance pour le retour.
7.  **Transport :** selon la connexion négociée, le navigateur peut
    utiliser TCP avec TLS ou QUIC sur UDP.
8.  **Port :** HTTPS utilise généralement le port serveur `443`.
9.  **Serveur :** le service distant reçoit la demande et renvoie les
    données.
10. **Retour :** le routeur utilise sa table NAT pour transmettre la
    réponse à ton ordinateur.

Vue simplifiée :

``` text
Ordinateur                         Routeur NAT                  Serveur web
192.168.1.20:53000                 198.51.100.8:61000           203.0.113.50:443
       |                                  |                            |
       | -- demande vers Internet ------> |                            |
       |                                  | ----- demande traduite --> |
       |                                  | <--------- réponse ------- |
       | <------ réponse traduite ------- |                            |
```

Les adresses `198.51.100.0/24` et `203.0.113.0/24` utilisées dans ce
schéma sont des plages réservées à la documentation : elles ne
représentent pas de vrais serveurs publics.

## 13. Quelques commandes utiles pour pratiquer

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

Les commandes disponibles et leurs options varient selon le système.
`ping` teste la connectivité IP avec ICMP ; il ne teste pas directement
si un port TCP donné est ouvert. `ss` et `netstat` permettent notamment
d'observer des sockets et des ports en écoute.

## 14. Les notions à ne pas confondre

  -----------------------------------------------------------------------
  Notion                              À quoi elle sert
  ----------------------------------- -----------------------------------
  Adresse IP                          Identifier une interface et
                                      acheminer les paquets IP

  Adresse MAC                         Identifier une interface sur le
                                      lien réseau local

  LAN                                 Réseau local reliant des appareils

  Routeur                             Faire circuler les paquets entre
                                      réseaux

  Passerelle par défaut               Routeur utilisé pour les
                                      destinations hors du sous-réseau

  Adresse privée                      Adresse prévue pour les réseaux
                                      privés

  Adresse publique                    Adresse routable sur Internet

  NAT/PAT                             Traduire des adresses, souvent
                                      aussi des ports

  Port                                Diriger le trafic vers un service
                                      ou une socket

  Client                              Programme qui demande un service

  Serveur                             Programme qui fournit un service

  TCP                                 Transport fiable et ordonné sous
                                      forme de flux

  UDP                                 Transport par datagrammes, sans
                                      garantie de livraison

  Socket                              Interface logicielle de
                                      communication réseau
  -----------------------------------------------------------------------

## 15. Résumé à retenir

-   **IP** indique où acheminer un paquet.
-   **Le port** indique à quel service ou programme le remettre.
-   **TCP ou UDP** définit comment les données sont transportées.
-   **La socket** est l'interface utilisée par le programme pour
    communiquer.
-   **Le LAN** est le réseau local.
-   **Le routeur** relie des réseaux.
-   **Le NAT** permet notamment à plusieurs appareils privés de partager
    une adresse publique IPv4.
-   **Le client** demande un service ; **le serveur** le fournit.

Une formule pratique pour visualiser une communication :

``` text
Protocole de transport + IP source:port source
                 |
                 v
        IP destination:port destination
```

Exemple : `TCP 192.168.1.20:53000 → 203.0.113.50:443`.
