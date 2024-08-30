from pydantic import BaseSettings
class Settings(BaseSettings):
    API_KEY: str
    DDR_PATH: str
    DDR_TRUNC_PATH: str
    LUNG_PATH: str
    MRI_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()
