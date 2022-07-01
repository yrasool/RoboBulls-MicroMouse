# RoboBulls-MicroMouse
Webots Project for developing our code for the RoboBulls Team to compete in the MicroMouse Compition 

# Webots Maze world files
Below is a reference to how the Maze Class interprates the world frame

```
Maze shape and index referance Top -> North & Right -> East
Each Cell is 180mm x 180mm

(0mm, 2880mm)                                     (2880mm, 2880m) 
ˇ                                                               ˇ
[  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15]
[ 16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31]
[ 32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47]
[ 48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63]
[ 64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79]        N
[ 80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95]        ˆ
[ 96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111]        |
[112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127]   W ‹--•--› E
[128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143]        |
[144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159]        ˇ
[160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175]        S
[176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191]
[192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207]
[208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223]
[224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239]
[240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255]
^                                                               ^
(0mm, 0mm)                                           (2880mm, 0m)

```

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
