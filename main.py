from dicom import *
from fastapi import FastAPI, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from config.settings import settings

app = FastAPI()

API_KEY="0PfSuTqMuPrKPrJLs9IblYvzslI4u9GsgcayLVSaD4reu79gq1DFv1rRuw7GXqF2i5rsWS25oGJcmS7tJjPk39qSDA2NEcesVmkktPMH0cj5Y9Pl22gb3IFXyrAlxcgn"

api_key = APIKeyHeader(name="api-key", auto_error=False)

folder_ddr = "dicom_ddr"
folder_lung = "dicom_lung"
folder_mri = "dicom_mri"

def get_api_key(
    api_key: str = Security(api_key),
) -> str:
    """Retrieve and validate an API key from the query parameters or HTTP header.

    Args:
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

class Item(BaseModel):
    downsampling_factor: int
    angle_style: int
    threshold: int
    data : dict

@app.get("/process_dicom/ddr/", response_model=Item)
async def process_dicom(downsampling_factor: int, angle_style: int, threshold: int, api_key: str = Security(get_api_key)) :
    try :
        series_array = read_series(settings.DDR_PATH)
        series_downsampled = downsampling(series_array, downsampling_factor)
        series_downsampled = change_angle(series_downsampled, angle_style)
        x, y, z = get_axis_series(series_downsampled, threshold)
        clean_dicom = {
            "downsampling_factor" : downsampling_factor,
            "angle_style" : angle_style,
            "threshold" : threshold,
            "data" : {
                "x" : x.tolist(),
                "y" : y.tolist(),
                "z" : z.tolist()
            }
        }
        return clean_dicom
    except Exception as e :
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/process_dicom/ddr_truncate/", response_model=Item)
async def process_dicom_truncate(downsampling_factor: int, angle_style: int, threshold: int, api_key: str = Security(get_api_key)) :
    try :
        series_array = read_series(settings.DDR_TRUNC_PATH)
        series_downsampled = downsampling(series_array, downsampling_factor)
        series_downsampled = change_angle(series_downsampled, angle_style)
        x, y, z = get_axis_series(series_downsampled, threshold)
        clean_dicom = {
            "downsampling_factor" : downsampling_factor,
            "angle_style" : angle_style,
            "threshold" : threshold,
            "data" : {
                "x" : x.tolist(),
                "y" : y.tolist(),
                "z" : z.tolist()
            }
        }
        return clean_dicom
    except Exception as e :
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/process_dicom/lung/", response_model=Item)
async def process_dicom(downsampling_factor: int, angle_style: int, threshold: int, api_key: str = Security(get_api_key)) :
    try :
        series_array = read_series(settings.LUNG_PATH)
        series_downsampled = downsampling(series_array, downsampling_factor)
        series_downsampled = change_angle(series_downsampled, angle_style)
        x, y, z = get_axis_series(series_downsampled, threshold)
        clean_dicom = {
            "downsampling_factor" : downsampling_factor,
            "angle_style" : angle_style,
            "threshold" : threshold,
            "data" : {
                "x" : x.tolist(),
                "y" : y.tolist(),
                "z" : z.tolist()
            }
        }
        return clean_dicom
    except Exception as e :
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/process_dicom/mri/", response_model=Item)
async def process_dicom(downsampling_factor: int, angle_style: int, threshold: int, api_key: str = Security(get_api_key)) :
    try :
        series_array = read_series(settings.MRI_PATH)
        series_downsampled = downsampling(series_array, downsampling_factor)
        series_downsampled = change_angle(series_downsampled, angle_style)
        x, y, z = get_axis_series(series_downsampled, threshold)
        clean_dicom = {
            "downsampling_factor" : downsampling_factor,
            "angle_style" : angle_style,
            "threshold" : threshold,
            "data" : {
                "x" : x.tolist(),
                "y" : y.tolist(),
                "z" : z.tolist()
            }
        }
        return clean_dicom
    except Exception as e :
        raise HTTPException(status_code=400, detail=str(e))