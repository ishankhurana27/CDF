import pandas as pd
from io import BytesIO

def dms_to_decimal(coord_str: str) -> float:
    try:
        dms, direction = coord_str.strip().split()
        degrees, minutes, seconds = map(float, dms.split(":"))
        decimal = degrees + minutes / 60 + seconds / 3600
        if direction in ("S", "W"):
            decimal *= -1
        return round(decimal, 6)
    except Exception as e:
        raise ValueError(f"Invalid coordinate format: {coord_str}")

def convert_to_cdf(json_data: dict) -> dict:
    return {
        "latitude": float(json_data["latitude"]),
        "longitude": float(json_data["longitude"]),
        "speed": float(json_data["speed"]),
        "bearing": float(json_data["bearing"]),
        "course": float(json_data["course"]),
        "sys_trk_no": int(json_data["sys_trk_no"]),
        "location": f'POINT({json_data["longitude"]} {json_data["latitude"]})',
        "raw_data": json_data
    }

def convert_to_cdf_from_csv_row(row: dict) -> dict:
    return {
        "latitude": dms_to_decimal(row["Lat / Lat Origin"]),
        "longitude": dms_to_decimal(row["Long / Long Origin"]),
        "speed": float(row["Speed Kts / Spare"]),
        "bearing": float(row.get("Course Deg / Bearing Deg", 0)),
        "course": float(row.get("Course Deg / Bearing Deg", 0)),
      # "sys_trk_no": int(row["Trk Display Num"]),
        #"location": f'POINT({dms_to_decimal(row["Long / Long Origin"])} {dms_to_decimal(row["Lat / Lat Origin"])})',
        "raw_data": dict(row)
    }

def parse_structured_file(file) -> pd.DataFrame:
    filename = file.filename.lower()
    file.file.seek(0)
    if filename.endswith(".csv"):
        return pd.read_csv(BytesIO(file.file.read()))
    elif filename.endswith(".tsv"):
        return pd.read_csv(BytesIO(file.file.read()), sep="\t")
    elif filename.endswith(".xlsx"):
        return pd.read_excel(BytesIO(file.file.read()))
    else:
        raise ValueError("Unsupported file format")
