import shutil
import requests

from datetime import date, datetime
from typing import Literal, TypedDict
from enum import Enum


__version__ = "3.0"


class Manufacturer(Enum):
    pfizer = 1
    moderna = 2
    astrazeneca = 3
    janssen = 4
    sinovac = 5


class Vaccination(TypedDict):
    date: date
    manufacturer: Manufacturer


class QRCode(TypedDict):
    name: str
    birth: str
    vaccinations: list[Vaccination]


def generate(first_name: str, last_name: str, birth_date: str,  **vaccinations: Manufacturer) -> None:
    """
    Generate your vaccination QR code.

    Args:
        first_name (str): name of the vaccinated person
        last_name (str): surname of the vaccindate person
        birth_date (str): birthday of the vaccinated person in YYYY-MM-DD format
        **vaccinations (Manufacturer): vaccination information as date=manufacturer 

    Return: None
    """
    qr_code = QRCode(
        name=f"{first_name} {last_name}",
        birth=birth_date,
        vaccinations=[
            Vaccination(manufacturer=manufacturer, date=datetime.strptime(date, "%Y-%m-%d"))
            for date, manufacturer in vaccinations.items()
        ],
    )
    res = requests.get(
        f"http://api.qrserver.com/v1/create-qr-code/?data={qr_code}", stream=True
    )
    if res.status_code != 200:
        raise Exception("QR code cannot be generated by QR Code Generator API.")
    with open("qr_code.png", "wb") as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)
    print("QR code has been generated.")
