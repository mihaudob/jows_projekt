# jows_projekt

## Generowanie ruchu
- iperf = BE, VoIP
```
server:
iperf -s -u -p 5061 {-S 0xC0} -l 200

client:
iperf -c 192.168.1.X -u -p 5061 {-S 0xC0} -l 200 -t 200 -b 200k -i 10
// -S = Type of service; payload (-l) to 200 bytes; the offered load (-b) to 200K
- VLC = Video
  - streaming - zapisac
    - odbior
    - nadanie
## Scenariusze
1. VoIP + BE + BE
- 50/45 - all good
- 1/94 - VoIP shitty
- w. jitter (?)
- wo. jitter (?)

1. Video + BE + BE
- 50/45 - all good
- 3/92 - shitty video
- w. jitter (?)
- wo. jitter (?)

1. VoIP + Video + BE
- 20/30/45 
- 2/3/99 
- w. jitter (?)
- wo. jitter (?)

## Ruch w sieci
- h11 - VoIP 
- h12 - BE 
- h21 - VoIP
- h22 - Video
- h31 - BE
- h32 - Video
## Symulacja
- minuta
- BE - 4 komendy
- VoIP - 4 komendy
- Video - VLC stream po HTTP
## Metody porownywania
- Wireshark (pcap)
 - do wykresu
- iperf na jitter, bandwidth, loss (-i 1)
  - zapisac wszystko na boku
- Jakosc video wizualna
