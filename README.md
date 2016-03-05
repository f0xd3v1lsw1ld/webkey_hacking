title: Hacking Conrad WebKey
date: 2016-03-05

Auf der diesjährigen Embedded World gab es wieder einige mehr oder wenige sinnvolle Werbegeschenke. Eines davon ist der USB-WebKey der Fa. Conrad.
Dieser funktioniert so: Nachdem er an den PC angeschlossen wurde, meldet er sich als HID an und nach dem er betätigt wurde, sendet er einige vorgefertige Tastaturcodes an den PC. Ziel ist es, dass mit dem Standard Browser die Webseite "www.community.conrad.com" angezeigt wird.

#Erster Test, unter Linux Mint
Kurz gesagt, der WebKey funktioniert unter meinem Linux Mint nicht. 
Nach kurzer Internet Recherche sieht es so aus, dass dies beabsichtigt ist. Grund ist sehr wahrscheinlich, dass Sicherheitsrisiko, was mit diesem WebKeys einhergeht. Schließlich ist vorab nicht abzusehen, was dieser alles so anstellen.
Wenn bei geöffnetem Terminal der Key betätigt wird, erscheint nur Kauderwelsch.
```
11911911946991111091091171101051161214699111110114971004699111109 r
```
Zumindest lässt sich unter Linux einges mehr über das Gerät herausfinden.
##dmesg
Schauen wir uns zuerst an, als was sich der WebKey im System anmeldet. Dazu folgender **dmesg** Auszug:
```
[  183.980631] usb 1-4: new low-speed USB device number 3 using xhci_hcd
[  184.170001] usb 1-4: New USB device found, idVendor=05ac, idProduct=020b
[  184.170009] usb 1-4: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[  184.170012] usb 1-4: Product: WebKey
[  184.170015] usb 1-4: Manufacturer: WebKey
[  184.170318] usb 1-4: ep 0x81 - rounding interval to 64 microframes, ep desc says 80 microframes
[  184.174468] input: WebKey WebKey as /devices/pci0000:00/0000:00:14.0/usb1/1-4/1-4:1.0/0003:05AC:020B.0003/input/input15
[  184.229367] hid-generic 0003:05AC:020B.0003: input,hidraw2: USB HID v1.10 Keyboard [WebKey WebKey] on usb-0000:00:14.0-4/input0
```
Wie man sieht handelt es sich um einen WebKey (ID 05AC:020B) und dieser wird als USB HID Keyboard im System registriert.

##lsusb
Um Details über dieses USB-Device herauszufinden, schauen wir uns das Ergbnis von **lsusb** an
```
Bus 001 Device 012: ID 05ac:020b Apple, Inc. Pro Keyboard [Mitsumi, A1048/US layout]
```
In der Ausgabe suchen wir nach der ID des WebKey und sehen, dass es sich angeblich um eine Apple Tastatur handeln soll.

##showkey

Die dritte Möglichkeit, welche ich ausprobiert habe, ist **showkey**. Mit diesem kleinen Tool kann man sich die Keycodes einer Tastatur ansehen.
```
$ showkey -a

Drücken Sie eine Taste - Strg+D beendet das Programm

r 	114 0162 0x72
^[OH 	 27 0033 0x1b
 	 79 0117 0x4f
 	 72 0110 0x48
^? 	127 0177 0x7f
1 	 49 0061 0x31
1 	 49 0061 0x31
9 	 57 0071 0x39
1 	 49 0061 0x31
1 	 49 0061 0x31
9 	 57 0071 0x39
1 	 49 0061 0x31
1 	 49 0061 0x31
9 	 57 0071 0x39
4 	 52 0064 0x34
6 	 54 0066 0x36
9 	 57 0071 0x39
9 	 57 0071 0x39
1 	 49 0061 0x31
1 	 49 0061 0x31
1 	 49 0061 0x31
1 	 49 0061 0x31
0 	 48 0060 0x30
9 	 57 0071 0x39
1 	 49 0061 0x31
0 	 48 0060 0x30
9 	 57 0071 0x39
1 	 49 0061 0x31
1 	 49 0061 0x31
7 	 55 0067 0x37
1 	 49 0061 0x31
1 	 49 0061 0x31
0 	 48 0060 0x30
1 	 49 0061 0x31
0 	 48 0060 0x30
5 	 53 0065 0x35
1 	 49 0061 0x31
1 	 49 0061 0x31
6 	 54 0066 0x36
1 	 49 0061 0x31
2 	 50 0062 0x32
1 	 49 0061 0x31
4 	 52 0064 0x34
6 	 54 0066 0x36
9 	 57 0071 0x39
9 	 57 0071 0x39
1 	 49 0061 0x31
1 	 49 0061 0x31
1 	 49 0061 0x31
1 	 49 0061 0x31
1 	 49 0061 0x31
0 	 48 0060 0x30
1 	 49 0061 0x31
1 	 49 0061 0x31
4 	 52 0064 0x34
9 	 57 0071 0x39
7 	 55 0067 0x37
1 	 49 0061 0x31
0 	 48 0060 0x30
0 	 48 0060 0x30
4 	 52 0064 0x34
6 	 54 0066 0x36
9 	 57 0071 0x39
9 	 57 0071 0x39
1 	 49 0061 0x31
1 	 49 0061 0x31
1 	 49 0061 0x31
1 	 49 0061 0x31
0 	 48 0060 0x30
9 	 57 0071 0x39
  	 32 0040 0x20
^M 	 13 0015 0x0d
^D 	  4 0004 0x04
```
Wie man erkennt, erkennt man nichts. Es bleibt der gleiche Kauderwelsch.

#[usbutils und usb-devices](https://unix.stackexchange.com/questions/60078/find-out-which-modules-are-associated-with-a-usb-device)
Die letzte Möglichkeit die mir eingefallen ist, bietet usbutils und das darin enthaltende Skript usb-devices. Wird dieses ausgeführt, werden zu jedem USB Device diverse Informationen und der verwendete Treiber, für den WebKey ist es **usbhid**, angezeigt. Genau dieser wäre auch der erste Ansatzpunkt, um herauszufinden warum der Webkey unter Mint nur Kauderwelsch ausgibt.

```
$ usb-utils
...
T:  Bus=01 Lev=01 Prnt=01 Port=03 Cnt=03 Dev#= 12 Spd=1.5 MxCh= 0
D:  Ver= 1.10 Cls=00(>ifc ) Sub=00 Prot=00 MxPS= 8 #Cfgs=  1
P:  Vendor=05ac ProdID=020b Rev=03.01
S:  Manufacturer=WebKey
S:  Product=WebKey
C:  #Ifs= 1 Cfg#= 1 Atr=80 MxPwr=32mA
I:  If#= 0 Alt= 0 #EPs= 1 Cls=03(HID  ) Sub=01 Prot=01 Driver=usbhid
...
```
Zur weiteren Analyse im Linux Mint sollte man sich also mal den **usbhid driver** ansehen.

#Zweiter Test, unter Windows 8.1
So nachdem ich unter Linux schon einige Details erfahren konnte, habe ich den WebKey auch unter Windows probiert. Hier funktioniert dieser auch wie er sollte. Nach Betätigung öffnet sich das **Ausführen Fenster** und die vorgesehene URL wird eingetragen. Daraus schließe ich das der WebKey am Anfang zumindest **WIN+R** zum öffnen des **Ausführen Fensters** sendet, daran anschließend die URL und abschließend einen Zeilenumbruch sendet.

#Hardware Analyse
Jetzt wo die Funktion des WebKeys bekannt ist und dieser zumindest unter Windows funktioniert, bin ich neugierig auf den Inhalt geworden. Dazu die drei kleinen Schrauben auf der Rückseite gelöst und man kann sich die kleine PCB im Inneren ansehen. Viel gibt es aber dabei nicht zu sehen. Das Teil ist sehr simmple aufgebaut. Unter der Versiegelung befindet sich ein kleiner Controller, zentral angeordnet die (ohne Deckel sehr helle) weiße LED und die beiden Button. Interresanter ist der kleine achtbeinige Käfer mit der **Aufschrift T24C02A** neben dem Anschluß der USB Leitungen. Bei diesem handelt es sich um einen 256 Byte großen I2C EEprom, wie es ihn z.B. von der Fa. [Atmel](www.atmel.com/images/doc0180.pdf) gibt. In diesem ist die URL abgelegt, welche nach der Betätigung angezeigt werden soll.
Um den EEprom auszulesen und zu Beschreiben muss dieser an einen externen Controller angeschlossen werden, welcher über eine I2C Schnittstelle und laut EEprom Datenblatt über 3,3V oder 5V Stromversorgung verfügen muss.

#WebKey und Raspberry Pi
##Funktionstest 
Für solche kleinen Bastelein eignet sich hervorragend das Raspberry Pi. Ich nehme dafür mein Model A. 
Aber bevor ich mich mit dem EEprom beschäftige, wird der WebKey natürlich auch im Raspbian geteset.
Mt laufenden Desktop funktioniert er nicht, es wird war "Ausführen" geöffnet, aber es erfolgt keine Eingabe der URL. Dies geht aber auch Prinzip bedingt nicht, da eine einfache Eingabe der URL nicht den Browser öffnet. Dazu müsste der Browser mit der Webseite als Paramter aufgerufen werden z.B. **epiphany www.raspberrypi.org**

Wird Raspbian ohne Desktop gestartet erfolgt zumindest die Ausgabe der URL (www.community.conrad.de). Der scheinbar unter Mint vorgesehende Schutz ist im Raspbian nicht enthalten.

##Anschluß
Damit das RPi mit dem EEprom kommunizieren kann, müssen beide zuerst miteinander kontaktiert werden. Im folgenden Bild ist die Anschlussbelegung dargestellt.

[BILD folgt]

Dafür müssen folgende Schritte ausgeführt werden:

###1. Raspberry Pi und WebKey ausschalten und von der Stromversorgung trennen.
###2. Anschlussleitungen an den EEprom anlöten
###3. Raspberry Pi Stiftleiste via Breadboard und Breadboardkabel mit dem vorbereiteten WebKey verbinden
###4. Raspberry Pi anschalten
###5. Auf das Raspberry PI **i2c-tools** installieren 
```sh
$ sudo apt-get install i2c-tools
```
###6. I2C aktivieren, dazu folgendes in die **/boot/config.txt** eintragen 
```
$ sudo vi /boot/config.txt
dtparam=i2c0=on
dtparam=i2c1=on
dtparam=i2c_arm=on
```
###6. Anschließend müssen noch die I2C Treiber für Linux und den Broadcom Chip geladen werden
```
$ sudo modprobe i2c_dev
$ sudo modprobe i2c-bcm2708
```
um dies permanent zu machen kann auch folgendes
- i2c_dev und
- i2c-bcm2708 
in **/etc/modules** eingetragen werden.
###7. Die I2C Adresse des WebKeys kann mittles **i2cdetect** herausgefunden werden.

```
$ i2cdetect -y 1 #(-y 1 entspricht I2C Bus 1)
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: 50 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
Die 7-bit Adresse des EEproms lautet also **0x50**.
###8. Zur Kommunikation mit dem EEprom können folgende Tools verwendet werden
- Lesen: **i2cget -y 1 <addresse>**
- Schreiben: **i2cset -y 1 <chip addresse> <reg> <wert>**
- Speicherauszug des EEprom anzeigen **i2cdump -y1 <chip addresse>**

WICHTIG: Zum Schreiben muss dasWrite Protection (WP) Pin auf Masse gezogen werden

## EEprom überschreiben
Nachdem jetzt das EEprom Layout bekannt ist, wird dieses ersteinmal gesichert. Dazu einfach die Ausgabe von i2cdump in eine Datei umleiten:
```
$ i2cdump -y 1 0x50 >eeprom_dump.txt
$ cat eeprom_dump.txt
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef
00: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
10: 54 4f 4e 54 45 58 7e 05 77 77 77 2e 63 6f 6d 6d    TONTEX~?www.comm
20: 75 6e 69 74 79 2e 63 6f 6e 72 61 64 2e 63 6f 6d    unity.conrad.com
30: 08 77 77 77 2e 63 6f 6d 6d 75 6e 69 74 7a 2e 63    ?www.communitz.c
40: 6f 6e 72 61 64 2e 63 6f 6d 00 13 a0 ff ff ff ff    onrad.com.??....
50: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
60: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
70: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
80: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
90: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
a0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
b0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
c0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
d0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
e0: ff ff 00 ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
f0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
```
Wie man dem Dump entnehmen kann beginnt der inhalt ab der Adresse 0x11. Was Dabei die ASCII Repräsentation (TONTEX) der ersten Bytes bedeutet ist mir nicht klar. Die eigentliche URL beginnt ab 0x18. Anschließend wird ist diese zweimal im Speicher gehalten, unterbrochen von einem 0x08 (Backspace?) und abgeschlossen von 0x00 0x13 und 0xA0. Wobei 0x00 wahrscheinlich das Textende signalisiert. Was die beiden letzten Bytes bedeuten ist mir noch nicht klar. Zumindest entspricht 0xA0 keinem ASCII Symbol mehr.

Um den EEprom zu beschreiben habe ich nicht **i2cset** verwendet, sondern ich habe mir mit hilfe des smbus Modules ein python Skript geschrieben. Dafür muss aber zuerst muss dafür aber das Python Module mit folgendem Befehl installiert werden.
```
$ sudo apt-get install python-smbus
```
Anschließend kann dieses Modul verwendet werden um lesend und schreibend via I2C auf den EEprom zuzugreifen. Anhand des ausgelesenden EEprom Inhalts wird die conrad URL durch die URL "www.raspberrypi.org" ersetzt. Ohne weitere Details zu dem Füllbyte (0x08) und den abschließenden Bytes (0x00, 0x13 und 0xA0) werden diese übernommen.

1. Am Begin werden die verwendeten Module (sys, time und smbus) eingebunden. Anschließend wird der verwendete I2C Bus (i2c_dev 1) und die 7-bit Addresse des EEproms 0x50 festgelegt. Darauf folgende werden zwei Hilfsvariablen reg (Laufvariable für das EEprom Register) und ret für die Rückgabewerte initialisiert. Im Letzten Schritt wird eine Instanz von SMBus mit dem verwendeten I2C Bus angelegt.
```python
import sys, time, smbus
#define used iic bus of rpi
iic_bus = 1
#define chip addrss, get with i2cdetect -y 1
iic_addr = 0x50
#EErom register
reg=0x00
#return value
ret=[]
#init smbus
eeprom = smbus.SMBus(iic_bus)
```
2. Der zweite Abschnitt beginnt mit der Definition der Startadresse im EEprom (0x18, siehe eeprom_dump.txt). Anschließend wird ein array bestehend aus der hexadezialen Repräsentation der URL **"www.raspberrypi.org"** angelegt. Die beiden weiteren Variablen enthalten das Füllbyte und die drei abschließenden Bytes.
```python
start=0x18
#data="www.raspberrypi.org"
data = [0x77,0x77,0x77,0x2e,0x72,0x61,0x73,0x70,0x62,0x65,0x72,0x72,0x70,0x69,0x2e,0x6f,0x72,0x67]
data1 =0x08
data2=[0x00, 0x13, 0xA0]
```
3. Im dritten Abschnitt wird der EEprom beschrieben, dazu wird zuerst die verwendete I2C-Adresse ausgegeben. Anschließend wird in einer Schleife der Inhalt des data Arrays (enthält die URL) beginnend bei der Startadresse in das EEprom geschrieben. Um den EEprom Zeit zu geben, wird nach jedem Byte 100ms gewartet. (Die Zeit habe ich wilkürlich gewählt, ohne Pause gibt es aber einen IO-Error.) Nach Abschluss der ersten Schleife wird das Füllbyte (0x08) und darauffolgende die URL in der zweiten Schleife in das EEprom geschrieben. Das Startbyte für die Zweite Adresse habe ich aus dem original EEprom dump entnommen. Auch ein direktes aneinander fügen, führte zum gleichen Ergebnis.
Am Ende werden noch die drei abschließenden Bytes ins EEprom geschrieben.
```python
print("Try to write to eeprom 0x%02X" % iic_addr)

try:
 #first loop for url
 for i in range(len(data)):
   eeprom.write_byte_data(iic_addr,start+i,data[i])
   time.sleep(0.1)

 eeprom.write_byte_data(iic_addr,start+len(data),data1)
 time.sleep(0.1)

 start = 0x31  #start+len(data)+1
 #second loop
 for i in range(len(data)):
   eeprom.write_byte_data(iic_addr,start+i,data[i])
   time.sleep(0.1)

 start = start+len(data)

 for i in range(len(data2)):
   eeprom.write_byte_data(iic_addr,start+i,data2[i])
   time.sleep(0.1)

except IOError, err:
  print("Error during communication with Device: 0x%02X" % iic_addr)
  exit(-1)
time.sleep(0.1)
```
4. Im vierten Abschnitt wird der neubeschriebene Inhalt nocheinmal ausgelesen und ausgegeben.
```python
for i in range(0,255):
 try:
  ret.append(eeprom.read_byte_data(iic_addr, reg+i))
 except IOError, err:
  print("Error during communication with Device: 0x%02X" % iic_addr)
  exit(-1)

print(ret)
out=""
for item in ret:
 out+="%c"%item

print(out)
```
Zur Kontroller nocheinmal den Inhalt des EEprom ausgeben.
```
$ i2cdump -y 1 0x50 >new_eeprom_dump.txt
$ cat new_eeprom_dump.txt
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef
00: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
10: 54 4f 4e 54 45 58 7e 05 77 77 77 2e 72 61 73 70    TONTEX~?www.rasp
20: 62 65 72 72 70 69 2e 6f 72 67 08 77 77 77 2e 72    berrpi.org?www.r
30: 61 73 70 62 65 72 72 70 69 2e 6f 72 67 00 13 a0    aspberrpi.org.??
40: 6f 6e 72 61 64 2e 63 6f 6d 00 13 a0 ff ff ff ff    onrad.com.??....
50: 00 13 a0 ff ff ff ff ff ff ff ff ff ff ff ff ff    .??.............
60: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
70: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
80: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
90: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
a0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
b0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
c0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
d0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
e0: ff ff 00 ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
f0: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
pi@noopi:~$

```

## Ergebnis
Nachdem das EEprom nun einen neuen Inhalt erhalten hat, muss natürlch versucht werden, ob diese URl auch ausgegeben wird. Dazu den WebKey mit den angelöteten Leitungen vom Raspberry Pi trennen und via USB anschließen.
Kurz den Button betätigt und ... die Ernüchterung folgt. Es erfolgt folgende Ausgabe

```sh
$http--
-bash: http--: command not found
```

Das erste Fazit lautet also, ein einfaches Überschreiben der URL im EEprom führt nicht dazu, dass diese korrekt ausgegeben wird. Dabei ist es egal ob die beiden URLs die selbe Startadressen wie im Original haben, oder direkt aneinander gekettet ins EEprom geschrieben werden. Es ist also noch etwas Analyseaufwand hinsichtlich der Funktionsweise nötig, evtl. handelt es sich bei den letzten beiden Bytes um eine Prüfsumme (z.b. crc16) oder Ähnliches.

Dazu fehlt mir aktuell aber die Zeit. Sobald ich aber etwas neues probiert habe, werde ich es hier aufschreiben.

Gut zu Wissen ist zumindest, dass man vor diesen "Geschenken" unter Linux (vorerst) gut geschützt ist.


