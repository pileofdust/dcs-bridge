# DCS Bridge

![GitHub last commit](https://img.shields.io/github/last-commit/pileofdust/dcs-bridge)
[![Tests Status](https://github.com/pileofdust/dcs-bridge/workflows/latest/badge.svg?branch=main&event=push)](https://github.com/pileofdust/dcs-bridge/actions?query=workflow%3Alatest+branch%3Amain+event%3Apush)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/pileofdust/dcs-bridge)
![GitHub](https://img.shields.io/github/license/pileofdust/dcs-bridge?color=green)

Bridging the gap between supporting tools and DCS, Virtual Reality and the Real World.

The full and immersive DCS experience usually includes a number of supporting applications and tools for
mission planning, kneeboard generation, campaign status and team communication.
In VR it is especially challenging to stitch all this together without breakin immersion by going back to
the real world with the mouse and the keyboard.

DCS Bridge is a tool to help stitch it all together, making it possible to stay in the virtual world
the whole sortie and between sorties. The tool will also help with loading the mission plan into the
aircraft mission computer while we are waiting for ED to implement the data cartridge functionality.

Currently, the tool only supports the F-16, but can easily be extended to support other airframes.

### Installation
- Make sure you have Python 3.9+ installed
- Make sure you have DSC-BIOS installed and running
- Download the latest release or build from the releases section on the right. For single executable file
    choose the _dcsbridge.pyc_ asset
- Place the file in the desired folder
- Run the commands below from a terminal window or VoiceAttack to interact with the aircraft in DCS

### Load a mission plan from CombatFlite excel template
```
> dcsbridge.pyc mission [--default-bingo DEFAULT_BINGO] <file>

positional arguments:
  file      path to excel file with mission plan

optional arguments:
  --default-bingo DEFAULT_BINGO     default bingo value if mission from mission plan
```

### Load steerpoints from DCS Scratchpad
```
> dcsbridge.pyc scratchpad [file]

optional arguments:
  file  file where DCS Scratchpad coordinates are stored, defaults to 0000.txt in default Scratchpad folder
```

### Load steerpoints from supplied Aerodrome data
Included are the Aerodrome data from Minsky's excellent kneeboards: https://www.digitalcombatsimulator.com/en/files/3312200/
```
> dcsbridge.pyc aerodrome {caucasus,nevada,syria,pg,mariana} <id>

positional arguments:
  {caucasus,nevada,syria,pg,mariana}    name of map to use
  id                                    id of aerodrome to load
```

### Load steerpoints from list of aerodromes or objectives (e.g. BlueFlag)
```
> dcsbridge.pyc index [--columns COLUMNS] <file> <index>

positional arguments:
  file        path to data file
  index       index value of entry to load

optional arguments:
  --columns COLUMNS, --cols COLUMNS
              list of data column number in the format id,coordinates,altitude
```

### Set bingo value
```
> dcsbridge.pyc bingo <bingo>

positional arguments:
  bingo       bingo value to set in airframe
```

### Set time to the current real world time
```
> dcsbridge.pyc time {local}

positional arguments:
  {local}     timezone to use when entering current time
```
