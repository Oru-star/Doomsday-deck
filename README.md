# Doomsday Deck

**A custom portable cyberdeck for computing, offline communication, electronics, and field experimentation.**

## Enclosure and Carrier Renders

These four renders show the overall enclosure concept and the carrier board from both sides.

<table width="100%">
  <tr>
    <td colspan="2" align="center">
      <a href="IMAGES/FRONT-RENDER.png"><img src="IMAGES/FRONT-RENDER.png" alt="Doomsday Deck enclosure — front render" width="100%"></a><br>
      <strong>Enclosure — Front</strong>
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <a href="IMAGES/BACK-RENDER.png"><img src="IMAGES/BACK-RENDER.png" alt="Doomsday Deck enclosure — back render" width="100%"></a><br>
      <strong>Enclosure — Back</strong>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <a href="IMAGES/FRONT-CARRIER.png"><img src="IMAGES/FRONT-CARRIER.png" alt="Doomsday Deck carrier board — front render" width="100%"></a><br>
      <strong>Carrier Board — Front</strong>
    </td>
    <td width="50%" align="center">
      <a href="IMAGES/BACK-CARRIER.png"><img src="IMAGES/BACK-CARRIER.png" alt="Doomsday Deck carrier board — back render" width="100%"></a><br>
      <strong>Carrier Board — Back</strong>
    </td>
  </tr>
</table>

## What Is It?

Doomsday Deck is a custom-built, portable cyberdeck which is mde for daily computing,offline computation, and electronics experimentation all in one!!. The design uses a Orange pi zero 3w as the main sbc,7inch Display,Custom Mechanical keyboard,20000 mah battery system,RTL Sdr,A lora module,External 20Gpio pins for adding external devices or tinkering with other hardware....

## Why I Built It

I Always find out the Cyberdecks to be so cool and i used to saw lots of videos releated to it and i always wanted to build one for my self , so when i got my RTL sdr and wanted to use it on daily basis, because of my Gaming laptop i was not able to use it properly so i thought why not make a Deck which will satisfy all my needs [SATTELITE COMMUNICATION , ELECTRONICS ] So i built it , this is totally made on my own flawour and all the parts used are the one i will really use on my daily basis and for sure this will be my daily driver..

## Design Breakdown

The images below are kept smaller so each design view can sit beside its explanation. Click an image to open it at full size!!!

### Carrier PCB Layouts

<table>
  <tr>
    <td width="50%" align="center" valign="top">
      <a href="IMAGES/C-PCB1.png"><img src="IMAGES/C-PCB1.png" alt="Carrier PCB layout — view 1" width="100%"></a><br>
      <em>C-PCB1</em>
    </td>
    <td valign="top">
      <strong>Carrier PCB — routing and placement view</strong><br><br>
      This view shows the component placement, connectors, mounting holes, board outlines, and routed connections on the carrier PCB.The carrier board is a four layer pcb , first layer consisting the Signal+Power, the second layer is the whole Ground layer where all the gnd connections of all the components are grounded up third layer too is Signal+Power , but i tried to use very few connections in the third layer because this is one of my starter pcb and lots of thing could go wrong so i keep very less signal traces in the third layer to make debugging simpler , fourth and the last layer is Signal only this has all the remaining important traces routed and if anything goes wrong we can easily diagnose the board easily .
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <a href="IMAGES/CPCB2.png"><img src="IMAGES/CPCB2.png" alt="Carrier PCB layout — view 2" width="100%"></a><br>
      <em>CPCB2</em>
    </td>
    <td valign="top">
      <strong>Carrier PCB —UPS HAT'S CONNECTION WITH THE CARRIER BOARD</strong><br><br>
      A second view of the carrier-board Shows the 3d model of the ups hat mechanically aligning to the carrier board which is clearly not made for it instead the UPS HAT is made for a rasberry pi 5 so by making a custom footprint by myself i managed to mechanically align the POGO pins of the UPS HAT to the pads of my carrier board , thanks to the good documentation of the waveshare , i managed to get all the mechanical knowledge abt the UPS HAT and using their original step file i managed to pin the position's of the pins and made the footprint which works perfectly fine with our carrier board
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <a href="IMAGES/C-PCB3.png"><img src="IMAGES/C-PCB3.png" alt="Carrier PCB layout — view 3" width="100%"></a><br>
      <em>C-PCB3</em>
    </td>
    <td valign="top">
      <strong>Carrier PCB -INTERNAL USB HUB</strong><br><br>
      this is one of the most hard part for me in this project , cause it was my first time integrating any ic in my project and frist time desigining the schematics around it , this is a custom made internal usb hub powered by the UPS HAT i previously mentioned abt , the data lines are directly connected to the Orange pi using the type c pins and the Orange pi and the carrier board / ic shares same gnd so it becomes easy to borrow the current from the UPS instead of getting it from the orange pi !!
    </td>
  </tr>
</table>

### Enclosure and Internal Arrangement

<table>
  <tr>
    <td width="50%" align="center" valign="top">
      <a href="IMAGES/BASE-DECK.png"><img src="IMAGES/BASE-DECK.png" alt="Doomsday Deck base assembly" width="100%"></a><br>
      <em>Base Deck</em>
    </td>
    <td valign="top">
      <strong>Base deck and component packaging</strong><br><br>
      The base model shows how all the internal components are alligned inetrnally , there are not all the step files in the screenshot but there are more compontents like the lora module , speakers , battery are on the opposite side , i also made the space for the ventilation so that the internals of the deck remains cool though the orange pi has the heat sink + fan but still with three in total fans , i think everythning will remain cooler under the load !!
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <a href="IMAGES/UPPER-FRONT-BASE-DECK.png"><img src="IMAGES/UPPER-FRONT-BASE-DECK.png" alt="Doomsday Deck upper front and base assembly" width="100%"></a><br>
      <em>Upper Front / Base</em>
    </td>
    <td valign="top">
      <strong>Upper-front and base fit</strong><br><br>
      This view is intended to show how the upper-front structure interfaces with the base. Check hinge, display support, enclosure wall thickness...
    </td>
  </tr>
</table>

### Features

| Feature | Purpose |
|---|---|
| **Orange Pi Zero 3W compute platform** | Main computing board for local tools and portable Linux use. |
| **Offline reference library** | Access documentation and reference material without an internet connection. |
| **LoRa communication** | Low-data-rate messaging using a Waveshare SX1262-based module; range depends on antenna, terrain, configuration, and local radio rules. |
| **20-pin GPIO expansion** | Expose SBC GPIO and expansion interfaces for add-on electronics. |
| **2.13-inch tri-colour e-paper display** | Low-power status or reference display. |
| **Scroll encoder and joystick** | Navigation, shortcuts, and pointer-style input. |
| **RTL-SDR Blog V3** | Receive-only RF experimentation using a USB-connected software-defined radio. |
| **Two 5 V 40 × 40 × 10 mm fans** | Move air through the enclosure and help manage temperatures. |
| **Two 8ohms 2w Electromagnetic Speakers** | for good audio... |

## Bill of Materials

See [`BOM.csv`](BOM.csv) for the parts list, vendor links, and budget estimate.
## Repository Structure

```text
Doomsday-deck/
├── Assets/                  # Project assets
├── carrier-orange pi zero 3w/  # Carrier-board design files
├── FIRMWARE/                # Firmware and configuration files
├── IMAGES/                  # Renders, PCB views, and reference images
├── PCB's/                   # PCB project files
├── step's n render's/       # CAD exports and additional renders
├── BOM.csv                  # Parts list and budget estimate
└── README.md                # Project overview and documentation
```

## Acknowledgements

A special thank you to **[Hack Club (Forge)](https://hackclub.com/)** for sponsoring the **Doomsday Deck** project and supporting me in hardware design, electronics, and open-source engineering.