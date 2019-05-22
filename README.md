# Pascal's Gif
As if math wasn't scary enough already!

This project makes 👻spooky👻 gifs by utilizing some interesting patterns that appear in binary representations of pascals triangle

## Prior Art
This program attempts to remake a gif I found from wikipedia.
The image can be found at:

![orig_gif](https://upload.wikimedia.org/wikipedia/commons/6/66/Pascal%27s_Triangle_animated_binary_rows.gif)

https://upload.wikimedia.org/wikipedia/commons/6/66/Pascal%27s_Triangle_animated_binary_rows.gif

The gif came with the following decription:

```Each frame represents a row in Pascal's triangle.
Each column of pixels is a number in binary with the least significant bit at the bottom.
Light pixels represent ones and the dark pixels are zeroes.
```

It took alot of exparamenting to get close to what the gif shows but the final product is close enough for me.

## How to Run

### Step 1. Clone Repo
```
git clone https://github.com/geooff/pascals_gif.git
```

### Step 2. Make venv
_Optional but recommended_
``` 
cd pascals_gif
python3 -m venv .
source bin/activate
```

### Step 3. Install requirements
```
pip install -r requirements.txt
```

### Step 4. Run program
Recommended parameters
```
python3 pascal_gif.py --num_frames 88 --pixel_dim 50 50
```

#### Exparamenting
To run the following parameters are required:
* num_frames: The total number of frames of the output gif (eg. 120)

Optional Parameters:
* frame_rate: The speed of the gif. Default: 0.5
* pixel_dim: Number of pixels contained in frame. Default 50x50
* frame_dim: Number of pixels contained in output. Default 400x400
* interpol: Round edges when upscaling frames (extra sp00ky)

## Sample Result

![Example](README_resources/pascals_triangle_88.gif)

The gif generated above used the following metadata:
* 50x50 pixel layout
* Upscales to 400x400
* 0.5s Frame timing
* 88 Frames

![Example_Interpol](README_resources/pascals_triangle_88_interpol.gif)

The gif generated above used the following metadata:
* 50x50 pixel layout
* Upscales to 400x400
* 0.5s Frame timing
* 88 Frames
* Interpolate = True

## Interpolate

The Pillow Image library in python allows for interpolation when upscaling. This can be used to make an interesting effect. To enable this behaviour utalize the flag
```
--interpol
```