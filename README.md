# pygame-pathfinder

Project I made when I was first starting with python.

|     |     |
| --- | --- |
| <img src="https://user-images.githubusercontent.com/76220140/112721168-77c35880-8f3d-11eb-8d6f-d9f5f63eae18.png" />|<img src="https://user-images.githubusercontent.com/76220140/112721170-7a25b280-8f3d-11eb-948a-3247f3b5e65e.png" />|

|     |     |
| --- | --- |
| <img src="https://user-images.githubusercontent.com/76220140/112721172-7e51d000-8f3d-11eb-95d0-fc15d538df82.gif" />|<img src="https://user-images.githubusercontent.com/76220140/112721172-7e51d000-8f3d-11eb-95d0-fc15d538df82.gif" />|

# Algorithm 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To be honest I was just messing around here and just coming up with ridiculous ideas. In my opinion this application takes a lot of shts to run because I really did not consider the efficiency of the algorithm.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;What I did to generate the growing and surrounding blocks thingy was get the coordinates (x, y) of either top, bottom, left, right and its corresponding adjacent corner, then make it as a basis to where I should put the border of the block. Then from there, if the border hits the other block, it will keep the coordinates of the border block that collided with the other block, then it will start making a path from the starting coordinates to the coordinates of the border block where it collided.

<p align="center">
  <img src="https://user-images.githubusercontent.com/76220140/112721178-80b42a00-8f3d-11eb-9f9d-b7f9f8c0843f.gif" />
</p>
