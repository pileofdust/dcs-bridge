# DCS Bridge
Bridging the gap between supporting tools and DCS, Virtual Reality and the Real World.

The full and immersive DCS experience usually includes a number of supporting applications and tools for
mission planning, kneeboard generation, campaign status and team communication.
In VR it is especially challenging to stitch all this together without breakin immersion by going back to
the real world with the mouse and the keyboard.

DCS Bridge is a tool to help stitch it all together, making it possible to stay in the virtual world
the whole sortie and between sorties. The tool will also help with loading the mission plan into the
aircraft mission computer while we are waiting for ED to implement the data cartridge functionality.

Currently, the tool only supports the F-16, but can easily be extended to support other airframes.

### Load a mission plan from CombatFlite excel template
```
> dcs-bridge mission [--default-bingo DEFAULT_BINGO] <file>

positional arguments:
  file      path to excel file with mission plan

optional arguments:
  --default-bingo DEFAULT_BINGO     default bingo value if mission from mission plan
```

### Load steerpoints from DCS Scratchpad
```
> dcs-bridge scratchpad [file]

optional arguments:
  file  file where DCS Scratchpad coordinates are stored, defaults to 0000.txt in default Scratchpad folder
```

### Load steerpoints from supplied Aerodrome data
Included are the Aerodrome data from Minsky's excellent kneeboards: https://www.digitalcombatsimulator.com/en/files/3312200/
```
> dcs-bridge aerodrome {caucasus,nevada,syria,pg,mariana} <id>

positional arguments:
  {caucasus,nevada,syria,pg,mariana}    name of map to use
  id                                    id of aerodrome to load
```

### Load steerpoints from list of aerodromes or objectives (e.g. BlueFlag)
```
> dcs-bridge index <file> <index>

positional arguments:
  file        path to data file
  index       index value of entry to load
```

### Set bingo value
```
> dcs-bridge bingo <bingo>

positional arguments:
  bingo       bingo value to set in airframe
```

### Set time to the current real world time
```
> dcs-bridge time {local}

positional arguments:
  {local}     timezone to use when entering current time
```
