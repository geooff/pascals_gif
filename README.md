# Pascals Gif

## About
This program attempts to remake a gif I found from wikipedia.
The image can be found at:

https://upload.wikimedia.org/wikipedia/commons/6/66/Pascal%27s_Triangle_animated_binary_rows.gif

The gif came with the following decription:

```Each frame represents a row in Pascal's triangle.
Each column of pixels is a number in binary with the least significant bit at the bottom.
Light pixels represent ones and the dark pixels are zeroes.
```

It took alot of exparamenting to get close to what the gif shows but the final product is close enough for me.

## How to Run

### Step 1. Clone Repo

### Step 2. Make venv
_Optional but recommended_
``` 
cd ~~project_folder~~
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