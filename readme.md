### Introduction

s22rgb mean sentinel 2 to rgb image.

The technical route is as follows:

1. Obtain the ZIP file list

2. The for loop runs iteratively and decompresses a single ZIP

3. Obtain the list of files in JP2 format, which corresponds to TIFF files of other remote sensing satellites

4.GDAL reads jp2 file, numpy calculates linear transformation, here using 2% linear transformation

5. Recombine it into a three-band matrix and save it as a common JPG format through OpencV

[![h7BBf1.png](https://z3.ax1x.com/2021/09/08/h7BBf1.png)](https://imgtu.com/i/h7BBf1)



win10 quick install and use:

```
pip install s22rgb -i https://pypi.python.org/simple
```

[![h7hTc4.jpg](https://z3.ax1x.com/2021/09/08/h7hTc4.jpg)](https://imgtu.com/i/h7hTc4)

usage:

[![hHecHe.jpg](https://z3.ax1x.com/2021/09/08/hHecHe.jpg)](https://imgtu.com/i/hHecHe)