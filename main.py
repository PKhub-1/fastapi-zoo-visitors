import asyncio
from io import BytesIO
from urllib.error import URLError
from urllib.request import Request, urlopen
from zipfile import BadZipFile

from fastapi import FastAPI, HTTPException
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

app = FastAPI(
    title="Zoo Visitors API",
    description="สถิติผู้เข้าชมสวนสัตว์จากชุดข้อมูลภาครัฐ Data.go.th",
    version="1.0.0",
)

DATASET_URL = "https://data.go.th/dataset/zoo-visitors2569"
RESOURCE_ID = "0ecc96cf-d914-42a1-b184-dbbd013c3c9c"
RESOURCE_URL = (
    "https://data.go.th/dataset/970c2632-1669-44aa-80c5-2c20cb2295e4/"
    "resource/0ecc96cf-d914-42a1-b184-dbbd013c3c9c/download/-.-..69.xlsx"
)


def _read_statistics() -> list[dict[str, object]]:
    request = Request(RESOURCE_URL, headers={"User-Agent": "ZooVisitorsAPI/1.0"})
    with urlopen(request, timeout=20) as response:
        workbook_data = response.read()

    workbook = load_workbook(BytesIO(workbook_data), data_only=True, read_only=True)
    try:
        if "statistics" not in workbook.sheetnames:
            raise ValueError("The source workbook does not contain a statistics sheet.")

        rows = workbook["statistics"].iter_rows(values_only=True)
        headers = next(rows, None)
        if not headers or not any(header is not None for header in headers):
            raise ValueError("The source workbook has no statistics column headers.")

        column_names = [
            str(header).strip() if header is not None else None for header in headers
        ]
        statistics = []
        for row in rows:
            record = {
                name: value
                for name, value in zip(column_names, row)
                if name is not None
            }
            if any(value is not None for value in record.values()):
                statistics.append(record)

        if not statistics:
            raise ValueError("The source workbook contains no statistics records.")
        return statistics
    finally:
        workbook.close()


@app.get("/api/zoo-visitors", summary="สถิติผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569")
async def get_zoo_visitors() -> dict[str, object]:
    try:
        statistics = await asyncio.to_thread(_read_statistics)
    except (URLError, TimeoutError, OSError, BadZipFile, InvalidFileException, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"ไม่สามารถอ่านข้อมูลจาก Data.go.th ได้: {exc}",
        ) from exc

    return {
        "source": "Data.go.th — องค์การสวนสัตว์แห่งประเทศไทย ในพระบรมราชูปถัมภ์",
        "dataset": "zoo-visitors2569",
        "dataset_url": DATASET_URL,
        "resource_id": RESOURCE_ID,
        "fiscal_year": 2569,
        "record_count": len(statistics),
        "statistics": statistics,
    }
