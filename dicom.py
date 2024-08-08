import numpy as np # linear algebra
import SimpleITK as sitk
from azure.storage.fileshare import ShareDirectoryClient, ShareFileClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import tempfile
import os

account_name = "amldevelopment2198817292"
account_key = "c8Uq0oz26wsfynCqhEXjnElvk2FlbkNAosg+DMk5Bbs4OWtle634Ur1r5OqJCoZhdv9VK1OE6VhZ+AStvWgA6A=="
container_name = "phe-dicom-dataset"

def read_series_from_azure(foldername) :
    try :
        print("Run read_series_from_azure()")
        # Create a BlobServiceClient
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net/",
            credential=account_key
        )

        # Create a ContainerClient
        container_client = blob_service_client.get_container_client(container_name)

        # Create a temporary directory to store the downloaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            # List blobs in the directory
            blob_list = container_client.list_blobs(name_starts_with=foldername)

            # Download each blob to the temporary directory
            for blob in blob_list:
                blob_client = container_client.get_blob_client(blob)
                download_file_path = os.path.join(temp_dir, os.path.basename(blob.name))
                print(f"Downloading blob: {blob.name} to {download_file_path}")
                with open(download_file_path, "wb") as download_file:
                    download_file.write(blob_client.download_blob().readall())
                print(f"Downloaded blob: {blob.name}")

            # Run the SimpleITK code with the local directory path
            series_reader = sitk.ImageSeriesReader()
            dicom_names = series_reader.GetGDCMSeriesFileNames(temp_dir)
            series_reader.SetFileNames(dicom_names)
            image = series_reader.Execute()

            # Process the image as needed
            print(f"Image size: {image.GetSize()}")

        # Load the series and convert to array
        series = series_reader.Execute()
        series_array = sitk.GetArrayFromImage(series)
        return series_array
    except Exception as e :
        print("read_series_from_azure() function get error :", e)

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

if __name__ == "__main__" :
    read_series_from_azure("dicom_lung")
    # read_series("./mount/dicom_lung")