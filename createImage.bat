@echo off
magick bones.png -size 275x372 ^
-background none -fill white -font Impact -gravity north -pointsize 30 ^
caption:"ME WAITING" -trim ^
( +clone -background black -shadow 200x2+0+0 ) +swap -background none ^
-gravity south ^
caption:@- -trim ^
( +clone -background black -shadow 200x2+0+0 ) +swap -background none -layers merge +repage ^
image.jpg