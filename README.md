# Zoo Visitors API

FastAPI service that reads the official fiscal-year-2569 XLSX resource from
[Data.go.th](https://data.go.th/dataset/zoo-visitors2569). The source workbook
([`zoo-visitors-2569.xlsx`](./zoo-visitors-2569.xlsx)) is included in the
repository so the deployed service does not depend on Data.go.th allowing
outbound downloads from its hosting provider. The returned `statistics` use the
source workbook's original column names and values; no visitor counts are
generated or hard-coded.

## Run locally

From the project directory, create and activate a virtual environment, then run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
fastapi dev main.py
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.
The API endpoint is [http://127.0.0.1:8000/api/zoo-visitors](http://127.0.0.1:8000/api/zoo-visitors).

## Test with Postman

Create a `GET` request to `http://127.0.0.1:8000/api/zoo-visitors` and send it.
The successful response is HTTP `200` with JSON. A source/network/workbook
failure is reported as HTTP `502`; the API does not silently substitute sample data.

## Example response

The following is a real row from the resource's `statistics` worksheet. The API
returns the complete worksheet rows and all non-empty source columns.

```json
{
  "source": "Data.go.th — องค์การสวนสัตว์แห่งประเทศไทย ในพระบรมราชูปถัมภ์",
  "dataset": "zoo-visitors2569",
  "dataset_url": "https://data.go.th/dataset/zoo-visitors2569",
  "resource_id": "0ecc96cf-d914-42a1-b184-dbbd013c3c9c",
  "fiscal_year": 2569,
  "record_count": 63,
  "statistics": [
    {
      "รายการ": "ผู้ใหญ่",
      "สวนสัตว์": "สวนสัตว์เปิดเขาเขียว",
      "ปีงบประมาณ": 2569,
      "ต.ค. 68": 59893,
      "พ.ย. 68": 31752,
      "ธ.ค. 68": 42297,
      "ม.ค.69": 27918,
      "ก.พ. 69": 25028,
      "มี.ค. 69": 37140,
      "เม.ย. 69": 47375,
      "พ.ค. 69": 43371,
      "มิ.ย. 69": 31181,
      "ก.ค. 69": 43190,
      "ส.ค. 69": null,
      "ก.ย. 69": null
    }
  ]
}
```

The example shows one entry for readability; the live endpoint returns all source
records. The workbook is a copy of the Data.go.th resource and reflects the data
available when it was downloaded. If the government resource is updated, download
the new XLSX, replace this file, and redeploy.
