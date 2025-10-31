# Sierpinski Triangle Generator

This repository provides a small command-line program for creating Sierpinski triangle fractals as SVG images.

## Requirements

- Python 3.9 or newer (only the Python standard library is used).

## Usage

Run the script with Python and specify the desired options. The example below generates an order-4 triangle with a side length of 200 units and writes it to `sample.svg`:

```bash
python test.py --order 4 --side-length 200 --output sample.svg
```

After the command finishes, open `sample.svg` in any web browser or vector graphics viewer to see the fractal.

### Additional options

- `--order`: recursion depth (default: 6)
- `--side-length`: side length of the base triangle in SVG units (default: 800)
- `--fill`: fill color for the triangles (default: `#1f77b4`)
- `--background`: background color of the canvas (default: `white`)
- `--output`: path to the generated SVG file (default: `sierpinski_triangle.svg`)

If you run the script without arguments, it uses the defaults and creates `sierpinski_triangle.svg` in the current directory:

```bash
python test.py
```

The script prints the absolute path of the generated file when it completes.
