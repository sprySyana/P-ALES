# Reflexions on the P-ALES project
In order to perfect the project, we must ask ourselves how to tacle the limitations that come with it. <br>
Here are some food for thoughts.
## Color limitations
### For humans
Human eyes are limited in their perception of color nuances, if the colors choosen are too close they will be perceived as similar. <br>
Neuromarketing expert Diana Derval tested that limitation and her results are :
   - 25% of the population sees under 20 color nuances, they're dischromate
   - around 50% of the population sees between 20 and 32 nuances
   - few sees between 33 and 39 nuances thanks to aving 4 photoreceptors (blue, green, red and orange-red)
   - screens are limited to à rendition of 35 nuances

The methodology used by Diana Derval is based on the diffraction of light spectrum, it's a flat representation of the color, <br>
whereas the P-ALES project treats colors as a 3D space (X=Red, Y=Green and Z=Blue).
### For screens
Each screen will render colors slightly differently, modifing the color nuance perceived by both the students and the teachers. <br>
Computer color rendition is limited by the quality of their screen and the power of their graphic card.
### Conclusion
Between the human and the screen limitation for color perception, <br>
if we can't attribute a unique color to each phonem, we'll have to use other means to differenciate phonems. <br>
One idea is to layer a design on top of a color to signify a variation like nasalisation, aspiration ... <br>
It would be beneficial to test the perception and capacity of differenciation of colors depending on the users, <br>
in order to know the optimal number of colors that we can use in order to avoid the problem of color-similarity. <br>
Knowing the maximum of color usable optimaly would show if the idea of making an all-langages color-phonem pairing algo if feasible and pertinent.
## Color attribution
### Current method
The method used is a descending algo were we are ajusting the positions of a cloud of points that each represents a phonem, <br>
relatively to each other, based on the frequency of the pair (frenquecy = distance from each other) inside the 3D cube of Colors (RGB).
#### Improvement ideas
implementing the calculation in 3 loops
   1.  rough placement
   2. refining the placement
   3. final ajustements
### Other methods
#### Inside the color cube
If we consider the use the RBG system of colors as a 3D square, we must remove some of the color possibilities for our color-phonem pairing : the triangle based pyramid in the RGB(0, 0, 0) corner. <br>
These colors, being too dark, will not be perceived by the users. <br>
We also could limit the use of the colors in the RGB(255, 255, 255) corner too, for their brightness. <br>
If we choose to do so, the optimal shape for our cloud of points will be almond-like. <br>
In the hypothesis that we have a definitive robust data for the frequecies of adjacent phonems pairs, <br>
we could force the 2 phonems of the highest frequency to be in diagonaly opposed corners :
   - the red : RGB(255, 0, 0) and the cyan : RGB(0, 255, 255)
   or
   - the blue : RGB(0, 0, 255) and the yellow : RGB(255, 255, 0)

and place other phonems using these two fixed positions.
#### Outside the color cube
In our current version we ask 2 complex tasks to our algo
   1. calculate the position of the points representing phonems, using the frequency as distance between pairs of points
   2. containing the cloud of points into a rather tiny space (the 255*255*255 color cube)

It might be easier to completely separate these two task into 2 full fledge algo working together. <br>
The fist placing each points relatively to each others without any boundary limitation : a "cloud spreading" algo. <br>
The second aplying the model by scaling it in order to respect the color-cube boundaries.



[//]: # (md How To : https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
