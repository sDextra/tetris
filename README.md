# Tetris (Ren'Py)
![screenshot](https://pp.userapi.com/c849416/v849416003/dc39a/luZjOyp1dgg.jpg)

## Features
Different modes
- Classic - field 10x20, low speed, no bonus
- New - field 12x25, normal speed, with bonus
- Hard - field 13x25, high speed, with bonus 
- Impossible - field 15x26, high speed, no bonus, no I tetromino

## Installation
Add files to your Ren'Py project

## Init
```
row - field width
column - field height
speed - falling speed
tops - number of top places
level - level of difficulty
mode - presence of a bonus
impossible - without I tetromino
for_level - the number of lines for level-up
```

## Usage
**Keys**:
- Left Arrow - move tetromino to the left
- Right Arrow - move tetromino to the right
- Up Arrow - rotate tetromino
- Down Arrow - increasing the speed of falling (pressing again disables it)
- Enter - instantly lower tetromino
- Space - remove current tetromino (if you have a bonus)

## License
[MIT](https://github.com/sDextra/tetris/blob/master/LICENSE/).
