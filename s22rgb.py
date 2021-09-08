from osgeo import gdal
import zipfile
import os
import cv2
import numpy as np

class S22rgb:
    def __init__(self, InputFilePath, OutputFilePath):
        self.InputFilePath = InputFilePath
        self.OutputFilePath = OutputFilePath
        self.zip = self.find_zip_image_file
        self.run()
    def run(self):
        '''
        批量运行
        The batch operation
        '''
        if len(self.zip()) != 0:
            for i in range(len(self.zip())):
                self.un_zip(self.zip()[i])
                SAFE_PATH = os.path.splitext(self.zip()[i])[0] + '.SAFE'
                file_dir = os.path.join( self.OutputFilePath, SAFE_PATH)
                imgfile, xml = self.get_file_name(file_dir)
                blue = self.read_jp2(imgfile[0])
                green = self.read_jp2(imgfile[1])
                red = self.read_jp2(imgfile[2])
                jpgfile = os.path.splitext(self.zip()[i])[0] + '.jpg'
                tarpath = os.path.join( self.OutputFilePath, jpgfile)
                self.rgb_jpg(red, green,blue , tarpath)

    def read_jp2(self,file):
        """
        读取jp2格式文件
        Read jp2 format files
        """
        IDataSet = gdal.Open(file)
        cols = IDataSet.RasterXSize
        rows = IDataSet.RasterYSize
        ImgBand = IDataSet.GetRasterBand(1)
        ImgRasterData = ImgBand.ReadAsArray(0, 0, cols, rows)
        return ImgRasterData

    def get_file_name(self, file_dir):
        """
        get jp2 file and MTD_TL.xml file
        :param file_dir: InputFilePath
        :return: Jp2 format list, mtd_tl. XML file
        """
        L = []
        xml = []
        for dirpath, dirnames, filenames in os.walk(file_dir):
            for file in filenames:
                if os.path.splitext(file)[1] == '.jp2':
                    if 'IMG_DATA' in dirpath:
                        if '_B' in os.path.splitext(file)[0]:
                            L.append(os.path.join(dirpath, file))
        for dirpath, dirnames, filenames in os.walk(file_dir):
            for file in filenames:
                if os.path.splitext(file)[0] == 'MTD_TL':

                    xml.append(os.path.join(dirpath, file))
        return L, xml[0]

    def find_zip_image_file(self):
        """
        This is the corresponding file to find zip
        :param inputpath: Destination folder
        :return:zip file list
        """
        inputpath  = self.InputFilePath
        os.chdir(inputpath)
        zip_fn = []
        for zip_name in os.listdir(inputpath):
            if zip_name.endswith('.zip'):
                zip_fn.append(zip_name)
        return zip_fn



    def un_zip(self,zippath):
        """Unpack"""
        zip_file = zipfile.ZipFile(zippath)
        zip_list = zip_file.namelist()
        for f in zip_list:
            zip_file.extract(f, self.OutputFilePath)  # Cycle unzip files to the specified directory

        zip_file.close()  # Close file, must have, free memory

    def translate(self, band, number = 2):
        """
        Convert the value of a band to the range 0-255
        2% linear conversion
        """
        # band_data = band.ReadAsArray(0, 0, cols, rows)
        # min = np.min(band)
        max = np.max(band)
        min = np.min(band)
        # nodata = band.GetNoDataValue()
        band = band.astype(np.float64)
        band[band == -9999] = np.nan
        band[band == 0] = np.nan

        band_data = band / max * 255
        # Convert nan in the data to a specific value, for example
        band_data[np.isnan(band_data)] = 0
        d2 = np.percentile(band_data, number)
        u98 = np.percentile(band_data, 100 - number)

        maxout = 255
        minout = 0

        data_8bit_new = minout + ((band_data - d2) / (u98 - d2)) * (maxout - minout)
        data_8bit_new[data_8bit_new < minout] = minout
        data_8bit_new[data_8bit_new > maxout] = maxout
        return data_8bit_new

    def globe_max_min_value(data, number=0):
        data[np.isnan(data)] = 0
        d2 = np.percentile(data, number)
        u98 = np.percentile(data, 100 - number)
        return u98, d2

    def rgb_jpg(self, band_red, band_green, band_blue, tarpath):
        """Generate RGB JPG images"""
        data_red = self.translate(band_red)
        data_green = self.translate(band_green)
        data_blue = self.translate(band_blue)
        datagray = cv2.merge([data_blue, data_green, data_red])
        # Sets the name of the output image
        cv2.imwrite(tarpath, datagray)


if __name__ == '__main__':
    img = 'G:\\'
    out = 'G:\sentinel'
    S22rgb(img, out)
