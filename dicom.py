import numpy as np # linear algebra
import SimpleITK as sitk
import tempfile
import os

def read_series(foldername) :
    try :
        print("Run read_series()")
        # Read the DICOM series
        series_reader = sitk.ImageSeriesReader()
        dicom_names = series_reader.GetGDCMSeriesFileNames(foldername)
        series_reader.SetFileNames(dicom_names)

        # Load the series and convert to array
        series = series_reader.Execute()
        series_array = sitk.GetArrayFromImage(series)
        return series_array
    except Exception as e :
        print("read_series() function get error :", e)

def downsampling(series_array, factor) :
    try :
        print("Run downsampling()")
        # For performance reasons, you might want to downsample your volume
        # if the full resolution is not required for the visualization
        series_downsampled = series_array[::factor, ::factor, ::factor]
        return series_downsampled
    except Exception as e :
        print("downsampling() function get error :", e)

def change_angle(series_downsampled, style) :
    try :
        print("Run change_angle()")
        if style == 0 :
            series_downsampled = np.transpose(series_downsampled, (0,1,2))
        elif style == 1 :
            series_downsampled = np.transpose(series_downsampled, (0,2,1))
        elif style == 2 :
            series_downsampled = np.transpose(series_downsampled, (1,0,2))
        elif style == 3 :
            series_downsampled = np.transpose(series_downsampled, (1,2,0))
        elif style == 4 :
            series_downsampled = np.transpose(series_downsampled, (2,0,1))
        elif style == 5 :
            series_downsampled = np.transpose(series_downsampled, (2,1,0))
        return series_downsampled
    except Exception as e :
        print("change_angle() function get error :", e)

def get_axis_series(series_downsampled, threshold) :
    try :
        print("Run get_axis_series()")
        x, y, z = np.where(series_downsampled > threshold)
        return x, y, z
    except Exception as e :
        print("get_axis_series() function get error :", e)

# if __name__ == "__main__" :
#     read_series_from_azure("dicom_lung")
    # read_series("./mount/dicom_lung")