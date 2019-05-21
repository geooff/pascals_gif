# Pascals Gif
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
Recommended parameters (160, 0.5)
```
python3 pascal_gif.py
```

## Limitaions 
The dimensions of the frame in pixel of the image must be a power of 10 (10x10, 100x100, ect..)
* This is due to how I choose to scale the images
* As a concequence of this I can't remake the original gif identically (It uses a frame of 50x50)

The edges of gifs generated are blurred, this was originally a bug but I decided I liked it
