# RoboBulls-MicroMouse
Webots Project for developing our code for the RoboBulls Team to compete in the MicroMouse Compition 

# Micromouse Maze Files and mazetool

All the maze are for the classic contest and so are 16x16 in size.

## File Formats

There are three types of maze file here, each in their own subdirectory.

### Binary
Binary mazes have the file extension `.maz` are exactly 256 bytes in size. Each byte holds the wall information for a single cell. Each wall is represented by one bit using the following masks:
```
    #define NORTH         (uint8_t)0x01
    #define EAST          (uint8_t)0x02
    #define SOUTH         (uint8_t)0x04
    #define WEST          (uint8_t)0x08
```
Thus, a cell with walls in the WEST and SOUTH directions would have the value 0x0C.

Note that internal walls are stored twice. If a cell has a wall to the East, the neighbour in that direction has a wall to the West. This redundancy greatly simplifies the use of the information and can be used to validate the maze data. When adding or removing a wall from the maze array, care must be taken to ensure both 'sides' get updated. 

A hex dump of a typical binary maze file, using the 'standard' format, looks like this:

```
 0E 0A 09 0C 0A 0A 0A 0A 0A 0A 08 0A 0A 0A 08 09
 0C 09 05 06 08 0A 0A 0A 0A 0B 06 0A 0A 0A 03 05
 05 05 05 0C 02 0B 0E 08 0A 0A 08 0A 08 08 09 05
 05 04 01 06 08 0A 09 04 0A 0A 00 0A 03 05 05 05
 05 05 04 09 06 09 05 04 0A 0A 02 0A 0B 05 05 05
 05 04 03 06 0A 02 03 06 0A 0A 0A 0A 09 05 05 05
 05 05 0D 0D 0D 0C 08 0A 0A 0A 0A 09 05 05 05 05
 06 03 04 01 04 01 05 0C 09 0C 08 01 05 05 05 05
 0C 08 01 06 01 05 04 02 03 05 05 05 05 05 05 05
 05 05 05 0D 06 01 05 0C 0A 01 05 05 05 05 05 05
 05 05 05 04 09 06 03 06 0A 02 00 03 05 04 03 05
 05 04 03 05 05 0C 0A 0A 08 09 04 0A 01 05 0D 05
 05 05 0D 05 05 04 0A 08 03 05 06 0A 03 05 04 01
 05 05 04 01 04 03 0C 02 0B 06 08 0A 0A 03 05 05
 05 06 01 07 06 08 02 0A 0A 0B 06 08 0A 0A 00 01
 06 0A 02 0A 0A 02 0B 0E 0A 0A 0A 02 0A 0A 03 07
```


### Text
Text mazes have the extension `.txt`. They are a directly printable view of the mazestored as ASCII text. For convenience, they have the start cell in the lower left corner. Printing a maze with a single character for each wall makes it very difficult to read because of the aspect ratio of typical printed text. The text files in this repository all use three characters for horizontal walls. The files all have at least 2178 characters. 

A text version of the maze data above looks like this:

```
o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o
|                                                               |
o   o---o---o---o---o---o---o---o---o---o---o---o   o---o   o---o
|       |                                   |                   |
o   o   o   o---o---o---o---o---o---o---o   o---o---o---o   o   o
|   |   |                                               |   |   |
o   o   o   o---o---o---o---o---o---o---o---o---o---o   o   o   o
|   |   |       |   |                               |   |   |   |
o   o   o   o   o   o   o---o---o---o---o---o   o   o   o   o   o
|   |   |   |   |   |   |                   |   |   |   |       |
o   o   o   o   o   o   o   o   o---o---o   o   o   o   o   o   o
|       |           |   |   |                       |       |   |
o   o---o   o   o   o   o   o   o---o---o   o---o---o   o---o   o
|   |   |   |   |   |   |   |               |           |   |   |
o   o   o   o   o   o   o   o---o---o   o   o   o---o---o   o   o
|   |   |   |   |   |   |   |       |   |   |       |   |   |   |
o   o   o   o   o   o   o   o   o   o   o   o   o   o   o   o   o
|   |   |               |   |       |       |   |       |   |   |
o   o   o   o---o---o---o   o---o   o---o---o   o   o   o   o---o
|   |   |   |           |                   |   |   |       |   |
o   o   o---o   o---o   o   o---o---o---o   o   o   o---o   o   o
|   |   |   |   |       |                   |           |       |
o   o   o   o   o   o   o---o   o---o   o---o---o---o   o   o   o
|   |       |       |   |               |                   |   |
o   o   o   o   o---o   o---o---o   o---o   o---o---o---o---o   o
|       |       |       |           |                       |   |
o---o---o---o---o   o---o---o   o---o---o---o---o---o   o---o   o
|                       |                       |               |
o   o---o---o   o---o   o---o---o   o---o---o   o---o---o   o   o
|   |                           |                           |   |
o   o   o---o---o---o---o---o   o   o---o---o---o---o---o---o   o
|   |                           |                               |
o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o---o
```
