# # from fastapi import FastAPI, Request
# # from pydantic import BaseModel

# # app = FastAPI()

# # class Payload(BaseModel):
    # # # Bạn có thể định nghĩa cấu trúc payload nếu muốn
    # # any_data: dict = {}

# # @app.get("/")
# # def handle_get():
    # # return {"message": "GET request received"}

# # @app.post("/")
# # async def handle_post(request: Request):
    # # data = await request.json()
    # # return {"message": "POST received", "data": data}

# # @app.put("/")
# # async def handle_put(request: Request):
    # # data = await request.json()
    # # return {"message": "PUT received", "data": data}





# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # ⚠️ Cho phép CORS cho tất cả origin (bạn có thể giới hạn nếu cần)
# app.add_middleware(
    # CORSMiddleware,
    # allow_origins=["*"],  # Hoặc ["http://localhost:3000"] nếu cụ thể hơn
    # allow_credentials=True,
    # allow_methods=["*"],
    # allow_headers=["*"],
# )

# @app.get("/")
# def handle_get():
    # return {"message": "GET request received"}



# @app.post("/")
# async def handle_post(request: Request):
    # data = await request.json()
    # return_data = []
    # return_data.append(
        # {
          # "__type": "HMHWeb.Models.DiemThi.TraCuuXem",
          # "ID": 3909,
          # "DotXem": "",
          # "Cot01": "250123",
          # "Cot02": "Lê Hà My",
          # "Cot03": "13/08/2010",
          # "Cot04": "Ngữ văn",
          # "Cot05": " 3.80 ",
          # "Cot06": " 7.25 ",
          # "Cot07": " 7.25 ",
          # "Cot08": " 8.50 ",
          # "Cot09": " 31.05 ",
          # "Cot10": "",
          # "Ten01": "SBD",
          # "Ten02": "Họ và tên",
          # "Ten03": "Ngày sinh",
          # "Ten04": "Chuyên",
          # "Ten05": "Toán vòng 1",
          # "Ten06": "Anh vòng 1",
          # "Ten07": "Văn vòng 1",
          # "Ten08": "Môn chuyên",
          # "Ten09": "Tổng điểm",
          # "Ten10": "",
          # "Hien01": 1,
          # "Hien02": 1,
          # "Hien03": 1,
          # "Hien04": 1,
          # "Hien05": 1,
          # "Hien06": 1,
          # "Hien07": 1,
          # "Hien08": 1,
          # "Hien09": 1,
          # "Hien10": 0
        # }
    # )
    # return {"message": "POST received", "d": return_data}



# # @app.put("/")
# # async def handle_put(request: Request):
    # # data = await request.json()
    # # return {"message": "PUT received", "d": f"[{data}]"}




from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
import base64

app = FastAPI()

# Bật CORS nếu cần gửi từ trình duyệt
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mô hình yêu cầu
# class SearchRequest(BaseModel):
    # dotXem: str
    # timKiem: str

@app.get("/{full_path:path}")
async def catch_all_get_method(full_path: str):
    return PlainTextResponse(f"Dữ liệu truy cập tại '/{full_path}' bị chặn!\nChỉ được phép truy cập để lấy dữ liệu từ máy chủ")

@app.api_route("/{full_path:path}", methods=[
    "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS",
    "CONNECT", "TRACE", "LINK", "UNLINK", "COPY", "MOVE", "LOCK",
    "UNLOCK", "PROPFIND", "PROPPATCH", "SEARCH", "MKCOL", "REPORT",
    "CHECKOUT", "MERGE", "MKACTIVITY", "ORDERPATCH", "ACL", "LABEL", "VERSION-CONTROL"
])
async def catch_all_method_prevent(request: Request, full_path: str):
    return JSONResponse({
            "method": request.method,
            "requestURL": f"{full_path}",
            "data": "[{}]",
            "message": f"""Application received: METHOD='{request.method}', LINKED='{full_path}', RETURN='Method not supported'"""
    })

password_typelocal: dict[str, str] = {}

# Dữ liệu
students = [
  {
    "SBD": "250001",
    "HoTen": "Cao Hà An",
    "NgaySinh": "04/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "6.00",
    "Van": "6.75",
    "MonChuyen": "6.25",
    "TongDiem": "26.33"
  },
  {
    "SBD": "250002",
    "HoTen": "Đặng Thiên An",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.20",
    "Anh": "4.25",
    "Van": "6.75",
    "MonChuyen": "7.50",
    "TongDiem": "25.45"
  },
  {
    "SBD": "250003",
    "HoTen": "Nguyễn Phan Hà An",
    "NgaySinh": "26/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "8.25",
    "Van": "7.75",
    "MonChuyen": "9.00",
    "TongDiem": "34.50"
  },
  {
    "SBD": "250004",
    "HoTen": "Nguyễn Trần Hải An",
    "NgaySinh": "26/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.70",
    "Anh": "8.25",
    "Van": "7.75",
    "MonChuyen": "10.25",
    "TongDiem": "37.08"
  },
  {
    "SBD": "250005",
    "HoTen": "Nguyễn Trần Hiền An",
    "NgaySinh": "26/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.30",
    "Anh": "7.00",
    "Van": "7.75",
    "MonChuyen": "10.00",
    "TongDiem": "35.05"
  },
  {
    "SBD": "250006",
    "HoTen": "Nguyễn Thi Ân",
    "NgaySinh": "11/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "7.75",
    "Van": "0.0",
    "MonChuyen": "0.0",
    "TongDiem": "0.0"
  },
  {
    "SBD": "250007",
    "HoTen": "Cao Thục Anh",
    "NgaySinh": "10/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.20",
    "Anh": "4.00",
    "Van": "8.00",
    "MonChuyen": "7.00",
    "TongDiem": "25.70"
  },
  {
    "SBD": "250008",
    "HoTen": "Lê Minh Nhật Anh",
    "NgaySinh": "29/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.10",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "14.00",
    "TongDiem": "42.10"
  },
  {
    "SBD": "250009",
    "HoTen": "Lê Thị Quỳnh Anh",
    "NgaySinh": "04/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.50",
    "Anh": "6.00",
    "Van": "8.00",
    "MonChuyen": "7.00",
    "TongDiem": "29.00"
  },
  {
    "SBD": "250010",
    "HoTen": "Lê Thục Anh",
    "NgaySinh": "04/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.80",
    "Anh": "4.75",
    "Van": "7.50",
    "MonChuyen": "7.25",
    "TongDiem": "27.93"
  },
  {
    "SBD": "250011",
    "HoTen": "Lương Nữ Hồng Anh",
    "NgaySinh": "12/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.90",
    "Anh": "4.75",
    "Van": "6.50",
    "MonChuyen": "10.25",
    "TongDiem": "31.53"
  },
  {
    "SBD": "250012",
    "HoTen": "Nguyễn Hà Anh",
    "NgaySinh": "19/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.80",
    "Anh": "6.75",
    "Van": "8.50",
    "MonChuyen": "10.75",
    "TongDiem": "37.18"
  },
  {
    "SBD": "250013",
    "HoTen": "Nguyễn Hà Anh",
    "NgaySinh": "08/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "2.70",
    "Anh": "2.75",
    "Van": "7.25",
    "MonChuyen": "7.00",
    "TongDiem": "23.20"
  },
  {
    "SBD": "250014",
    "HoTen": "Nguyễn Lê Hà Anh",
    "NgaySinh": "31/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.40",
    "Anh": "7.75",
    "Van": "8.00",
    "MonChuyen": "11.00",
    "TongDiem": "35.65"
  },
  {
    "SBD": "250015",
    "HoTen": "Nguyễn Lê Tú Anh",
    "NgaySinh": "09/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.70",
    "Anh": "5.50",
    "Van": "7.50",
    "MonChuyen": "5.00",
    "TongDiem": "24.20"
  },
  {
    "SBD": "250016",
    "HoTen": "Nguyễn Phương Anh",
    "NgaySinh": "04/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.90",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "10.50",
    "TongDiem": "33.40"
  },
  {
    "SBD": "250017",
    "HoTen": "Nguyễn Thị Hiền Anh",
    "NgaySinh": "29/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.60",
    "Anh": "7.00",
    "Van": "7.00",
    "MonChuyen": "10.00",
    "TongDiem": "33.60"
  },
  {
    "SBD": "250018",
    "HoTen": "Nguyễn Thị Hiền Anh",
    "NgaySinh": "08/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.30",
    "Anh": "6.75",
    "Van": "6.00",
    "MonChuyen": "7.00",
    "TongDiem": "27.55"
  },
  {
    "SBD": "250019",
    "HoTen": "Nguyễn Thị Hoài Anh",
    "NgaySinh": "18/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.10",
    "Anh": "3.00",
    "Van": "7.50",
    "MonChuyen": "6.00",
    "TongDiem": "24.60"
  },
  {
    "SBD": "250020",
    "HoTen": "Nguyễn Thị Lâm Anh",
    "NgaySinh": "14/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.20",
    "Anh": "7.50",
    "Van": "8.00",
    "MonChuyen": "10.50",
    "TongDiem": "37.45"
  },
  {
    "SBD": "250021",
    "HoTen": "Nguyễn Thị Vân Anh",
    "NgaySinh": "10/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.50",
    "Anh": "6.00",
    "Van": "8.00",
    "MonChuyen": "8.75",
    "TongDiem": "32.63"
  },
  {
    "SBD": "250022",
    "HoTen": "Phan Thị Châu Anh",
    "NgaySinh": "14/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.50",
    "Anh": "4.75",
    "Van": "6.75",
    "MonChuyen": "7.00",
    "TongDiem": "27.50"
  },
  {
    "SBD": "250023",
    "HoTen": "Trần Bảo Anh",
    "NgaySinh": "25/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "8.75",
    "Van": "7.50",
    "MonChuyen": "8.50",
    "TongDiem": "34.00"
  },
  {
    "SBD": "250024",
    "HoTen": "Phan Gia Bảo",
    "NgaySinh": "25/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.40",
    "Anh": "6.25",
    "Van": "5.75",
    "MonChuyen": "7.00",
    "TongDiem": "25.90"
  },
  {
    "SBD": "250025",
    "HoTen": "Trần Gia Bảo",
    "NgaySinh": "19/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "2.80",
    "Anh": "8.25",
    "Van": "6.25",
    "MonChuyen": "8.00",
    "TongDiem": "29.30"
  },
  {
    "SBD": "250026",
    "HoTen": "Hoàng Hồng Bích",
    "NgaySinh": "06/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.50",
    "Anh": "6.25",
    "Van": "7.00",
    "MonChuyen": "7.50",
    "TongDiem": "29.00"
  },
  {
    "SBD": "250027",
    "HoTen": "Võ Thị Yến Bình",
    "NgaySinh": "24/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.50",
    "Anh": "7.75",
    "Van": "6.75",
    "MonChuyen": "9.50",
    "TongDiem": "34.25"
  },
  {
    "SBD": "250028",
    "HoTen": "Cao Ngọc Minh Châu",
    "NgaySinh": "12/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.20",
    "Anh": "5.50",
    "Van": "7.25",
    "MonChuyen": "10.25",
    "TongDiem": "33.33"
  },
  {
    "SBD": "250029",
    "HoTen": "Ngô Tuệ Châu",
    "NgaySinh": "25/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.40",
    "Anh": "4.25",
    "Van": "7.00",
    "MonChuyen": "8.00",
    "TongDiem": "27.65"
  },
  {
    "SBD": "250030",
    "HoTen": "Nguyễn Hoàng Châu",
    "NgaySinh": "10/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "8.20",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "41.45"
  },
  {
    "SBD": "250031",
    "HoTen": "Nguyễn Ngọc Châu",
    "NgaySinh": "23/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.10",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "9.00",
    "TongDiem": "32.85"
  },
  {
    "SBD": "250032",
    "HoTen": "Nguyễn Phạm Bảo Châu",
    "NgaySinh": "27/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.50",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "8.00",
    "TongDiem": "30.00"
  },
  {
    "SBD": "250033",
    "HoTen": "Trần Thị Minh Châu",
    "NgaySinh": "19/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.00",
    "Anh": "6.00",
    "Van": "7.25",
    "MonChuyen": "8.50",
    "TongDiem": "32.00"
  },
  {
    "SBD": "250034",
    "HoTen": "Trịnh Thị Minh Châu",
    "NgaySinh": "12/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.50",
    "Anh": "5.50",
    "Van": "6.50",
    "MonChuyen": "8.00",
    "TongDiem": "28.50"
  },
  {
    "SBD": "250035",
    "HoTen": "Lê Khánh Chi",
    "NgaySinh": "22/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.40",
    "Anh": "6.25",
    "Van": "7.50",
    "MonChuyen": "8.00",
    "TongDiem": "31.15"
  },
  {
    "SBD": "250036",
    "HoTen": "Ngô Lê Tùng Chi",
    "NgaySinh": "16/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.90",
    "Anh": "7.50",
    "Van": "7.25",
    "MonChuyen": "9.00",
    "TongDiem": "33.15"
  },
  {
    "SBD": "250037",
    "HoTen": "Nguyễn Đoàn Mai Chi",
    "NgaySinh": "16/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.60",
    "Anh": "4.25",
    "Van": "7.25",
    "MonChuyen": "9.50",
    "TongDiem": "30.35"
  },
  {
    "SBD": "250038",
    "HoTen": "Nguyễn Hồ Mai Chi",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.10",
    "Anh": "9.00",
    "Van": "8.25",
    "MonChuyen": "11.00",
    "TongDiem": "37.85"
  },
  {
    "SBD": "250039",
    "HoTen": "Nguyễn Khánh Chi",
    "NgaySinh": "04/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.10",
    "Anh": "7.25",
    "Van": "7.00",
    "MonChuyen": "8.00",
    "TongDiem": "32.35"
  },
  {
    "SBD": "250040",
    "HoTen": "Nguyễn Thị Thục Chi",
    "NgaySinh": "12/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.30",
    "Anh": "2.75",
    "Van": "7.50",
    "MonChuyen": "7.50",
    "TongDiem": "25.80"
  },
  {
    "SBD": "250041",
    "HoTen": "Nguyễn Thị Thùy Chi",
    "NgaySinh": "28/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "4.00",
    "Van": "7.50",
    "MonChuyen": "8.50",
    "TongDiem": "28.45"
  },
  {
    "SBD": "250042",
    "HoTen": "Nguyễn Tùng Chi",
    "NgaySinh": "26/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "2.70",
    "Anh": "5.75",
    "Van": "7.00",
    "MonChuyen": "7.50",
    "TongDiem": "26.70"
  },
  {
    "SBD": "250043",
    "HoTen": "Trần Thị Linh Chi",
    "NgaySinh": "27/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.50",
    "Anh": "9.50",
    "Van": "8.00",
    "MonChuyen": "11.50",
    "TongDiem": "40.25"
  },
  {
    "SBD": "250044",
    "HoTen": "Trần Thị Quỳnh Chi",
    "NgaySinh": "09/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "2.80",
    "Anh": "4.00",
    "Van": "7.50",
    "MonChuyen": "4.75",
    "TongDiem": "21.43"
  },
  {
    "SBD": "250047",
    "HoTen": "Phạm Đan Đan",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.00",
    "Anh": "4.00",
    "Van": "7.00",
    "MonChuyen": "5.50",
    "TongDiem": "23.25"
  },
  {
    "SBD": "250048",
    "HoTen": "Phùng Lê Linh Đan",
    "NgaySinh": "21/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.40",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "12.00",
    "TongDiem": "36.15"
  },
  {
    "SBD": "250049",
    "HoTen": "Trần Hồng Đăng",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.40",
    "Anh": "5.00",
    "Van": "6.25",
    "MonChuyen": "5.00",
    "TongDiem": "22.15"
  },
  {
    "SBD": "250050",
    "HoTen": "Dương Hồ Ngọc Diệp",
    "NgaySinh": "25/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.20",
    "Anh": "8.75",
    "Van": "7.50",
    "MonChuyen": "10.50",
    "TongDiem": "37.20"
  },
  {
    "SBD": "250051",
    "HoTen": "Trần Hoàng Dung",
    "NgaySinh": "01/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.30",
    "Anh": "5.50",
    "Van": "7.25",
    "MonChuyen": "5.00",
    "TongDiem": "24.55"
  },
  {
    "SBD": "250052",
    "HoTen": "Đinh Tiến Dũng",
    "NgaySinh": "11/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.80",
    "Anh": "3.75",
    "Van": "7.50",
    "MonChuyen": "8.50",
    "TongDiem": "29.80"
  },
  {
    "SBD": "250053",
    "HoTen": "Lê Đậu Thuỳ Dương",
    "NgaySinh": "07/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.80",
    "Anh": "5.25",
    "Van": "8.25",
    "MonChuyen": "13.00",
    "TongDiem": "37.80"
  },
  {
    "SBD": "250054",
    "HoTen": "Nguyễn Thị Thuỳ Dương",
    "NgaySinh": "31/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.80",
    "Anh": "3.00",
    "Van": "6.75",
    "MonChuyen": "10.00",
    "TongDiem": "28.55"
  },
  {
    "SBD": "250055",
    "HoTen": "Thái Thị Thùy Dương",
    "NgaySinh": "28/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "6.25",
    "Van": "7.50",
    "MonChuyen": "8.50",
    "TongDiem": "31.50"
  },
  {
    "SBD": "250056",
    "HoTen": "Thái Thuỳ Dương",
    "NgaySinh": "25/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.20",
    "Anh": "5.50",
    "Van": "0.0",
    "MonChuyen": "0.0",
    "TongDiem": "0.0"
  },
  {
    "SBD": "250057",
    "HoTen": "Hoàng Thị Mỹ Duyên",
    "NgaySinh": "07/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.20",
    "Anh": "3.75",
    "Van": "6.75",
    "MonChuyen": "8.00",
    "TongDiem": "25.70"
  },
  {
    "SBD": "250058",
    "HoTen": "Hoàng Thị Mỹ Duyên",
    "NgaySinh": "22/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.40",
    "Anh": "6.75",
    "Van": "7.75",
    "MonChuyen": "11.00",
    "TongDiem": "36.40"
  },
  {
    "SBD": "250059",
    "HoTen": "Trần Thị Linh Giang",
    "NgaySinh": "03/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.80",
    "Anh": "4.75",
    "Van": "7.00",
    "MonChuyen": "10.50",
    "TongDiem": "32.30"
  },
  {
    "SBD": "250060",
    "HoTen": "Văn Thị Hương Giang",
    "NgaySinh": "17/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "8.25",
    "Van": "8.25",
    "MonChuyen": "11.25",
    "TongDiem": "37.58"
  },
  {
    "SBD": "250061",
    "HoTen": "Đoàn Việt Hà",
    "NgaySinh": "14/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.70",
    "Anh": "6.00",
    "Van": "7.00",
    "MonChuyen": "7.00",
    "TongDiem": "28.20"
  },
  {
    "SBD": "250062",
    "HoTen": "Lê Ngọc Hà",
    "NgaySinh": "20/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.40",
    "Anh": "6.75",
    "Van": "7.50",
    "MonChuyen": "8.00",
    "TongDiem": "32.65"
  },
  {
    "SBD": "250063",
    "HoTen": "Nguyễn Lê Khánh Hà",
    "NgaySinh": "18/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.30",
    "Anh": "9.00",
    "Van": "7.75",
    "MonChuyen": "12.50",
    "TongDiem": "41.80"
  },
  {
    "SBD": "250064",
    "HoTen": "Nguyễn Thị Hồng Hà",
    "NgaySinh": "19/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.90",
    "Anh": "8.75",
    "Van": "8.00",
    "MonChuyen": "11.50",
    "TongDiem": "39.90"
  },
  {
    "SBD": "250065",
    "HoTen": "Nguyễn Vân Hà",
    "NgaySinh": "25/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.50",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "8.50",
    "TongDiem": "34.75"
  },
  {
    "SBD": "250066",
    "HoTen": "Nguyễn Việt Hà",
    "NgaySinh": "01/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "9.75",
    "Van": "8.25",
    "MonChuyen": "11.00",
    "TongDiem": "40.10"
  },
  {
    "SBD": "250067",
    "HoTen": "Thái Tĩnh Hà",
    "NgaySinh": "03/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "8.25",
    "Van": "7.75",
    "MonChuyen": "9.50",
    "TongDiem": "35.85"
  },
  {
    "SBD": "250068",
    "HoTen": "Phan Hoàng Gia Hân",
    "NgaySinh": "12/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.40",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "6.75",
    "TongDiem": "27.78"
  },
  {
    "SBD": "250069",
    "HoTen": "Hồ Thị Minh Hằng",
    "NgaySinh": "13/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.10",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "9.50",
    "TongDiem": "36.35"
  },
  {
    "SBD": "250070",
    "HoTen": "Nguyễn Thanh Hiền",
    "NgaySinh": "31/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.40",
    "Anh": "6.25",
    "Van": "6.75",
    "MonChuyen": "8.50",
    "TongDiem": "31.15"
  },
  {
    "SBD": "250071",
    "HoTen": "Nguyễn Thị Minh Hiền",
    "NgaySinh": "13/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.30",
    "Anh": "9.25",
    "Van": "8.00",
    "MonChuyen": "9.00",
    "TongDiem": "36.05"
  },
  {
    "SBD": "250072",
    "HoTen": "Nguyễn Thị Thảo Hiền",
    "NgaySinh": "21/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.40",
    "Anh": "4.00",
    "Van": "7.25",
    "MonChuyen": "9.00",
    "TongDiem": "29.15"
  },
  {
    "SBD": "250073",
    "HoTen": "Trần Thị Hoài",
    "NgaySinh": "03/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.10",
    "Anh": "6.00",
    "Van": "7.50",
    "MonChuyen": "9.00",
    "TongDiem": "32.10"
  },
  {
    "SBD": "250074",
    "HoTen": "Nguyễn Nhật Hoàng",
    "NgaySinh": "17/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.90",
    "Anh": "5.75",
    "Van": "7.00",
    "MonChuyen": "7.25",
    "TongDiem": "29.53"
  },
  {
    "SBD": "250075",
    "HoTen": "Trần Gia Hoàng",
    "NgaySinh": "01/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "7.40",
    "Anh": "8.75",
    "Van": "7.50",
    "MonChuyen": "9.00",
    "TongDiem": "37.15"
  },
  {
    "SBD": "250076",
    "HoTen": "Vũ Thuý Hường",
    "NgaySinh": "02/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.20",
    "Anh": "6.25",
    "Van": "7.00",
    "MonChuyen": "8.75",
    "TongDiem": "32.58"
  },
  {
    "SBD": "250077",
    "HoTen": "Hồ Đức Huy",
    "NgaySinh": "19/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.30",
    "Anh": "5.75",
    "Van": "6.50",
    "MonChuyen": "5.00",
    "TongDiem": "24.05"
  },
  {
    "SBD": "250078",
    "HoTen": "Nguyễn Minh Huyền",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "9.00",
    "TongDiem": "34.10"
  },
  {
    "SBD": "250079",
    "HoTen": "Võ Thị Khánh Huyền",
    "NgaySinh": "28/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.40",
    "Anh": "5.00",
    "Van": "7.25",
    "MonChuyen": "8.50",
    "TongDiem": "29.40"
  },
  {
    "SBD": "250080",
    "HoTen": "Đoàn Thị Kiều Khanh",
    "NgaySinh": "21/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.70",
    "Anh": "8.00",
    "Van": "8.00",
    "MonChuyen": "10.00",
    "TongDiem": "35.70"
  },
  {
    "SBD": "250081",
    "HoTen": "Lê Nguyễn Ngọc Khánh",
    "NgaySinh": "13/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.40",
    "Anh": "5.75",
    "Van": "7.00",
    "MonChuyen": "7.00",
    "TongDiem": "28.65"
  },
  {
    "SBD": "250082",
    "HoTen": "Nguyễn Đình Duy Khánh",
    "NgaySinh": "07/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.30",
    "Anh": "8.00",
    "Van": "7.50",
    "MonChuyen": "7.00",
    "TongDiem": "31.30"
  },
  {
    "SBD": "250083",
    "HoTen": "Phạm Nhật Khánh",
    "NgaySinh": "13/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.40",
    "Anh": "7.50",
    "Van": "6.75",
    "MonChuyen": "5.25",
    "TongDiem": "26.53"
  },
  {
    "SBD": "250084",
    "HoTen": "Trần Võ Minh Khánh",
    "NgaySinh": "19/03/2009",
    "Chuyen": "Ngữ văn",
    "Toan": "6.10",
    "Anh": "6.75",
    "Van": "6.75",
    "MonChuyen": "7.25",
    "TongDiem": "30.48"
  },
  {
    "SBD": "250085",
    "HoTen": "Trần Hữu Anh Khoa",
    "NgaySinh": "23/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.50",
    "Anh": "7.75",
    "Van": "7.00",
    "MonChuyen": "8.00",
    "TongDiem": "30.25"
  },
  {
    "SBD": "250086",
    "HoTen": "Đặng Lê Minh Khuê",
    "NgaySinh": "24/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "7.75",
    "Van": "7.25",
    "MonChuyen": "7.75",
    "TongDiem": "30.83"
  },
  {
    "SBD": "250087",
    "HoTen": "Nguyễn Thái Kiên",
    "NgaySinh": "11/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.40",
    "Anh": "7.75",
    "Van": "6.25",
    "MonChuyen": "2.00",
    "TongDiem": "21.40"
  },
  {
    "SBD": "250088",
    "HoTen": "Phạm Đức Kiên",
    "NgaySinh": "09/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.80",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "10.50",
    "TongDiem": "34.80"
  },
  {
    "SBD": "250089",
    "HoTen": "Nguyễn Lê Thùy Lâm",
    "NgaySinh": "22/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.50",
    "Anh": "7.25",
    "Van": "6.50",
    "MonChuyen": "6.50",
    "TongDiem": "30.00"
  },
  {
    "SBD": "250090",
    "HoTen": "Nguyễn Trúc Lâm",
    "NgaySinh": "15/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.40",
    "Anh": "4.75",
    "Van": "7.00",
    "MonChuyen": "7.50",
    "TongDiem": "26.40"
  },
  {
    "SBD": "250091",
    "HoTen": "Nguyễn Tùng Lâm",
    "NgaySinh": "23/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.20",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "10.75",
    "TongDiem": "36.08"
  },
  {
    "SBD": "250092",
    "HoTen": "Phan Thùy Lâm",
    "NgaySinh": "09/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.80",
    "Anh": "9.50",
    "Van": "6.75",
    "MonChuyen": "16.00",
    "TongDiem": "47.05"
  },
  {
    "SBD": "250093",
    "HoTen": "Bùi Khánh Linh",
    "NgaySinh": "20/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.00",
    "Anh": "8.25",
    "Van": "7.25",
    "MonChuyen": "7.50",
    "TongDiem": "32.75"
  },
  {
    "SBD": "250094",
    "HoTen": "Bùi Nguyễn Bảo Linh",
    "NgaySinh": "20/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.20",
    "Anh": "4.75",
    "Van": "7.00",
    "MonChuyen": "7.75",
    "TongDiem": "26.58"
  },
  {
    "SBD": "250095",
    "HoTen": "Chế Hạnh Linh",
    "NgaySinh": "07/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "7.25",
    "Van": "7.50",
    "MonChuyen": "9.50",
    "TongDiem": "34.60"
  },
  {
    "SBD": "250096",
    "HoTen": "Chu Diệu Linh",
    "NgaySinh": "06/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.70",
    "Anh": "5.00",
    "Van": "5.50",
    "MonChuyen": "8.00",
    "TongDiem": "28.20"
  },
  {
    "SBD": "250097",
    "HoTen": "Dương Thái Ngọc Linh",
    "NgaySinh": "21/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "3.75",
    "Van": "6.50",
    "MonChuyen": "7.25",
    "TongDiem": "25.33"
  },
  {
    "SBD": "250098",
    "HoTen": "Hồ Bảo Linh",
    "NgaySinh": "01/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "2.60",
    "Anh": "4.50",
    "Van": "7.25",
    "MonChuyen": "7.75",
    "TongDiem": "25.98"
  },
  {
    "SBD": "250099",
    "HoTen": "Hồ Gia Linh",
    "NgaySinh": "15/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.00",
    "Anh": "5.25",
    "Van": "6.50",
    "MonChuyen": "3.00",
    "TongDiem": "22.25"
  },
  {
    "SBD": "250100",
    "HoTen": "Hoàng Diệu Linh",
    "NgaySinh": "05/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.10",
    "Anh": "6.50",
    "Van": "7.50",
    "MonChuyen": "10.25",
    "TongDiem": "35.48"
  },
  {
    "SBD": "250101",
    "HoTen": "Hoàng Thị Khánh Linh",
    "NgaySinh": "02/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.40",
    "Anh": "7.25",
    "Van": "7.75",
    "MonChuyen": "14.00",
    "TongDiem": "42.40"
  },
  {
    "SBD": "250102",
    "HoTen": "Lê Hoàng Khánh Linh",
    "NgaySinh": "12/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.00",
    "Anh": "7.25",
    "Van": "7.75",
    "MonChuyen": "9.50",
    "TongDiem": "35.25"
  },
  {
    "SBD": "250103",
    "HoTen": "Nguyễn Khánh Linh",
    "NgaySinh": "02/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.60",
    "Anh": "4.00",
    "Van": "7.25",
    "MonChuyen": "7.00",
    "TongDiem": "26.35"
  },
  {
    "SBD": "250104",
    "HoTen": "Nguyễn Khánh Linh",
    "NgaySinh": "03/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.90",
    "Anh": "7.25",
    "Van": "8.25",
    "MonChuyen": "9.00",
    "TongDiem": "34.90"
  },
  {
    "SBD": "250105",
    "HoTen": "Nguyễn Khánh Linh",
    "NgaySinh": "13/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.70",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "5.50",
    "TongDiem": "26.95"
  },
  {
    "SBD": "250106",
    "HoTen": "Nguyễn Ngọc Gia Linh",
    "NgaySinh": "16/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.90",
    "Anh": "4.25",
    "Van": "7.50",
    "MonChuyen": "9.00",
    "TongDiem": "29.15"
  },
  {
    "SBD": "250107",
    "HoTen": "Nguyễn Ngọc Linh",
    "NgaySinh": "09/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.20",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "4.00",
    "TongDiem": "26.45"
  },
  {
    "SBD": "250108",
    "HoTen": "Nguyễn Ngọc Linh",
    "NgaySinh": "04/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.10",
    "Anh": "8.00",
    "Van": "8.00",
    "MonChuyen": "11.00",
    "TongDiem": "37.60"
  },
  {
    "SBD": "250110",
    "HoTen": "Nguyễn Thị Khánh Linh",
    "NgaySinh": "30/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "5.50",
    "Van": "7.25",
    "MonChuyen": "10.50",
    "TongDiem": "34.10"
  },
  {
    "SBD": "250111",
    "HoTen": "Nguyễn Thuỳ Linh",
    "NgaySinh": "09/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.90",
    "Anh": "4.25",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "33.15"
  },
  {
    "SBD": "250112",
    "HoTen": "Phạm Hoàng Khánh Linh",
    "NgaySinh": "09/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.40",
    "Anh": "4.75",
    "Van": "8.00",
    "MonChuyen": "10.00",
    "TongDiem": "33.15"
  },
  {
    "SBD": "250113",
    "HoTen": "Phan Thị Hà Linh",
    "NgaySinh": "19/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.60",
    "Anh": "7.50",
    "Van": "7.25",
    "MonChuyen": "8.00",
    "TongDiem": "30.35"
  },
  {
    "SBD": "250114",
    "HoTen": "Thái Cẩm Linh",
    "NgaySinh": "15/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.30",
    "Anh": "6.50",
    "Van": "7.75",
    "MonChuyen": "12.00",
    "TongDiem": "37.55"
  },
  {
    "SBD": "250115",
    "HoTen": "Võ Hoàng Linh",
    "NgaySinh": "16/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.20",
    "Anh": "5.75",
    "Van": "6.00",
    "MonChuyen": "10.00",
    "TongDiem": "29.95"
  },
  {
    "SBD": "250116",
    "HoTen": "Võ Thị Thảo Ly",
    "NgaySinh": "05/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.80",
    "Anh": "7.25",
    "Van": "7.25",
    "MonChuyen": "8.50",
    "TongDiem": "31.05"
  },
  {
    "SBD": "250117",
    "HoTen": "Lê Thị Thanh Mai",
    "NgaySinh": "16/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "7.40",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "11.00",
    "TongDiem": "40.40"
  },
  {
    "SBD": "250118",
    "HoTen": "Nguyễn Sỹ Mạnh",
    "NgaySinh": "06/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.10",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "7.00",
    "TongDiem": "32.10"
  },
  {
    "SBD": "250119",
    "HoTen": "Hoàng Chế Thủy Minh",
    "NgaySinh": "23/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.90",
    "Anh": "5.25",
    "Van": "7.25",
    "MonChuyen": "7.50",
    "TongDiem": "28.65"
  },
  {
    "SBD": "250120",
    "HoTen": "Nguyễn Ngọc Minh",
    "NgaySinh": "27/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.50",
    "Anh": "7.50",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "36.00"
  },
  {
    "SBD": "250121",
    "HoTen": "Đậu Thị My My",
    "NgaySinh": "17/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.10",
    "Anh": "6.00",
    "Van": "7.25",
    "MonChuyen": "11.00",
    "TongDiem": "33.85"
  },
  {
    "SBD": "250122",
    "HoTen": "Đoàn Thảo My",
    "NgaySinh": "28/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.20",
    "Anh": "4.75",
    "Van": "6.75",
    "MonChuyen": "3.25",
    "TongDiem": "19.58"
  },
  {
    "SBD": "250123",
    "HoTen": "Lê Hà My",
    "NgaySinh": "13/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.80",
    "Anh": "7.25",
    "Van": "7.25",
    "MonChuyen": "8.50",
    "TongDiem": "31.05"
  },
  {
    "SBD": "250124",
    "HoTen": "Nguyễn Trà My",
    "NgaySinh": "14/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.10",
    "Anh": "3.25",
    "Van": "6.50",
    "MonChuyen": "3.50",
    "TongDiem": "20.10"
  },
  {
    "SBD": "250125",
    "HoTen": "Nguyễn Trần Trà My",
    "NgaySinh": "30/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.90",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "12.00",
    "TongDiem": "37.65"
  },
  {
    "SBD": "250126",
    "HoTen": "Phan Dương Trà My",
    "NgaySinh": "13/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "5.00",
    "Van": "6.75",
    "MonChuyen": "6.50",
    "TongDiem": "25.70"
  },
  {
    "SBD": "250127",
    "HoTen": "Phan Thảo My",
    "NgaySinh": "11/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.70",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "4.75",
    "TongDiem": "23.33"
  },
  {
    "SBD": "250128",
    "HoTen": "Trần Hà My",
    "NgaySinh": "12/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.20",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "7.75",
    "TongDiem": "32.58"
  },
  {
    "SBD": "250129",
    "HoTen": "Hồ Dương Lê Na",
    "NgaySinh": "24/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.00",
    "Anh": "8.00",
    "Van": "7.50",
    "MonChuyen": "6.50",
    "TongDiem": "29.25"
  },
  {
    "SBD": "250130",
    "HoTen": "Lê Khánh Nam",
    "NgaySinh": "03/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "4.25",
    "Van": "7.00",
    "MonChuyen": "6.50",
    "TongDiem": "26.60"
  },
  {
    "SBD": "250131",
    "HoTen": "Nguyễn Hữu Bảo Nam",
    "NgaySinh": "12/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.40",
    "Anh": "5.50",
    "Van": "7.00",
    "MonChuyen": "7.00",
    "TongDiem": "27.40"
  },
  {
    "SBD": "250132",
    "HoTen": "Nguyễn Hằng Nga",
    "NgaySinh": "15/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.00",
    "Anh": "5.00",
    "Van": "7.25",
    "MonChuyen": "6.00",
    "TongDiem": "27.25"
  },
  {
    "SBD": "250133",
    "HoTen": "Nguyễn Phạm Hằng Nga",
    "NgaySinh": "13/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.40",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "6.50",
    "TongDiem": "26.15"
  },
  {
    "SBD": "250134",
    "HoTen": "Phạm Phương Nga",
    "NgaySinh": "22/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.20",
    "Anh": "8.75",
    "Van": "7.50",
    "MonChuyen": "12.00",
    "TongDiem": "40.45"
  },
  {
    "SBD": "250135",
    "HoTen": "Nguyễn Bảo Ngân",
    "NgaySinh": "28/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.00",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "10.00",
    "TongDiem": "35.50"
  },
  {
    "SBD": "250136",
    "HoTen": "Lê Hồng Ngọc",
    "NgaySinh": "20/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.50",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "11.00",
    "TongDiem": "34.50"
  },
  {
    "SBD": "250137",
    "HoTen": "Nguyễn Bảo Ngọc",
    "NgaySinh": "06/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.50",
    "Anh": "7.25",
    "Van": "7.75",
    "MonChuyen": "11.50",
    "TongDiem": "37.75"
  },
  {
    "SBD": "250140",
    "HoTen": "Nguyễn Mỹ Ngọc",
    "NgaySinh": "16/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.80",
    "Anh": "5.25",
    "Van": "7.00",
    "MonChuyen": "10.00",
    "TongDiem": "32.05"
  },
  {
    "SBD": "250142",
    "HoTen": "Phan Thị Bảo Ngọc",
    "NgaySinh": "04/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "7.25",
    "Van": "7.75",
    "MonChuyen": "9.25",
    "TongDiem": "34.48"
  },
  {
    "SBD": "250143",
    "HoTen": "Trần Hà Ngọc",
    "NgaySinh": "07/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "7.25",
    "Van": "7.50",
    "MonChuyen": "10.50",
    "TongDiem": "34.70"
  },
  {
    "SBD": "250144",
    "HoTen": "Võ Hoàng Bảo Ngọc",
    "NgaySinh": "06/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.00",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "10.50",
    "TongDiem": "32.50"
  },
  {
    "SBD": "250145",
    "HoTen": "Nguyễn Hạnh Nguyên",
    "NgaySinh": "10/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "5.75",
    "Van": "7.50",
    "MonChuyen": "10.75",
    "TongDiem": "34.38"
  },
  {
    "SBD": "250146",
    "HoTen": "Nguyễn Lê Thảo Nguyên",
    "NgaySinh": "28/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.00",
    "Anh": "6.25",
    "Van": "7.50",
    "MonChuyen": "12.50",
    "TongDiem": "36.50"
  },
  {
    "SBD": "250147",
    "HoTen": "Thái Bình Nguyên",
    "NgaySinh": "25/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "3.50",
    "Van": "7.50",
    "MonChuyen": "11.75",
    "TongDiem": "33.63"
  },
  {
    "SBD": "250148",
    "HoTen": "Võ An Nguyên",
    "NgaySinh": "11/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "7.25",
    "Van": "8.00",
    "MonChuyen": "11.00",
    "TongDiem": "37.35"
  },
  {
    "SBD": "250149",
    "HoTen": "Lê Thị Thanh Nhâm",
    "NgaySinh": "12/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "7.50",
    "Anh": "8.25",
    "Van": "8.25",
    "MonChuyen": "10.25",
    "TongDiem": "39.38"
  },
  {
    "SBD": "250150",
    "HoTen": "Cao Gia Nhi",
    "NgaySinh": "21/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "7.30",
    "Anh": "9.50",
    "Van": "8.25",
    "MonChuyen": "11.50",
    "TongDiem": "42.30"
  },
  {
    "SBD": "250151",
    "HoTen": "Lê Thị Yến Nhi",
    "NgaySinh": "14/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.10",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "9.50",
    "TongDiem": "34.60"
  },
  {
    "SBD": "250152",
    "HoTen": "Nguyễn Lương Yến Nhi",
    "NgaySinh": "20/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.50",
    "Anh": "5.75",
    "Van": "6.75",
    "MonChuyen": "11.50",
    "TongDiem": "34.25"
  },
  {
    "SBD": "250153",
    "HoTen": "Nguyễn Thái Thảo Nhi",
    "NgaySinh": "16/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.10",
    "Anh": "4.25",
    "Van": "0.0",
    "MonChuyen": "0.0",
    "TongDiem": "0.0"
  },
  {
    "SBD": "250154",
    "HoTen": "Nguyễn Thủy Nhi",
    "NgaySinh": "20/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.20",
    "Anh": "6.25",
    "Van": "7.50",
    "MonChuyen": "8.25",
    "TongDiem": "31.33"
  },
  {
    "SBD": "250155",
    "HoTen": "Nguyễn Trần Yến Nhi",
    "NgaySinh": "21/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "6.00",
    "Van": "7.75",
    "MonChuyen": "7.50",
    "TongDiem": "29.20"
  },
  {
    "SBD": "250156",
    "HoTen": "Ông Tuệ Nhi",
    "NgaySinh": "05/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.30",
    "Anh": "9.00",
    "Van": "8.00",
    "MonChuyen": "12.00",
    "TongDiem": "41.30"
  },
  {
    "SBD": "250157",
    "HoTen": "Phan Phương Nhi",
    "NgaySinh": "25/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.40",
    "Anh": "8.75",
    "Van": "8.00",
    "MonChuyen": "11.50",
    "TongDiem": "40.40"
  },
  {
    "SBD": "250158",
    "HoTen": "Trần Mai Nhi",
    "NgaySinh": "08/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.30",
    "Anh": "6.00",
    "Van": "7.50",
    "MonChuyen": "8.50",
    "TongDiem": "30.55"
  },
  {
    "SBD": "250159",
    "HoTen": "Trần Thảo Nhi",
    "NgaySinh": "03/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.00",
    "Anh": "9.00",
    "Van": "8.00",
    "MonChuyen": "9.00",
    "TongDiem": "36.50"
  },
  {
    "SBD": "250160",
    "HoTen": "Trần Uyên Nhi",
    "NgaySinh": "20/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "6.75",
    "Van": "8.25",
    "MonChuyen": "7.50",
    "TongDiem": "30.45"
  },
  {
    "SBD": "250161",
    "HoTen": "Võ Phương Nhi",
    "NgaySinh": "28/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.20",
    "Anh": "6.75",
    "Van": "7.75",
    "MonChuyen": "12.00",
    "TongDiem": "35.70"
  },
  {
    "SBD": "250162",
    "HoTen": "Cao Lê An Nhiên",
    "NgaySinh": "17/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "7.50",
    "Van": "7.75",
    "MonChuyen": "12.00",
    "TongDiem": "37.45"
  },
  {
    "SBD": "250163",
    "HoTen": "Nguyễn Nữ Tâm Như",
    "NgaySinh": "02/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.40",
    "Anh": "7.50",
    "Van": "8.25",
    "MonChuyen": "10.00",
    "TongDiem": "37.15"
  },
  {
    "SBD": "250164",
    "HoTen": "Phan Quỳnh Như",
    "NgaySinh": "10/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "2.80",
    "Anh": "7.25",
    "Van": "6.75",
    "MonChuyen": "6.50",
    "TongDiem": "26.55"
  },
  {
    "SBD": "250165",
    "HoTen": "Văn Gia Như",
    "NgaySinh": "22/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.00",
    "Anh": "6.75",
    "Van": "6.75",
    "MonChuyen": "6.00",
    "TongDiem": "25.50"
  },
  {
    "SBD": "250166",
    "HoTen": "Võ Yến Như",
    "NgaySinh": "25/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.80",
    "Anh": "7.75",
    "Van": "7.75",
    "MonChuyen": "10.00",
    "TongDiem": "36.30"
  },
  {
    "SBD": "250167",
    "HoTen": "Võ Thị Thảo Nương",
    "NgaySinh": "09/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.10",
    "Anh": "7.75",
    "Van": "6.75",
    "MonChuyen": "11.50",
    "TongDiem": "37.85"
  },
  {
    "SBD": "250168",
    "HoTen": "Trần Hà Phan",
    "NgaySinh": "17/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.60",
    "Anh": "5.75",
    "Van": "6.00",
    "MonChuyen": "7.00",
    "TongDiem": "26.85"
  },
  {
    "SBD": "250169",
    "HoTen": "Hồ Thị Hồng Phúc",
    "NgaySinh": "06/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.60",
    "Anh": "8.25",
    "Van": "7.25",
    "MonChuyen": "9.50",
    "TongDiem": "34.35"
  },
  {
    "SBD": "250170",
    "HoTen": "Ngô Thụy Hồng Phúc",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.90",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "13.00",
    "TongDiem": "40.40"
  },
  {
    "SBD": "250171",
    "HoTen": "Trần Mai Phương",
    "NgaySinh": "12/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.80",
    "Anh": "5.25",
    "Van": "7.00",
    "MonChuyen": "10.50",
    "TongDiem": "32.80"
  },
  {
    "SBD": "250172",
    "HoTen": "Trương Thị Hà Phương",
    "NgaySinh": "15/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "7.75",
    "Van": "6.75",
    "MonChuyen": "5.25",
    "TongDiem": "27.38"
  },
  {
    "SBD": "250174",
    "HoTen": "Nguyễn Thục Quyên",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.10",
    "Anh": "7.00",
    "Van": "7.00",
    "MonChuyen": "10.00",
    "TongDiem": "34.10"
  },
  {
    "SBD": "250175",
    "HoTen": "Nguyễn Thục Quyên",
    "NgaySinh": "06/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.90",
    "Anh": "8.25",
    "Van": "7.75",
    "MonChuyen": "9.75",
    "TongDiem": "36.53"
  },
  {
    "SBD": "250177",
    "HoTen": "Trương Phước Sang",
    "NgaySinh": "06/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.80",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "6.50",
    "TongDiem": "26.55"
  },
  {
    "SBD": "250178",
    "HoTen": "Nguyễn Cảnh Thạc",
    "NgaySinh": "04/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.10",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "4.50",
    "TongDiem": "25.10"
  },
  {
    "SBD": "250179",
    "HoTen": "Nguyễn Thị Như Thành",
    "NgaySinh": "08/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.20",
    "Anh": "7.75",
    "Van": "7.00",
    "MonChuyen": "9.00",
    "TongDiem": "34.45"
  },
  {
    "SBD": "250180",
    "HoTen": "Nguyễn Dương Phương Thảo",
    "NgaySinh": "23/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.70",
    "Anh": "8.00",
    "Van": "8.25",
    "MonChuyen": "11.00",
    "TongDiem": "39.45"
  },
  {
    "SBD": "250181",
    "HoTen": "Nguyễn Phương Thảo",
    "NgaySinh": "15/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.70",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "11.00",
    "TongDiem": "34.95"
  },
  {
    "SBD": "250182",
    "HoTen": "Nguyễn Thị Phương Thảo",
    "NgaySinh": "22/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.00",
    "Anh": "7.50",
    "Van": "6.25",
    "MonChuyen": "11.00",
    "TongDiem": "34.25"
  },
  {
    "SBD": "250183",
    "HoTen": "Đặng Thị Tâm Thư",
    "NgaySinh": "29/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "6.25",
    "Van": "7.25",
    "MonChuyen": "13.00",
    "TongDiem": "38.60"
  },
  {
    "SBD": "250184",
    "HoTen": "Đoàn Anh Thư",
    "NgaySinh": "21/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.70",
    "Anh": "4.75",
    "Van": "7.50",
    "MonChuyen": "14.00",
    "TongDiem": "36.95"
  },
  {
    "SBD": "250185",
    "HoTen": "Lê Mai Thảo Thương",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.60",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "9.25",
    "TongDiem": "35.73"
  },
  {
    "SBD": "250186",
    "HoTen": "Phan Thị Quỳnh Thương",
    "NgaySinh": "05/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.80",
    "Anh": "4.25",
    "Van": "6.75",
    "MonChuyen": "9.00",
    "TongDiem": "28.30"
  },
  {
    "SBD": "250187",
    "HoTen": "Trương Phạm Khánh Thy",
    "NgaySinh": "24/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.50",
    "Anh": "4.00",
    "Van": "7.25",
    "MonChuyen": "6.50",
    "TongDiem": "25.50"
  },
  {
    "SBD": "250188",
    "HoTen": "Võ Thị Hương Trà",
    "NgaySinh": "30/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.30",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "8.50",
    "TongDiem": "31.55"
  },
  {
    "SBD": "250189",
    "HoTen": "Dương Thuỳ Trâm",
    "NgaySinh": "30/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "6.75",
    "Van": "7.50",
    "MonChuyen": "12.00",
    "TongDiem": "37.85"
  },
  {
    "SBD": "250190",
    "HoTen": "Lưu Nguyễn Bảo Trâm",
    "NgaySinh": "03/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.90",
    "Anh": "5.75",
    "Van": "7.50",
    "MonChuyen": "12.00",
    "TongDiem": "35.15"
  },
  {
    "SBD": "250191",
    "HoTen": "Nguyễn Bảo Trâm",
    "NgaySinh": "28/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.90",
    "Anh": "5.25",
    "Van": "7.00",
    "MonChuyen": "13.00",
    "TongDiem": "36.65"
  },
  {
    "SBD": "250192",
    "HoTen": "Nguyễn Thị Huyền Trân",
    "NgaySinh": "21/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "5.25",
    "Van": "5.75",
    "MonChuyen": "8.00",
    "TongDiem": "28.00"
  },
  {
    "SBD": "250193",
    "HoTen": "Đặng Thị Minh Trang",
    "NgaySinh": "04/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.90",
    "Anh": "8.50",
    "Van": "7.25",
    "MonChuyen": "10.00",
    "TongDiem": "35.65"
  },
  {
    "SBD": "250194",
    "HoTen": "Hoàng Minh Trang",
    "NgaySinh": "20/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.40",
    "Anh": "6.75",
    "Van": "7.00",
    "MonChuyen": "10.50",
    "TongDiem": "34.90"
  },
  {
    "SBD": "250195",
    "HoTen": "Kỳ Diệu Trang",
    "NgaySinh": "08/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "4.00",
    "Van": "5.25",
    "MonChuyen": "4.00",
    "TongDiem": "19.45"
  },
  {
    "SBD": "250196",
    "HoTen": "Ngô Phương Trang",
    "NgaySinh": "21/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.40",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "7.50",
    "TongDiem": "31.65"
  },
  {
    "SBD": "250197",
    "HoTen": "Nguyễn Khánh Trang",
    "NgaySinh": "31/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.10",
    "Anh": "7.00",
    "Van": "7.50",
    "MonChuyen": "11.25",
    "TongDiem": "35.48"
  },
  {
    "SBD": "250198",
    "HoTen": "Nguyễn Thảo Trang",
    "NgaySinh": "02/10/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.10",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "10.25",
    "TongDiem": "35.48"
  },
  {
    "SBD": "250199",
    "HoTen": "Nguyễn Trà Trang",
    "NgaySinh": "22/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "5.50",
    "Van": "7.50",
    "MonChuyen": "9.00",
    "TongDiem": "31.50"
  },
  {
    "SBD": "250200",
    "HoTen": "Phạm Yến Trang",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.40",
    "Anh": "6.00",
    "Van": "6.75",
    "MonChuyen": "7.00",
    "TongDiem": "28.65"
  },
  {
    "SBD": "250201",
    "HoTen": "Thái Thu Trang",
    "NgaySinh": "09/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.60",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "8.00",
    "TongDiem": "29.35"
  },
  {
    "SBD": "250202",
    "HoTen": "Trần Huyền Trang",
    "NgaySinh": "04/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.20",
    "Anh": "4.75",
    "Van": "6.75",
    "MonChuyen": "7.00",
    "TongDiem": "27.20"
  },
  {
    "SBD": "250203",
    "HoTen": "Võ Quỳnh Trang",
    "NgaySinh": "05/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.80",
    "Anh": "7.25",
    "Van": "7.00",
    "MonChuyen": "6.00",
    "TongDiem": "29.05"
  },
  {
    "SBD": "250204",
    "HoTen": "Nguyễn Thị Cẩm Tú",
    "NgaySinh": "20/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.40",
    "Anh": "3.00",
    "Van": "5.75",
    "MonChuyen": "6.50",
    "TongDiem": "21.90"
  },
  {
    "SBD": "250205",
    "HoTen": "Trần Đức Tuấn",
    "NgaySinh": "27/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.60",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "8.50",
    "TongDiem": "33.85"
  },
  {
    "SBD": "250206",
    "HoTen": "Nguyễn Phan Gia Tuệ",
    "NgaySinh": "01/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.30",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "9.00",
    "TongDiem": "31.80"
  },
  {
    "SBD": "250207",
    "HoTen": "Nguyễn Thị Minh Tuyền",
    "NgaySinh": "12/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.30",
    "Anh": "5.00",
    "Van": "7.75",
    "MonChuyen": "10.00",
    "TongDiem": "32.05"
  },
  {
    "SBD": "250208",
    "HoTen": "Đậu Phan Tố Uyên",
    "NgaySinh": "13/07/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "5.00",
    "Van": "7.25",
    "MonChuyen": "12.00",
    "TongDiem": "35.25"
  },
  {
    "SBD": "250209",
    "HoTen": "Đậu Việt Hồng Uyên",
    "NgaySinh": "26/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.20",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "10.00",
    "TongDiem": "34.95"
  },
  {
    "SBD": "250210",
    "HoTen": "Lê Phương Uyên",
    "NgaySinh": "31/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "4.75",
    "Van": "7.00",
    "MonChuyen": "9.00",
    "TongDiem": "30.25"
  },
  {
    "SBD": "250211",
    "HoTen": "Nhâm Lê Tú Uyên",
    "NgaySinh": "02/04/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.20",
    "Anh": "7.75",
    "Van": "8.00",
    "MonChuyen": "13.00",
    "TongDiem": "41.45"
  },
  {
    "SBD": "250212",
    "HoTen": "Phạm Thái Uyên",
    "NgaySinh": "06/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.40",
    "Anh": "5.75",
    "Van": "5.75",
    "MonChuyen": "7.50",
    "TongDiem": "27.15"
  },
  {
    "SBD": "250213",
    "HoTen": "Phan Võ Thục Uyên",
    "NgaySinh": "03/01/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.10",
    "Anh": "6.00",
    "Van": "7.50",
    "MonChuyen": "11.25",
    "TongDiem": "35.48"
  },
  {
    "SBD": "250214",
    "HoTen": "Trần Thục Uyên",
    "NgaySinh": "14/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "6.00",
    "Van": "7.00",
    "MonChuyen": "8.50",
    "TongDiem": "31.35"
  },
  {
    "SBD": "250215",
    "HoTen": "Võ Hà Uyên",
    "NgaySinh": "17/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.50",
    "Anh": "7.25",
    "Van": "7.25",
    "MonChuyen": "8.50",
    "TongDiem": "32.75"
  },
  {
    "SBD": "250216",
    "HoTen": "Chu Quang Vinh",
    "NgaySinh": "25/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.40",
    "Anh": "8.25",
    "Van": "6.25",
    "MonChuyen": "6.00",
    "TongDiem": "26.90"
  },
  {
    "SBD": "250217",
    "HoTen": "Võ Hà Uy Vũ",
    "NgaySinh": "11/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "7.75",
    "Van": "7.00",
    "MonChuyen": "8.00",
    "TongDiem": "30.95"
  },
  {
    "SBD": "250218",
    "HoTen": "Nguyễn Cao Thảo Vy",
    "NgaySinh": "05/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.80",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "13.50",
    "TongDiem": "41.30"
  },
  {
    "SBD": "250219",
    "HoTen": "Nguyễn Đan Vy",
    "NgaySinh": "12/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.40",
    "Anh": "5.00",
    "Van": "7.25",
    "MonChuyen": "10.50",
    "TongDiem": "33.40"
  },
  {
    "SBD": "250220",
    "HoTen": "Nguyễn Hà Khánh Vy",
    "NgaySinh": "19/12/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "9.00",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "38.60"
  },
  {
    "SBD": "250221",
    "HoTen": "Nguyễn Thảo Vy",
    "NgaySinh": "18/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "6.00",
    "Anh": "7.75",
    "Van": "6.75",
    "MonChuyen": "11.00",
    "TongDiem": "37.00"
  },
  {
    "SBD": "250222",
    "HoTen": "Nguyễn Thị Bảo Vy",
    "NgaySinh": "14/03/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.20",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "10.00",
    "TongDiem": "32.20"
  },
  {
    "SBD": "250223",
    "HoTen": "Nguyễn Thị Thảo Vy",
    "NgaySinh": "25/09/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.10",
    "Anh": "8.50",
    "Van": "6.75",
    "MonChuyen": "10.00",
    "TongDiem": "35.35"
  },
  {
    "SBD": "250224",
    "HoTen": "Nguyễn Tường Vy",
    "NgaySinh": "24/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.60",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "10.50",
    "TongDiem": "36.60"
  },
  {
    "SBD": "250225",
    "HoTen": "Phan Nguyễn Hà Vy",
    "NgaySinh": "19/06/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.20",
    "Anh": "8.75",
    "Van": "5.50",
    "MonChuyen": "10.50",
    "TongDiem": "35.20"
  },
  {
    "SBD": "250226",
    "HoTen": "Phan Thị Khánh Vy",
    "NgaySinh": "23/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.90",
    "Anh": "6.50",
    "Van": "7.75",
    "MonChuyen": "11.50",
    "TongDiem": "37.40"
  },
  {
    "SBD": "250227",
    "HoTen": "Trần Hà Vy",
    "NgaySinh": "23/08/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.00",
    "Anh": "6.00",
    "Van": "7.00",
    "MonChuyen": "11.00",
    "TongDiem": "34.50"
  },
  {
    "SBD": "250228",
    "HoTen": "Nguyễn Thị Kim Xuyến",
    "NgaySinh": "01/02/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "4.60",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "7.50",
    "TongDiem": "28.60"
  },
  {
    "SBD": "250229",
    "HoTen": "Lương Hải Yến",
    "NgaySinh": "09/05/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "3.80",
    "Anh": "6.50",
    "Van": "6.25",
    "MonChuyen": "8.00",
    "TongDiem": "28.55"
  },
  {
    "SBD": "250230",
    "HoTen": "Võ Hoàng Yến",
    "NgaySinh": "28/11/2010",
    "Chuyen": "Ngữ văn",
    "Toan": "5.70",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "14.00",
    "TongDiem": "43.45"
  },
  {
    "SBD": "250231",
    "HoTen": "Đặng Ngọc Bảo An",
    "NgaySinh": "15/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "9.75",
    "Van": "6.50",
    "MonChuyen": "9.70",
    "TongDiem": "36.00"
  },
  {
    "SBD": "250232",
    "HoTen": "Dương Đặng Hà An",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.00",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "8.95",
    "TongDiem": "34.18"
  },
  {
    "SBD": "250233",
    "HoTen": "Giản Nguyễn Hà An",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.30",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "7.80",
    "TongDiem": "33.00"
  },
  {
    "SBD": "250234",
    "HoTen": "Hoàng Thái An",
    "NgaySinh": "10/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "9.50",
    "Van": "6.00",
    "MonChuyen": "13.50",
    "TongDiem": "40.85"
  },
  {
    "SBD": "250235",
    "HoTen": "Nguyễn Hà An",
    "NgaySinh": "03/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "9.50",
    "Van": "6.25",
    "MonChuyen": "10.70",
    "TongDiem": "36.30"
  },
  {
    "SBD": "250236",
    "HoTen": "Nguyễn Hà An",
    "NgaySinh": "02/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.75",
    "Van": "6.00",
    "MonChuyen": "10.90",
    "TongDiem": "37.50"
  },
  {
    "SBD": "250238",
    "HoTen": "Nguyễn Lê Hà An",
    "NgaySinh": "17/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.30",
    "Anh": "9.00",
    "Van": "7.75",
    "MonChuyen": "9.05",
    "TongDiem": "35.63"
  },
  {
    "SBD": "250239",
    "HoTen": "Nguyễn Phong An",
    "NgaySinh": "11/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.50",
    "Anh": "8.50",
    "Van": "5.50",
    "MonChuyen": "7.35",
    "TongDiem": "30.53"
  },
  {
    "SBD": "250240",
    "HoTen": "Nguyễn Thị Hoài An",
    "NgaySinh": "18/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.70",
    "Anh": "4.75",
    "Van": "7.00",
    "MonChuyen": "2.85",
    "TongDiem": "19.73"
  },
  {
    "SBD": "250242",
    "HoTen": "Phan Nguyên An",
    "NgaySinh": "10/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.20",
    "Anh": "9.50",
    "Van": "7.75",
    "MonChuyen": "12.25",
    "TongDiem": "42.83"
  },
  {
    "SBD": "250243",
    "HoTen": "Trần Hà An",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.10",
    "Anh": "9.75",
    "Van": "8.25",
    "MonChuyen": "13.75",
    "TongDiem": "42.73"
  },
  {
    "SBD": "250244",
    "HoTen": "Nguyễn Trần Gia Ân",
    "NgaySinh": "15/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "6.75",
    "Van": "7.00",
    "MonChuyen": "4.55",
    "TongDiem": "25.68"
  },
  {
    "SBD": "250245",
    "HoTen": "Bùi Thị Diệp Anh",
    "NgaySinh": "30/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.30",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "7.70",
    "TongDiem": "34.60"
  },
  {
    "SBD": "250246",
    "HoTen": "Cao Hà Anh",
    "NgaySinh": "22/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "13.15",
    "TongDiem": "42.33"
  },
  {
    "SBD": "250247",
    "HoTen": "Cung Đình Đức Anh",
    "NgaySinh": "02/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "7.75",
    "Van": "6.00",
    "MonChuyen": "3.60",
    "TongDiem": "24.55"
  },
  {
    "SBD": "250248",
    "HoTen": "Đặng Thị Phương Anh",
    "NgaySinh": "11/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "5.10",
    "TongDiem": "27.45"
  },
  {
    "SBD": "250249",
    "HoTen": "Đậu Hà Anh",
    "NgaySinh": "05/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "7.00",
    "Van": "7.25",
    "MonChuyen": "4.45",
    "TongDiem": "26.73"
  },
  {
    "SBD": "250250",
    "HoTen": "Đậu Thị Lan Anh",
    "NgaySinh": "22/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "10.00",
    "Van": "6.75",
    "MonChuyen": "15.00",
    "TongDiem": "44.45"
  },
  {
    "SBD": "250251",
    "HoTen": "Dương Quỳnh Anh",
    "NgaySinh": "05/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "11.45",
    "TongDiem": "39.08"
  },
  {
    "SBD": "250252",
    "HoTen": "Hồ Phương Anh",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "7.50",
    "Van": "6.75",
    "MonChuyen": "6.35",
    "TongDiem": "28.18"
  },
  {
    "SBD": "250253",
    "HoTen": "Hồ Quỳnh Anh",
    "NgaySinh": "30/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.90",
    "Anh": "9.75",
    "Van": "8.00",
    "MonChuyen": "13.40",
    "TongDiem": "45.75"
  },
  {
    "SBD": "250254",
    "HoTen": "Hoàng Nguyễn Phương Anh",
    "NgaySinh": "10/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "11.00",
    "TongDiem": "38.45"
  },
  {
    "SBD": "250255",
    "HoTen": "Hoàng Phạm Quỳnh Anh",
    "NgaySinh": "22/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.50",
    "Anh": "9.00",
    "Van": "6.50",
    "MonChuyen": "14.30",
    "TongDiem": "43.45"
  },
  {
    "SBD": "250256",
    "HoTen": "Hoàng Thị Châu Anh",
    "NgaySinh": "21/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "10.80",
    "TongDiem": "38.85"
  },
  {
    "SBD": "250257",
    "HoTen": "Hoàng Thị Vân Anh",
    "NgaySinh": "03/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "10.60",
    "TongDiem": "38.15"
  },
  {
    "SBD": "250258",
    "HoTen": "Hoàng Trâm Anh",
    "NgaySinh": "02/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.60",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "8.40",
    "TongDiem": "34.70"
  },
  {
    "SBD": "250259",
    "HoTen": "Hoàng Trâm Anh",
    "NgaySinh": "26/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "7.20",
    "TongDiem": "31.65"
  },
  {
    "SBD": "250260",
    "HoTen": "Lê Quỳnh Anh",
    "NgaySinh": "06/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.20",
    "Anh": "9.50",
    "Van": "6.75",
    "MonChuyen": "10.10",
    "TongDiem": "35.60"
  },
  {
    "SBD": "250261",
    "HoTen": "Mạnh Thùy Anh",
    "NgaySinh": "20/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.50",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "7.40",
    "TongDiem": "32.60"
  },
  {
    "SBD": "250262",
    "HoTen": "Nguyễn Cao Hoài Anh",
    "NgaySinh": "04/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "9.75",
    "Van": "6.25",
    "MonChuyen": "9.20",
    "TongDiem": "34.50"
  },
  {
    "SBD": "250263",
    "HoTen": "Nguyễn Đức Anh",
    "NgaySinh": "23/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.20",
    "Anh": "7.50",
    "Van": "6.25",
    "MonChuyen": "4.80",
    "TongDiem": "25.15"
  },
  {
    "SBD": "250264",
    "HoTen": "Nguyễn Hoài Anh",
    "NgaySinh": "26/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "9.95",
    "TongDiem": "34.78"
  },
  {
    "SBD": "250265",
    "HoTen": "Nguyễn Minh Anh",
    "NgaySinh": "11/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.00",
    "Anh": "9.00",
    "Van": "8.00",
    "MonChuyen": "8.15",
    "TongDiem": "33.23"
  },
  {
    "SBD": "250266",
    "HoTen": "Nguyễn Minh Anh",
    "NgaySinh": "22/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.10",
    "Anh": "8.00",
    "Van": "8.00",
    "MonChuyen": "6.35",
    "TongDiem": "29.63"
  },
  {
    "SBD": "250267",
    "HoTen": "Nguyễn Ngọc Anh",
    "NgaySinh": "24/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.90",
    "Anh": "10.00",
    "Van": "5.25",
    "MonChuyen": "14.30",
    "TongDiem": "41.60"
  },
  {
    "SBD": "250269",
    "HoTen": "Nguyễn Thảo Anh",
    "NgaySinh": "31/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.00",
    "Anh": "7.75",
    "Van": "7.25",
    "MonChuyen": "6.60",
    "TongDiem": "29.90"
  },
  {
    "SBD": "250270",
    "HoTen": "Nguyễn Thị Bảo Anh",
    "NgaySinh": "22/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "8.25",
    "Van": "7.50",
    "MonChuyen": "7.15",
    "TongDiem": "30.88"
  },
  {
    "SBD": "250271",
    "HoTen": "Nguyễn Trâm Anh",
    "NgaySinh": "08/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "10.00",
    "Van": "7.75",
    "MonChuyen": "16.90",
    "TongDiem": "47.60"
  },
  {
    "SBD": "250273",
    "HoTen": "Phạm Diệu Anh",
    "NgaySinh": "27/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "11.20",
    "TongDiem": "38.55"
  },
  {
    "SBD": "250274",
    "HoTen": "Phạm Hồng Bảo Anh",
    "NgaySinh": "17/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.10",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "6.00",
    "TongDiem": "30.60"
  },
  {
    "SBD": "250275",
    "HoTen": "Tạ Việt Anh",
    "NgaySinh": "30/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "8.80",
    "TongDiem": "33.70"
  },
  {
    "SBD": "250276",
    "HoTen": "Trần Hà Anh",
    "NgaySinh": "17/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "7.85",
    "TongDiem": "33.63"
  },
  {
    "SBD": "250277",
    "HoTen": "Trần Lê Anh",
    "NgaySinh": "05/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.60",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "10.45",
    "TongDiem": "38.53"
  },
  {
    "SBD": "250278",
    "HoTen": "Trần Phương Anh",
    "NgaySinh": "19/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.40",
    "Anh": "7.50",
    "Van": "7.25",
    "MonChuyen": "5.45",
    "TongDiem": "26.33"
  },
  {
    "SBD": "250279",
    "HoTen": "Phạm Thị Ngọc Ánh",
    "NgaySinh": "03/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.10",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "8.65",
    "TongDiem": "35.33"
  },
  {
    "SBD": "250280",
    "HoTen": "Cao Việt Bách",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "9.50",
    "Van": "6.00",
    "MonChuyen": "7.55",
    "TongDiem": "32.63"
  },
  {
    "SBD": "250281",
    "HoTen": "Phan Trọng Bách",
    "NgaySinh": "26/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.10",
    "Anh": "8.50",
    "Van": "6.50",
    "MonChuyen": "6.15",
    "TongDiem": "30.33"
  },
  {
    "SBD": "250282",
    "HoTen": "Nguyễn Võ Khánh Băng",
    "NgaySinh": "26/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.20",
    "Anh": "6.75",
    "Van": "6.00",
    "MonChuyen": "3.50",
    "TongDiem": "21.20"
  },
  {
    "SBD": "250283",
    "HoTen": "Hoàng Đức Bảo",
    "NgaySinh": "16/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.20",
    "Anh": "8.00",
    "Van": "6.75",
    "MonChuyen": "4.55",
    "TongDiem": "27.78"
  },
  {
    "SBD": "250284",
    "HoTen": "Lâm Gia Bảo",
    "NgaySinh": "18/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.00",
    "Anh": "10.00",
    "Van": "7.25",
    "MonChuyen": "16.95",
    "TongDiem": "49.68"
  },
  {
    "SBD": "250285",
    "HoTen": "Nguyễn Thiệu Bảo",
    "NgaySinh": "19/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.00",
    "Anh": "10.00",
    "Van": "6.50",
    "MonChuyen": "11.25",
    "TongDiem": "40.38"
  },
  {
    "SBD": "250286",
    "HoTen": "Trương Xuân Bảo",
    "NgaySinh": "02/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "8.25",
    "Van": "6.75",
    "MonChuyen": "3.95",
    "TongDiem": "25.33"
  },
  {
    "SBD": "250287",
    "HoTen": "Vũ Chí Bảo",
    "NgaySinh": "06/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "5.25",
    "TongDiem": "29.63"
  },
  {
    "SBD": "250289",
    "HoTen": "Đặng Hồ Bảo Châu",
    "NgaySinh": "08/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.10",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "15.35",
    "TongDiem": "42.88"
  },
  {
    "SBD": "250290",
    "HoTen": "Đậu Hoàng Châu",
    "NgaySinh": "06/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "8.50",
    "Van": "7.25",
    "MonChuyen": "6.50",
    "TongDiem": "30.70"
  },
  {
    "SBD": "250291",
    "HoTen": "Lê Minh Bảo Châu",
    "NgaySinh": "05/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.80",
    "Anh": "9.00",
    "Van": "5.75",
    "MonChuyen": "4.85",
    "TongDiem": "28.83"
  },
  {
    "SBD": "250292",
    "HoTen": "Nguyễn Bùi Bảo Châu",
    "NgaySinh": "29/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "7.50",
    "Van": "7.50",
    "MonChuyen": "5.60",
    "TongDiem": "28.00"
  },
  {
    "SBD": "250293",
    "HoTen": "Nguyễn Trần Bảo Châu",
    "NgaySinh": "14/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.50",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "7.80",
    "TongDiem": "35.20"
  },
  {
    "SBD": "250294",
    "HoTen": "Bùi Hà Bảo Chi",
    "NgaySinh": "11/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "6.20",
    "TongDiem": "30.25"
  },
  {
    "SBD": "250295",
    "HoTen": "Đào Khánh Chi",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "6.45",
    "TongDiem": "32.18"
  },
  {
    "SBD": "250296",
    "HoTen": "Đậu Quỳnh Chi",
    "NgaySinh": "08/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "8.50",
    "Van": "8.00",
    "MonChuyen": "10.20",
    "TongDiem": "37.00"
  },
  {
    "SBD": "250297",
    "HoTen": "Đinh Yên Chi",
    "NgaySinh": "21/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.90",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "4.75",
    "TongDiem": "28.28"
  },
  {
    "SBD": "250298",
    "HoTen": "Nguyễn Khánh Chi",
    "NgaySinh": "10/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.80",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "11.15",
    "TongDiem": "39.53"
  },
  {
    "SBD": "250299",
    "HoTen": "Nguyễn Lê Linh Chi",
    "NgaySinh": "26/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.40",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "8.75",
    "TongDiem": "37.03"
  },
  {
    "SBD": "250300",
    "HoTen": "Nguyễn Linh Chi",
    "NgaySinh": "29/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "9.25",
    "TongDiem": "35.73"
  },
  {
    "SBD": "250302",
    "HoTen": "Nguyễn Ngọc Khánh Chi",
    "NgaySinh": "26/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.30",
    "Anh": "9.75",
    "Van": "7.25",
    "MonChuyen": "14.55",
    "TongDiem": "44.13"
  },
  {
    "SBD": "250303",
    "HoTen": "Nguyễn Phan Uyển Chi",
    "NgaySinh": "06/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.20",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "13.45",
    "TongDiem": "40.13"
  },
  {
    "SBD": "250304",
    "HoTen": "Nguyễn Quỳnh Chi",
    "NgaySinh": "09/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "8.65",
    "TongDiem": "34.38"
  },
  {
    "SBD": "250305",
    "HoTen": "Phạm Diệp Chi",
    "NgaySinh": "07/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.00",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "12.40",
    "TongDiem": "40.35"
  },
  {
    "SBD": "250306",
    "HoTen": "Phan Thị Quỳnh Chi",
    "NgaySinh": "01/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "8.25",
    "Van": "6.75",
    "MonChuyen": "7.10",
    "TongDiem": "31.05"
  },
  {
    "SBD": "250307",
    "HoTen": "Thái Đan Chi",
    "NgaySinh": "10/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.75",
    "Van": "7.50",
    "MonChuyen": "13.25",
    "TongDiem": "42.53"
  },
  {
    "SBD": "250308",
    "HoTen": "Trần Lê Khánh Chi",
    "NgaySinh": "13/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.70",
    "Anh": "8.50",
    "Van": "7.75",
    "MonChuyen": "8.15",
    "TongDiem": "34.18"
  },
  {
    "SBD": "250309",
    "HoTen": "Trần Thị Mai Chi",
    "NgaySinh": "17/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.30",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "10.15",
    "TongDiem": "38.53"
  },
  {
    "SBD": "250310",
    "HoTen": "Nguyễn Đặng Bá Cường",
    "NgaySinh": "09/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.60",
    "Anh": "9.50",
    "Van": "6.50",
    "MonChuyen": "10.00",
    "TongDiem": "37.60"
  },
  {
    "SBD": "250311",
    "HoTen": "Võ Đình Việt Cường",
    "NgaySinh": "16/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.60",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "11.15",
    "TongDiem": "35.58"
  },
  {
    "SBD": "250313",
    "HoTen": "Lê Thảo Đan",
    "NgaySinh": "06/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "11.25",
    "TongDiem": "38.98"
  },
  {
    "SBD": "250314",
    "HoTen": "Nguyễn Phan Thảo Đan",
    "NgaySinh": "31/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "8.75",
    "Van": "7.50",
    "MonChuyen": "11.40",
    "TongDiem": "38.05"
  },
  {
    "SBD": "250315",
    "HoTen": "Nguyễn Thị Linh Đan",
    "NgaySinh": "14/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "9.45",
    "TongDiem": "35.48"
  },
  {
    "SBD": "250316",
    "HoTen": "Vương Thừa Đăng",
    "NgaySinh": "07/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.10",
    "Anh": "9.00",
    "Van": "6.50",
    "MonChuyen": "15.60",
    "TongDiem": "45.00"
  },
  {
    "SBD": "250317",
    "HoTen": "Trần Quang Danh",
    "NgaySinh": "29/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.90",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "11.90",
    "TongDiem": "40.00"
  },
  {
    "SBD": "250318",
    "HoTen": "Hoàng Ngọc Đạt",
    "NgaySinh": "02/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "11.45",
    "TongDiem": "39.53"
  },
  {
    "SBD": "250319",
    "HoTen": "Nguyễn Bảo Đạt",
    "NgaySinh": "20/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "9.65",
    "TongDiem": "36.83"
  },
  {
    "SBD": "250320",
    "HoTen": "Phan Tiến Đạt",
    "NgaySinh": "03/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.90",
    "Anh": "8.50",
    "Van": "5.50",
    "MonChuyen": "5.45",
    "TongDiem": "27.08"
  },
  {
    "SBD": "250321",
    "HoTen": "Trần Tấn Đạt",
    "NgaySinh": "29/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.20",
    "Anh": "10.00",
    "Van": "7.75",
    "MonChuyen": "10.95",
    "TongDiem": "40.38"
  },
  {
    "SBD": "250322",
    "HoTen": "Phan Ngọc Diệp",
    "NgaySinh": "18/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "9.50",
    "Van": "8.00",
    "MonChuyen": "12.75",
    "TongDiem": "42.23"
  },
  {
    "SBD": "250323",
    "HoTen": "Trần Diệp Diệp",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.90",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "8.70",
    "TongDiem": "33.95"
  },
  {
    "SBD": "250324",
    "HoTen": "Nguyễn Tài Định",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.30",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "16.75",
    "TongDiem": "48.18"
  },
  {
    "SBD": "250325",
    "HoTen": "Đoàn Thị Mai Đông",
    "NgaySinh": "20/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.60",
    "Anh": "7.75",
    "Van": "6.75",
    "MonChuyen": "3.35",
    "TongDiem": "23.13"
  },
  {
    "SBD": "250326",
    "HoTen": "Hoàng Thanh Đức",
    "NgaySinh": "18/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.00",
    "Van": "5.75",
    "MonChuyen": "8.30",
    "TongDiem": "32.60"
  },
  {
    "SBD": "250327",
    "HoTen": "Lê Minh Đức",
    "NgaySinh": "15/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.70",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "9.70",
    "TongDiem": "36.00"
  },
  {
    "SBD": "250328",
    "HoTen": "Nguyễn Lương Đức",
    "NgaySinh": "29/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.10",
    "Anh": "3.50",
    "Van": "7.00",
    "MonChuyen": "3.55",
    "TongDiem": "19.93"
  },
  {
    "SBD": "250329",
    "HoTen": "Nguyễn Thị Thuỳ Dung",
    "NgaySinh": "07/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "9.35",
    "TongDiem": "35.63"
  },
  {
    "SBD": "250330",
    "HoTen": "Nguyễn Thị Thùy Dung",
    "NgaySinh": "04/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.30",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "12.10",
    "TongDiem": "42.20"
  },
  {
    "SBD": "250331",
    "HoTen": "Nguyễn Thùy Dung",
    "NgaySinh": "08/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.90",
    "Anh": "10.00",
    "Van": "7.75",
    "MonChuyen": "11.40",
    "TongDiem": "41.75"
  },
  {
    "SBD": "250332",
    "HoTen": "Hồ Đình Dũng",
    "NgaySinh": "08/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.40",
    "Anh": "8.75",
    "Van": "7.00",
    "MonChuyen": "7.50",
    "TongDiem": "34.40"
  },
  {
    "SBD": "250333",
    "HoTen": "Hoàng Nghĩa Dũng",
    "NgaySinh": "07/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "12.60",
    "TongDiem": "39.90"
  },
  {
    "SBD": "250334",
    "HoTen": "Nguyễn Trọng Dũng",
    "NgaySinh": "18/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "13.00",
    "TongDiem": "41.15"
  },
  {
    "SBD": "250335",
    "HoTen": "Nguyễn Tuấn Dũng",
    "NgaySinh": "01/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.20",
    "Anh": "9.50",
    "Van": "7.25",
    "MonChuyen": "14.95",
    "TongDiem": "45.38"
  },
  {
    "SBD": "250336",
    "HoTen": "Hoàng Lê Nhật Dương",
    "NgaySinh": "07/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.10",
    "Anh": "10.00",
    "Van": "6.25",
    "MonChuyen": "12.00",
    "TongDiem": "40.35"
  },
  {
    "SBD": "250337",
    "HoTen": "Lê Phạm Thuỳ Dương",
    "NgaySinh": "24/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.50",
    "Anh": "9.00",
    "Van": "6.00",
    "MonChuyen": "11.00",
    "TongDiem": "37.00"
  },
  {
    "SBD": "250338",
    "HoTen": "Nguyễn Thùy Dương",
    "NgaySinh": "26/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "9.00",
    "Van": "0.0",
    "MonChuyen": "0.0",
    "TongDiem": "0.0"
  },
  {
    "SBD": "250339",
    "HoTen": "Nguyễn Tuấn Dương",
    "NgaySinh": "25/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "9.50",
    "Van": "6.75",
    "MonChuyen": "10.50",
    "TongDiem": "36.70"
  },
  {
    "SBD": "250340",
    "HoTen": "Trần Thị Ánh Dương",
    "NgaySinh": "18/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "9.75",
    "Van": "6.50",
    "MonChuyen": "12.60",
    "TongDiem": "39.95"
  },
  {
    "SBD": "250341",
    "HoTen": "Trần Mai Phương Giang",
    "NgaySinh": "05/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.20",
    "Anh": "9.75",
    "Van": "7.50",
    "MonChuyen": "13.05",
    "TongDiem": "44.03"
  },
  {
    "SBD": "250342",
    "HoTen": "Uông Lê Hương Giang",
    "NgaySinh": "24/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "6.30",
    "TongDiem": "31.85"
  },
  {
    "SBD": "250344",
    "HoTen": "Lê Hải Hà",
    "NgaySinh": "09/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "8.35",
    "TongDiem": "33.63"
  },
  {
    "SBD": "250345",
    "HoTen": "Lê Nguyễn Việt Hà",
    "NgaySinh": "17/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.30",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "5.25",
    "TongDiem": "28.93"
  },
  {
    "SBD": "250346",
    "HoTen": "Nguyễn Khánh Hà",
    "NgaySinh": "17/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "9.75",
    "Van": "8.25",
    "MonChuyen": "12.10",
    "TongDiem": "42.85"
  },
  {
    "SBD": "250347",
    "HoTen": "Nguyễn Ngọc Hà",
    "NgaySinh": "21/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "3.85",
    "TongDiem": "25.53"
  },
  {
    "SBD": "250348",
    "HoTen": "Nguyễn Thanh Hà",
    "NgaySinh": "29/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.50",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "5.95",
    "TongDiem": "28.43"
  },
  {
    "SBD": "250349",
    "HoTen": "Bùi Mạnh Hải",
    "NgaySinh": "10/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "9.55",
    "TongDiem": "35.28"
  },
  {
    "SBD": "250350",
    "HoTen": "Trần Ngọc Hải",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "8.30",
    "TongDiem": "34.85"
  },
  {
    "SBD": "250351",
    "HoTen": "Đào Hali",
    "NgaySinh": "30/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "3.00",
    "Van": "6.00",
    "MonChuyen": "3.40",
    "TongDiem": "18.70"
  },
  {
    "SBD": "250352",
    "HoTen": "Lê Thị Khánh Hân",
    "NgaySinh": "01/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.20",
    "Anh": "8.00",
    "Van": "5.75",
    "MonChuyen": "3.90",
    "TongDiem": "23.80"
  },
  {
    "SBD": "250353",
    "HoTen": "Nguyễn Thị Gia Hân",
    "NgaySinh": "21/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.20",
    "Anh": "5.25",
    "Van": "6.75",
    "MonChuyen": "3.30",
    "TongDiem": "20.15"
  },
  {
    "SBD": "250354",
    "HoTen": "Phạm Trần Gia Hân",
    "NgaySinh": "08/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "3.55",
    "TongDiem": "23.78"
  },
  {
    "SBD": "250355",
    "HoTen": "Lê Minh Hằng",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.10",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "6.80",
    "TongDiem": "31.05"
  },
  {
    "SBD": "250356",
    "HoTen": "Nguyễn Minh Hằng",
    "NgaySinh": "19/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "15.30",
    "TongDiem": "46.40"
  },
  {
    "SBD": "250357",
    "HoTen": "Nguyễn Quý Vân Hằng",
    "NgaySinh": "08/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "9.75",
    "Van": "6.00",
    "MonChuyen": "9.65",
    "TongDiem": "34.93"
  },
  {
    "SBD": "250358",
    "HoTen": "Phùng Hồng Hạnh",
    "NgaySinh": "12/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.50",
    "Anh": "9.50",
    "Van": "7.25",
    "MonChuyen": "8.85",
    "TongDiem": "35.53"
  },
  {
    "SBD": "250359",
    "HoTen": "Trương Đức Hiệp",
    "NgaySinh": "30/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.00",
    "Anh": "8.00",
    "Van": "6.50",
    "MonChuyen": "5.25",
    "TongDiem": "26.38"
  },
  {
    "SBD": "250360",
    "HoTen": "Nguyễn Minh Hiếu",
    "NgaySinh": "30/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "8.40",
    "Anh": "10.00",
    "Van": "7.50",
    "MonChuyen": "16.40",
    "TongDiem": "50.50"
  },
  {
    "SBD": "250361",
    "HoTen": "Nguyễn Minh Hiếu",
    "NgaySinh": "19/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.60",
    "Anh": "9.75",
    "Van": "6.25",
    "MonChuyen": "10.45",
    "TongDiem": "38.28"
  },
  {
    "SBD": "250362",
    "HoTen": "Võ Minh Hiếu",
    "NgaySinh": "06/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.00",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "10.15",
    "TongDiem": "36.23"
  },
  {
    "SBD": "250363",
    "HoTen": "Nguyễn Đình Hiệu",
    "NgaySinh": "15/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "8.75",
    "Van": "5.50",
    "MonChuyen": "8.40",
    "TongDiem": "31.55"
  },
  {
    "SBD": "250364",
    "HoTen": "Lê Phương Hoa",
    "NgaySinh": "25/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.90",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "13.50",
    "TongDiem": "43.90"
  },
  {
    "SBD": "250365",
    "HoTen": "Nguyễn Cảnh Hoàn",
    "NgaySinh": "24/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "9.50",
    "Van": "6.25",
    "MonChuyen": "9.90",
    "TongDiem": "37.30"
  },
  {
    "SBD": "250366",
    "HoTen": "Nguyễn Công Việt Hoàng",
    "NgaySinh": "28/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.90",
    "Anh": "10.00",
    "Van": "7.00",
    "MonChuyen": "14.50",
    "TongDiem": "45.65"
  },
  {
    "SBD": "250367",
    "HoTen": "Nguyễn Thị Minh Hồng",
    "NgaySinh": "26/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "8.80",
    "TongDiem": "34.55"
  },
  {
    "SBD": "250368",
    "HoTen": "Dương Mạnh Hùng",
    "NgaySinh": "18/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.10",
    "Anh": "10.00",
    "Van": "6.25",
    "MonChuyen": "13.65",
    "TongDiem": "42.83"
  },
  {
    "SBD": "250369",
    "HoTen": "Mạnh Phi Hùng",
    "NgaySinh": "26/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.30",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "13.70",
    "TongDiem": "42.35"
  },
  {
    "SBD": "250370",
    "HoTen": "Nguyễn Manh Hùng",
    "NgaySinh": "08/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.50",
    "Anh": "6.75",
    "Van": "5.50",
    "MonChuyen": "1.90",
    "TongDiem": "18.60"
  },
  {
    "SBD": "250371",
    "HoTen": "Hoàng Gia Hưng",
    "NgaySinh": "12/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "8.25",
    "Van": "6.25",
    "MonChuyen": "6.70",
    "TongDiem": "29.35"
  },
  {
    "SBD": "250372",
    "HoTen": "Hoàng Tiến Hưng",
    "NgaySinh": "29/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "2.55",
    "TongDiem": "24.18"
  },
  {
    "SBD": "250373",
    "HoTen": "Nguyễn Hoàng Hưng",
    "NgaySinh": "20/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "6.25",
    "Van": "7.00",
    "MonChuyen": "3.05",
    "TongDiem": "23.23"
  },
  {
    "SBD": "250374",
    "HoTen": "Nguyễn Khánh Hưng",
    "NgaySinh": "05/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "8.00",
    "Van": "6.50",
    "MonChuyen": "5.85",
    "TongDiem": "27.98"
  },
  {
    "SBD": "250375",
    "HoTen": "Trần Công Hưng",
    "NgaySinh": "06/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.70",
    "Anh": "9.00",
    "Van": "6.25",
    "MonChuyen": "5.05",
    "TongDiem": "26.53"
  },
  {
    "SBD": "250376",
    "HoTen": "Hồ Huyền Hương",
    "NgaySinh": "02/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "8.00",
    "Van": "7.50",
    "MonChuyen": "7.05",
    "TongDiem": "31.68"
  },
  {
    "SBD": "250377",
    "HoTen": "Nguyễn Dương Huy",
    "NgaySinh": "11/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "8.50",
    "Van": "6.50",
    "MonChuyen": "11.70",
    "TongDiem": "36.95"
  },
  {
    "SBD": "250378",
    "HoTen": "Phan Đức Huy",
    "NgaySinh": "20/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.70",
    "Anh": "9.25",
    "Van": "5.25",
    "MonChuyen": "12.65",
    "TongDiem": "39.18"
  },
  {
    "SBD": "250379",
    "HoTen": "Phùng Quang Huy",
    "NgaySinh": "17/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "8.50",
    "Van": "5.50",
    "MonChuyen": "5.30",
    "TongDiem": "27.55"
  },
  {
    "SBD": "250380",
    "HoTen": "Đậu Khánh Huyền",
    "NgaySinh": "14/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.30",
    "Anh": "9.75",
    "Van": "7.25",
    "MonChuyen": "10.20",
    "TongDiem": "37.60"
  },
  {
    "SBD": "250381",
    "HoTen": "Nguyễn Khánh Huyền",
    "NgaySinh": "24/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "8.50",
    "Van": "6.25",
    "MonChuyen": "4.65",
    "TongDiem": "28.13"
  },
  {
    "SBD": "250382",
    "HoTen": "Nguyễn Khánh Huyền",
    "NgaySinh": "24/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "9.75",
    "Van": "7.75",
    "MonChuyen": "13.25",
    "TongDiem": "41.88"
  },
  {
    "SBD": "250383",
    "HoTen": "Nguyễn Khánh Huyền",
    "NgaySinh": "05/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.80",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "14.35",
    "TongDiem": "46.33"
  },
  {
    "SBD": "250384",
    "HoTen": "Vũ Lê Minh Khang",
    "NgaySinh": "08/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.00",
    "Anh": "8.50",
    "Van": "6.25",
    "MonChuyen": "7.30",
    "TongDiem": "30.70"
  },
  {
    "SBD": "250385",
    "HoTen": "Nguyễn Thị Bảo Khanh",
    "NgaySinh": "08/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.70",
    "Anh": "9.00",
    "Van": "6.25",
    "MonChuyen": "6.55",
    "TongDiem": "28.78"
  },
  {
    "SBD": "250386",
    "HoTen": "Điền Văn Nam Khánh",
    "NgaySinh": "15/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.70",
    "Anh": "10.00",
    "Van": "6.50",
    "MonChuyen": "12.95",
    "TongDiem": "41.63"
  },
  {
    "SBD": "250387",
    "HoTen": "Hoàng Đăng Nghĩa Khánh",
    "NgaySinh": "20/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.30",
    "Anh": "9.75",
    "Van": "6.50",
    "MonChuyen": "14.35",
    "TongDiem": "45.08"
  },
  {
    "SBD": "250388",
    "HoTen": "Nguyễn Đình Bảo Khánh",
    "NgaySinh": "21/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.80",
    "Anh": "5.25",
    "Van": "7.25",
    "MonChuyen": "4.20",
    "TongDiem": "25.60"
  },
  {
    "SBD": "250389",
    "HoTen": "Nguyễn Nam Khánh",
    "NgaySinh": "04/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.00",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "11.60",
    "TongDiem": "39.15"
  },
  {
    "SBD": "250390",
    "HoTen": "Nguyễn Ngọc Khánh",
    "NgaySinh": "09/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.70",
    "Anh": "9.75",
    "Van": "8.00",
    "MonChuyen": "13.85",
    "TongDiem": "44.23"
  },
  {
    "SBD": "250391",
    "HoTen": "Nguyễn Quốc Khánh",
    "NgaySinh": "14/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.80",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "9.45",
    "TongDiem": "37.98"
  },
  {
    "SBD": "250392",
    "HoTen": "Nguyễn Thị Ngọc Khánh",
    "NgaySinh": "17/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "14.25",
    "TongDiem": "42.43"
  },
  {
    "SBD": "250393",
    "HoTen": "Nguyễn Vân Khánh",
    "NgaySinh": "29/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "6.25",
    "Van": "7.50",
    "MonChuyen": "6.20",
    "TongDiem": "28.15"
  },
  {
    "SBD": "250394",
    "HoTen": "Cao Đăng Khoa",
    "NgaySinh": "12/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "8.10",
    "Anh": "9.75",
    "Van": "6.25",
    "MonChuyen": "11.95",
    "TongDiem": "42.03"
  },
  {
    "SBD": "250395",
    "HoTen": "Nguyễn Duy Khoa",
    "NgaySinh": "06/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "8.90",
    "Anh": "10.00",
    "Van": "6.75",
    "MonChuyen": "16.20",
    "TongDiem": "49.95"
  },
  {
    "SBD": "250396",
    "HoTen": "Phạm Đăng Khoa",
    "NgaySinh": "23/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "9.75",
    "Van": "6.75",
    "MonChuyen": "10.75",
    "TongDiem": "37.33"
  },
  {
    "SBD": "250397",
    "HoTen": "Phạm Nguyễn Đăng Khoa",
    "NgaySinh": "29/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "8.50",
    "TongDiem": "33.10"
  },
  {
    "SBD": "250398",
    "HoTen": "Trần Xuân Khoa",
    "NgaySinh": "13/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "8.75",
    "Van": "6.00",
    "MonChuyen": "11.25",
    "TongDiem": "36.83"
  },
  {
    "SBD": "250399",
    "HoTen": "Phạm Nguyên Anh Khôi",
    "NgaySinh": "04/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "8.50",
    "Van": "6.75",
    "MonChuyen": "7.25",
    "TongDiem": "30.53"
  },
  {
    "SBD": "250400",
    "HoTen": "Phạm Nguyễn Minh Khuê",
    "NgaySinh": "26/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "12.80",
    "TongDiem": "42.40"
  },
  {
    "SBD": "250401",
    "HoTen": "Võ Ngọc Mai Khuê",
    "NgaySinh": "09/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "9.15",
    "TongDiem": "34.43"
  },
  {
    "SBD": "250403",
    "HoTen": "Nguyễn Đức Kiên",
    "NgaySinh": "23/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.00",
    "Van": "4.75",
    "MonChuyen": "8.90",
    "TongDiem": "33.10"
  },
  {
    "SBD": "250404",
    "HoTen": "Nguyễn Phan Đức Kiên",
    "NgaySinh": "18/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "7.50",
    "Van": "4.25",
    "MonChuyen": "5.05",
    "TongDiem": "25.73"
  },
  {
    "SBD": "250406",
    "HoTen": "Hoàng Anh Kiệt",
    "NgaySinh": "16/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "8.25",
    "Van": "5.50",
    "MonChuyen": "6.35",
    "TongDiem": "27.88"
  },
  {
    "SBD": "250408",
    "HoTen": "Trần Bá Kiệt",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.80",
    "Anh": "9.75",
    "Van": "6.75",
    "MonChuyen": "17.15",
    "TongDiem": "50.03"
  },
  {
    "SBD": "250409",
    "HoTen": "Nguyễn Kế Lâm",
    "NgaySinh": "24/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "7.75",
    "Van": "6.75",
    "MonChuyen": "11.65",
    "TongDiem": "36.28"
  },
  {
    "SBD": "250410",
    "HoTen": "Trần Hoàng Bảo Lâm",
    "NgaySinh": "30/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.90",
    "Anh": "9.75",
    "Van": "6.00",
    "MonChuyen": "16.10",
    "TongDiem": "46.80"
  },
  {
    "SBD": "250411",
    "HoTen": "Võ Trần Tùng Lâm",
    "NgaySinh": "27/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.20",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "4.95",
    "TongDiem": "30.38"
  },
  {
    "SBD": "250412",
    "HoTen": "Dương Thị Hồng Liên",
    "NgaySinh": "10/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "7.25",
    "Van": "6.25",
    "MonChuyen": "3.75",
    "TongDiem": "23.53"
  },
  {
    "SBD": "250413",
    "HoTen": "Nguyễn Lina",
    "NgaySinh": "23/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.90",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "9.20",
    "TongDiem": "34.95"
  },
  {
    "SBD": "250414",
    "HoTen": "Cao Phương Linh",
    "NgaySinh": "13/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "9.50",
    "Van": "7.25",
    "MonChuyen": "11.55",
    "TongDiem": "39.68"
  },
  {
    "SBD": "250415",
    "HoTen": "Đặng Gia Linh",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "10.75",
    "TongDiem": "37.48"
  },
  {
    "SBD": "250416",
    "HoTen": "Đinh Nguyễn Hà Linh",
    "NgaySinh": "02/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.30",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "11.10",
    "TongDiem": "38.45"
  },
  {
    "SBD": "250417",
    "HoTen": "Dương Nguyễn Trúc Linh",
    "NgaySinh": "11/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.30",
    "Anh": "9.00",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "38.30"
  },
  {
    "SBD": "250418",
    "HoTen": "Hoàng Khánh Linh",
    "NgaySinh": "12/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.20",
    "Anh": "9.75",
    "Van": "8.00",
    "MonChuyen": "9.00",
    "TongDiem": "38.45"
  },
  {
    "SBD": "250420",
    "HoTen": "Lê Hoàng Bảo Linh",
    "NgaySinh": "07/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.00",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "6.85",
    "TongDiem": "34.03"
  },
  {
    "SBD": "250421",
    "HoTen": "Lê Trần Phương Linh",
    "NgaySinh": "17/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.10",
    "Anh": "7.50",
    "Van": "8.00",
    "MonChuyen": "5.40",
    "TongDiem": "27.70"
  },
  {
    "SBD": "250422",
    "HoTen": "Nguyễn Hà Linh",
    "NgaySinh": "19/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "8.25",
    "Van": "6.75",
    "MonChuyen": "8.25",
    "TongDiem": "32.78"
  },
  {
    "SBD": "250424",
    "HoTen": "Nguyễn Ngọc Thảo Linh",
    "NgaySinh": "11/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.50",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "3.90",
    "TongDiem": "25.85"
  },
  {
    "SBD": "250425",
    "HoTen": "Nguyễn Thị Thùy Linh",
    "NgaySinh": "21/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "7.45",
    "TongDiem": "31.73"
  },
  {
    "SBD": "250426",
    "HoTen": "Nguyễn Trần Khánh Linh",
    "NgaySinh": "25/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "9.60",
    "TongDiem": "36.05"
  },
  {
    "SBD": "250427",
    "HoTen": "Trần Nữ Mỹ Linh",
    "NgaySinh": "22/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "8.75",
    "Van": "7.75",
    "MonChuyen": "9.75",
    "TongDiem": "35.53"
  },
  {
    "SBD": "250428",
    "HoTen": "Trần Thị Khánh Linh",
    "NgaySinh": "23/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "11.65",
    "TongDiem": "39.88"
  },
  {
    "SBD": "250430",
    "HoTen": "Trương Thùy Linh",
    "NgaySinh": "14/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "8.10",
    "TongDiem": "34.45"
  },
  {
    "SBD": "250432",
    "HoTen": "Đậu Bảo Long",
    "NgaySinh": "30/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "9.75",
    "Van": "6.25",
    "MonChuyen": "6.75",
    "TongDiem": "32.53"
  },
  {
    "SBD": "250434",
    "HoTen": "Nguyễn Thị Hồng Luyến",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "9.75",
    "Van": "8.00",
    "MonChuyen": "13.65",
    "TongDiem": "43.43"
  },
  {
    "SBD": "250435",
    "HoTen": "Nguyễn Thị Khánh Ly",
    "NgaySinh": "19/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "8.50",
    "Van": "6.75",
    "MonChuyen": "10.60",
    "TongDiem": "36.95"
  },
  {
    "SBD": "250436",
    "HoTen": "Nguyễn Ngọc Mai",
    "NgaySinh": "06/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.10",
    "Anh": "6.00",
    "Van": "6.75",
    "MonChuyen": "4.00",
    "TongDiem": "22.85"
  },
  {
    "SBD": "250438",
    "HoTen": "Đặng Nhật Minh",
    "NgaySinh": "15/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "8.65",
    "TongDiem": "35.43"
  },
  {
    "SBD": "250439",
    "HoTen": "Hoàng Bình Minh",
    "NgaySinh": "21/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "7.50",
    "Van": "5.50",
    "MonChuyen": "4.80",
    "TongDiem": "24.60"
  },
  {
    "SBD": "250440",
    "HoTen": "Hoàng Công Minh",
    "NgaySinh": "24/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "8.80",
    "TongDiem": "35.20"
  },
  {
    "SBD": "250441",
    "HoTen": "Hoàng Nhật Minh",
    "NgaySinh": "15/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "8.50",
    "Van": "6.00",
    "MonChuyen": "6.65",
    "TongDiem": "30.28"
  },
  {
    "SBD": "250443",
    "HoTen": "Lê Quốc Minh",
    "NgaySinh": "04/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "9.75",
    "Van": "6.25",
    "MonChuyen": "13.70",
    "TongDiem": "43.25"
  },
  {
    "SBD": "250444",
    "HoTen": "Ngô Quang Minh",
    "NgaySinh": "02/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "7.75",
    "Van": "5.00",
    "MonChuyen": "6.30",
    "TongDiem": "26.80"
  },
  {
    "SBD": "250445",
    "HoTen": "Nguyễn Nhật Minh",
    "NgaySinh": "22/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "3.90",
    "TongDiem": "23.40"
  },
  {
    "SBD": "250446",
    "HoTen": "Nguyễn Thiện Minh",
    "NgaySinh": "29/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.90",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "3.90",
    "TongDiem": "26.75"
  },
  {
    "SBD": "250447",
    "HoTen": "Phan Nhật Minh",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "8.50",
    "Van": "6.25",
    "MonChuyen": "4.45",
    "TongDiem": "27.03"
  },
  {
    "SBD": "250449",
    "HoTen": "Thái Đức Minh",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "9.75",
    "Van": "7.25",
    "MonChuyen": "15.25",
    "TongDiem": "46.28"
  },
  {
    "SBD": "250450",
    "HoTen": "Trần Nguyễn Quang Minh",
    "NgaySinh": "31/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.20",
    "Anh": "8.75",
    "Van": "7.00",
    "MonChuyen": "7.90",
    "TongDiem": "33.80"
  },
  {
    "SBD": "250451",
    "HoTen": "Trần Quang Minh",
    "NgaySinh": "02/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.80",
    "Anh": "9.00",
    "Van": "6.50",
    "MonChuyen": "11.90",
    "TongDiem": "40.15"
  },
  {
    "SBD": "250453",
    "HoTen": "Đậu Trần Hàn My",
    "NgaySinh": "30/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "10.00",
    "TongDiem": "36.05"
  },
  {
    "SBD": "250454",
    "HoTen": "Hồ Việt My",
    "NgaySinh": "13/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "3.10",
    "TongDiem": "25.30"
  },
  {
    "SBD": "250455",
    "HoTen": "Nguyễn Ngọc Hà My",
    "NgaySinh": "21/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "8.80",
    "TongDiem": "35.90"
  },
  {
    "SBD": "250456",
    "HoTen": "Nguyễn Trà My",
    "NgaySinh": "01/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "7.50",
    "Van": "6.25",
    "MonChuyen": "5.10",
    "TongDiem": "25.80"
  },
  {
    "SBD": "250457",
    "HoTen": "Võ Hồ Hà My",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "7.75",
    "Van": "6.50",
    "MonChuyen": "4.90",
    "TongDiem": "27.00"
  },
  {
    "SBD": "250458",
    "HoTen": "Lương My Na",
    "NgaySinh": "27/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "10.00",
    "TongDiem": "35.55"
  },
  {
    "SBD": "250459",
    "HoTen": "Đinh Hoàng Nam",
    "NgaySinh": "10/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.70",
    "Anh": "10.00",
    "Van": "7.25",
    "MonChuyen": "13.40",
    "TongDiem": "45.05"
  },
  {
    "SBD": "250461",
    "HoTen": "Lê Nhật Nam",
    "NgaySinh": "22/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.20",
    "Anh": "8.75",
    "Van": "6.25",
    "MonChuyen": "5.70",
    "TongDiem": "26.75"
  },
  {
    "SBD": "250462",
    "HoTen": "Phan Nhật Nam",
    "NgaySinh": "05/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "8.50",
    "Van": "6.50",
    "MonChuyen": "4.50",
    "TongDiem": "26.25"
  },
  {
    "SBD": "250463",
    "HoTen": "Võ Thành Nam",
    "NgaySinh": "02/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "8.25",
    "Van": "5.25",
    "MonChuyen": "3.90",
    "TongDiem": "24.05"
  },
  {
    "SBD": "250464",
    "HoTen": "Nguyễn Linh Nga",
    "NgaySinh": "30/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "9.25",
    "Van": "6.00",
    "MonChuyen": "4.35",
    "TongDiem": "26.08"
  },
  {
    "SBD": "250465",
    "HoTen": "Nguyễn Thị Bảo Nga",
    "NgaySinh": "28/04/2009",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.75",
    "Van": "6.75",
    "MonChuyen": "14.45",
    "TongDiem": "44.18"
  },
  {
    "SBD": "250467",
    "HoTen": "Đinh Nguyễn Kim Ngân",
    "NgaySinh": "15/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.80",
    "Anh": "9.25",
    "Van": "8.00",
    "MonChuyen": "10.50",
    "TongDiem": "39.80"
  },
  {
    "SBD": "250468",
    "HoTen": "Nguyễn Thị Kim Ngân",
    "NgaySinh": "23/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.50",
    "Anh": "9.25",
    "Van": "7.75",
    "MonChuyen": "8.70",
    "TongDiem": "36.55"
  },
  {
    "SBD": "250469",
    "HoTen": "Nguyễn Thị Kim Ngân",
    "NgaySinh": "22/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "0.0",
    "TongDiem": "0.0"
  },
  {
    "SBD": "250470",
    "HoTen": "Thiều Minh Ngân",
    "NgaySinh": "10/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "8.50",
    "Van": "7.25",
    "MonChuyen": "7.35",
    "TongDiem": "31.98"
  },
  {
    "SBD": "250471",
    "HoTen": "Trình Ngọc Khánh Ngân",
    "NgaySinh": "11/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.10",
    "Anh": "7.00",
    "Van": "7.25",
    "MonChuyen": "4.25",
    "TongDiem": "24.73"
  },
  {
    "SBD": "250472",
    "HoTen": "Nguyễn Công Nghĩa",
    "NgaySinh": "14/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "8.00",
    "Van": "6.00",
    "MonChuyen": "5.30",
    "TongDiem": "26.55"
  },
  {
    "SBD": "250473",
    "HoTen": "Hoàng Bảo Ngọc",
    "NgaySinh": "04/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.50",
    "Anh": "9.25",
    "Van": "6.00",
    "MonChuyen": "10.05",
    "TongDiem": "35.83"
  },
  {
    "SBD": "250474",
    "HoTen": "Ngô Nguyễn Bảo Ngọc",
    "NgaySinh": "28/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "8.20",
    "TongDiem": "33.50"
  },
  {
    "SBD": "250475",
    "HoTen": "Trần Thị Khánh Ngọc",
    "NgaySinh": "16/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "9.45",
    "TongDiem": "36.43"
  },
  {
    "SBD": "250476",
    "HoTen": "Trương Nguyễn Thiên Ngọc",
    "NgaySinh": "09/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "9.75",
    "Van": "6.50",
    "MonChuyen": "10.80",
    "TongDiem": "37.25"
  },
  {
    "SBD": "250477",
    "HoTen": "Đinh Nguyễn Thảo Nguyên",
    "NgaySinh": "14/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.75",
    "Van": "7.50",
    "MonChuyen": "16.75",
    "TongDiem": "48.38"
  },
  {
    "SBD": "250478",
    "HoTen": "Hồ Cảnh Nguyên",
    "NgaySinh": "20/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "8.75",
    "Van": "6.00",
    "MonChuyen": "8.65",
    "TongDiem": "32.03"
  },
  {
    "SBD": "250479",
    "HoTen": "Hoàng Trung Nguyên",
    "NgaySinh": "12/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "9.75",
    "Van": "6.25",
    "MonChuyen": "10.35",
    "TongDiem": "36.03"
  },
  {
    "SBD": "250480",
    "HoTen": "Nguyễn Doãn Đăng Nguyên",
    "NgaySinh": "24/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "14.00",
    "TongDiem": "42.15"
  },
  {
    "SBD": "250481",
    "HoTen": "Nguyễn Thành Nguyên",
    "NgaySinh": "14/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "9.00",
    "Van": "6.25",
    "MonChuyen": "14.50",
    "TongDiem": "42.80"
  },
  {
    "SBD": "250482",
    "HoTen": "Nguyễn Thảo Nguyên",
    "NgaySinh": "02/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.60",
    "Anh": "6.00",
    "Van": "6.25",
    "MonChuyen": "2.75",
    "TongDiem": "19.98"
  },
  {
    "SBD": "250483",
    "HoTen": "Nguyễn Thảo Nguyên",
    "NgaySinh": "31/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.20",
    "Anh": "6.25",
    "Van": "6.25",
    "MonChuyen": "5.40",
    "TongDiem": "24.80"
  },
  {
    "SBD": "250484",
    "HoTen": "Phan Thành Nguyên",
    "NgaySinh": "02/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "2.80",
    "Anh": "8.25",
    "Van": "5.50",
    "MonChuyen": "7.60",
    "TongDiem": "27.95"
  },
  {
    "SBD": "250485",
    "HoTen": "Nguyễn Thị Thanh Nhàn",
    "NgaySinh": "17/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "10.00",
    "Van": "7.75",
    "MonChuyen": "14.80",
    "TongDiem": "46.65"
  },
  {
    "SBD": "250486",
    "HoTen": "Lê Quang Nhật",
    "NgaySinh": "25/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "9.75",
    "Van": "6.75",
    "MonChuyen": "9.60",
    "TongDiem": "36.10"
  },
  {
    "SBD": "250487",
    "HoTen": "Phan Minh Nhật",
    "NgaySinh": "26/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.10",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "11.15",
    "TongDiem": "39.33"
  },
  {
    "SBD": "250488",
    "HoTen": "Chu Tuệ Nhi",
    "NgaySinh": "11/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "15.05",
    "TongDiem": "46.03"
  },
  {
    "SBD": "250489",
    "HoTen": "Lê Hạnh Nhi",
    "NgaySinh": "01/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "5.60",
    "TongDiem": "28.70"
  },
  {
    "SBD": "250490",
    "HoTen": "Lê Thị Yến Nhi",
    "NgaySinh": "30/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "9.75",
    "Van": "7.25",
    "MonChuyen": "15.35",
    "TongDiem": "44.73"
  },
  {
    "SBD": "250491",
    "HoTen": "Ngô Thảo Nhi",
    "NgaySinh": "17/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "11.70",
    "TongDiem": "39.50"
  },
  {
    "SBD": "250492",
    "HoTen": "Nguyễn Hoàng Gia Nhi",
    "NgaySinh": "03/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.10",
    "Anh": "6.25",
    "Van": "6.25",
    "MonChuyen": "3.20",
    "TongDiem": "21.40"
  },
  {
    "SBD": "250494",
    "HoTen": "Nguyễn Thị Tuệ Nhi",
    "NgaySinh": "15/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.60",
    "Anh": "8.75",
    "Van": "7.00",
    "MonChuyen": "8.00",
    "TongDiem": "33.35"
  },
  {
    "SBD": "250495",
    "HoTen": "Nguyễn Tuệ Nhi",
    "NgaySinh": "26/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.50",
    "Anh": "8.25",
    "Van": "8.25",
    "MonChuyen": "6.20",
    "TongDiem": "31.30"
  },
  {
    "SBD": "250496",
    "HoTen": "Phạm Vũ Yến Nhi",
    "NgaySinh": "26/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.80",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "9.35",
    "TongDiem": "33.58"
  },
  {
    "SBD": "250497",
    "HoTen": "Phùng Nguyễn Quỳnh Nhi",
    "NgaySinh": "26/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.40",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "4.75",
    "TongDiem": "25.28"
  },
  {
    "SBD": "250498",
    "HoTen": "Trần Gia Nhi",
    "NgaySinh": "16/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "8.25",
    "Van": "7.75",
    "MonChuyen": "8.35",
    "TongDiem": "33.63"
  },
  {
    "SBD": "250499",
    "HoTen": "Trần Thảo Nhi",
    "NgaySinh": "18/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "10.70",
    "TongDiem": "36.35"
  },
  {
    "SBD": "250500",
    "HoTen": "Nguyễn Quỳnh Như",
    "NgaySinh": "02/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.70",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "6.80",
    "TongDiem": "31.90"
  },
  {
    "SBD": "250501",
    "HoTen": "Nguyễn Quỳnh Như",
    "NgaySinh": "02/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.75",
    "Van": "7.25",
    "MonChuyen": "9.75",
    "TongDiem": "37.03"
  },
  {
    "SBD": "250502",
    "HoTen": "Dương Khánh Nhung",
    "NgaySinh": "07/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.50",
    "Van": "7.75",
    "MonChuyen": "12.90",
    "TongDiem": "42.60"
  },
  {
    "SBD": "250503",
    "HoTen": "Nguyễn Thị Tuyết Nhung",
    "NgaySinh": "08/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.70",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "8.15",
    "TongDiem": "32.18"
  },
  {
    "SBD": "250504",
    "HoTen": "Nguyễn Trịnh Đình Phát",
    "NgaySinh": "15/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.70",
    "Anh": "10.00",
    "Van": "5.75",
    "MonChuyen": "8.10",
    "TongDiem": "33.60"
  },
  {
    "SBD": "250505",
    "HoTen": "Đặng Trần Phong",
    "NgaySinh": "17/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.90",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "11.45",
    "TongDiem": "38.83"
  },
  {
    "SBD": "250507",
    "HoTen": "Đinh Quang Phong",
    "NgaySinh": "18/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.50",
    "Anh": "8.50",
    "Van": "6.25",
    "MonChuyen": "9.95",
    "TongDiem": "36.18"
  },
  {
    "SBD": "250508",
    "HoTen": "Đoàn Gia Phong",
    "NgaySinh": "30/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "10.60",
    "TongDiem": "37.60"
  },
  {
    "SBD": "250509",
    "HoTen": "Ngô Tuấn Phong",
    "NgaySinh": "12/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "6.75",
    "Van": "5.75",
    "MonChuyen": "7.20",
    "TongDiem": "28.10"
  },
  {
    "SBD": "250510",
    "HoTen": "Bùi Anh Phú",
    "NgaySinh": "02/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.70",
    "Anh": "8.75",
    "Van": "5.25",
    "MonChuyen": "2.90",
    "TongDiem": "24.05"
  },
  {
    "SBD": "250511",
    "HoTen": "Trần Hoàng Nguyên Phú",
    "NgaySinh": "16/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "8.90",
    "Anh": "10.00",
    "Van": "7.25",
    "MonChuyen": "14.60",
    "TongDiem": "48.05"
  },
  {
    "SBD": "250512",
    "HoTen": "Đặng Xuân Phúc",
    "NgaySinh": "07/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.50",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "4.85",
    "TongDiem": "29.03"
  },
  {
    "SBD": "250513",
    "HoTen": "Lê Viết Phúc",
    "NgaySinh": "21/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.60",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "7.75",
    "TongDiem": "34.23"
  },
  {
    "SBD": "250514",
    "HoTen": "Nguyễn Sỹ Phúc",
    "NgaySinh": "19/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "4.90",
    "TongDiem": "28.55"
  },
  {
    "SBD": "250515",
    "HoTen": "Trương Xuân Phúc",
    "NgaySinh": "02/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.60",
    "Anh": "5.00",
    "Van": "4.00",
    "MonChuyen": "2.45",
    "TongDiem": "16.28"
  },
  {
    "SBD": "250516",
    "HoTen": "Nguyễn Lê Phước",
    "NgaySinh": "15/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.90",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "13.75",
    "TongDiem": "43.03"
  },
  {
    "SBD": "250517",
    "HoTen": "Dương Nữ Mai Phương",
    "NgaySinh": "27/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "11.60",
    "TongDiem": "37.75"
  },
  {
    "SBD": "250518",
    "HoTen": "Nguyễn Anh Phương",
    "NgaySinh": "21/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.00",
    "Anh": "7.00",
    "Van": "7.00",
    "MonChuyen": "4.40",
    "TongDiem": "25.60"
  },
  {
    "SBD": "250519",
    "HoTen": "Nguyễn Hà Phương",
    "NgaySinh": "19/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.50",
    "Anh": "9.75",
    "Van": "8.00",
    "MonChuyen": "11.85",
    "TongDiem": "41.03"
  },
  {
    "SBD": "250520",
    "HoTen": "Nguyễn Hà Phương",
    "NgaySinh": "13/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.20",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "5.00",
    "TongDiem": "28.70"
  },
  {
    "SBD": "250521",
    "HoTen": "Nguyễn Thị Mai Phương",
    "NgaySinh": "08/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "9.00",
    "Van": "7.50",
    "MonChuyen": "8.80",
    "TongDiem": "35.50"
  },
  {
    "SBD": "250522",
    "HoTen": "Võ Thị Minh Phương",
    "NgaySinh": "17/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.10",
    "Anh": "8.25",
    "Van": "7.50",
    "MonChuyen": "8.15",
    "TongDiem": "31.08"
  },
  {
    "SBD": "250523",
    "HoTen": "Bùi Hoàng Quân",
    "NgaySinh": "03/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.10",
    "Anh": "9.00",
    "Van": "6.25",
    "MonChuyen": "6.25",
    "TongDiem": "27.73"
  },
  {
    "SBD": "250524",
    "HoTen": "Nguyễn Anh Quân",
    "NgaySinh": "06/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.50",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "6.10",
    "TongDiem": "32.15"
  },
  {
    "SBD": "250526",
    "HoTen": "Nguyễn Hoàng Quân",
    "NgaySinh": "04/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.00",
    "Anh": "9.75",
    "Van": "6.00",
    "MonChuyen": "10.30",
    "TongDiem": "36.20"
  },
  {
    "SBD": "250527",
    "HoTen": "Nguyễn Hoàng Quân",
    "NgaySinh": "21/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.70",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "9.15",
    "TongDiem": "35.43"
  },
  {
    "SBD": "250528",
    "HoTen": "Nguyễn Lê Anh Quân",
    "NgaySinh": "18/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "2.60",
    "Anh": "7.00",
    "Van": "6.00",
    "MonChuyen": "5.70",
    "TongDiem": "24.15"
  },
  {
    "SBD": "250529",
    "HoTen": "Nguyễn Tùng Quân",
    "NgaySinh": "28/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.90",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "6.65",
    "TongDiem": "30.88"
  },
  {
    "SBD": "250530",
    "HoTen": "Phạm Anh Quân",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "5.75",
    "Van": "6.50",
    "MonChuyen": "3.40",
    "TongDiem": "23.15"
  },
  {
    "SBD": "250531",
    "HoTen": "Phạm Đức Minh Quân",
    "NgaySinh": "26/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.20",
    "Anh": "7.50",
    "Van": "7.50",
    "MonChuyen": "6.30",
    "TongDiem": "30.65"
  },
  {
    "SBD": "250532",
    "HoTen": "Hồ Minh Quang",
    "NgaySinh": "13/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "5.30",
    "TongDiem": "29.00"
  },
  {
    "SBD": "250533",
    "HoTen": "Lê Viết Quang",
    "NgaySinh": "03/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.50",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "8.60",
    "TongDiem": "37.40"
  },
  {
    "SBD": "250535",
    "HoTen": "Nguyễn Tiến Quốc",
    "NgaySinh": "06/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "9.50",
    "Van": "6.50",
    "MonChuyen": "12.90",
    "TongDiem": "39.95"
  },
  {
    "SBD": "250536",
    "HoTen": "Nguyễn Văn Quyền",
    "NgaySinh": "23/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "7.00",
    "Anh": "9.50",
    "Van": "6.75",
    "MonChuyen": "10.20",
    "TongDiem": "38.55"
  },
  {
    "SBD": "250537",
    "HoTen": "Đinh Trần Bảo Quỳnh",
    "NgaySinh": "02/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.30",
    "Anh": "6.25",
    "Van": "6.25",
    "MonChuyen": "4.85",
    "TongDiem": "23.08"
  },
  {
    "SBD": "250538",
    "HoTen": "Hoàng Thúy Quỳnh",
    "NgaySinh": "19/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "10.05",
    "TongDiem": "37.88"
  },
  {
    "SBD": "250539",
    "HoTen": "Lê Mai Quỳnh",
    "NgaySinh": "28/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.30",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "6.15",
    "TongDiem": "29.53"
  },
  {
    "SBD": "250540",
    "HoTen": "Trần Đặng Linh San",
    "NgaySinh": "17/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "7.25",
    "Van": "7.00",
    "MonChuyen": "4.20",
    "TongDiem": "25.15"
  },
  {
    "SBD": "250541",
    "HoTen": "Trần Tuệ San",
    "NgaySinh": "17/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.80",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "4.75",
    "TongDiem": "26.18"
  },
  {
    "SBD": "250542",
    "HoTen": "Trần Anh Sơn",
    "NgaySinh": "25/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "8.25",
    "Van": "6.75",
    "MonChuyen": "4.45",
    "TongDiem": "28.08"
  },
  {
    "SBD": "250543",
    "HoTen": "Võ Bảo Sơn",
    "NgaySinh": "19/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "9.75",
    "TongDiem": "36.38"
  },
  {
    "SBD": "250544",
    "HoTen": "Vương Thị Linh Sương",
    "NgaySinh": "06/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.50",
    "Van": "6.50",
    "MonChuyen": "4.90",
    "TongDiem": "28.75"
  },
  {
    "SBD": "250545",
    "HoTen": "Đào Danh Tài",
    "NgaySinh": "13/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "7.00",
    "Van": "4.50",
    "MonChuyen": "2.85",
    "TongDiem": "21.18"
  },
  {
    "SBD": "250546",
    "HoTen": "Đặng An Tâm",
    "NgaySinh": "21/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.60",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "10.35",
    "TongDiem": "38.63"
  },
  {
    "SBD": "250547",
    "HoTen": "Phan Lê Thanh",
    "NgaySinh": "17/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "9.15",
    "TongDiem": "35.78"
  },
  {
    "SBD": "250548",
    "HoTen": "Trần Thanh Thanh",
    "NgaySinh": "30/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.20",
    "Anh": "7.50",
    "Van": "6.25",
    "MonChuyen": "5.80",
    "TongDiem": "26.65"
  },
  {
    "SBD": "250549",
    "HoTen": "Nguyễn Chí Thành",
    "NgaySinh": "02/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.10",
    "Anh": "9.00",
    "Van": "5.50",
    "MonChuyen": "5.15",
    "TongDiem": "28.33"
  },
  {
    "SBD": "250550",
    "HoTen": "Cao Phương Thảo",
    "NgaySinh": "13/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "11.35",
    "TongDiem": "37.53"
  },
  {
    "SBD": "250551",
    "HoTen": "Hồ Trần Phương Thảo",
    "NgaySinh": "19/08/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "15.45",
    "TongDiem": "44.78"
  },
  {
    "SBD": "250552",
    "HoTen": "Phạm Phương Thảo",
    "NgaySinh": "09/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "14.00",
    "TongDiem": "43.55"
  },
  {
    "SBD": "250553",
    "HoTen": "Phạm Thị Phương Thảo",
    "NgaySinh": "23/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "6.25",
    "Van": "7.00",
    "MonChuyen": "6.15",
    "TongDiem": "27.08"
  },
  {
    "SBD": "250554",
    "HoTen": "Trần Minh Thảo",
    "NgaySinh": "10/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.80",
    "Anh": "7.50",
    "Van": "7.50",
    "MonChuyen": "7.75",
    "TongDiem": "30.43"
  },
  {
    "SBD": "250555",
    "HoTen": "Trần Thị Thuận Thảo",
    "NgaySinh": "21/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "4.85",
    "TongDiem": "28.33"
  },
  {
    "SBD": "250556",
    "HoTen": "Trịnh Phương Thảo",
    "NgaySinh": "10/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.90",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "11.90",
    "TongDiem": "39.50"
  },
  {
    "SBD": "250558",
    "HoTen": "Hoàng Duy Thông",
    "NgaySinh": "03/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "6.50",
    "Van": "6.25",
    "MonChuyen": "5.55",
    "TongDiem": "26.48"
  },
  {
    "SBD": "250559",
    "HoTen": "Chu Minh Thu",
    "NgaySinh": "27/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.90",
    "Anh": "9.00",
    "Van": "6.50",
    "MonChuyen": "10.55",
    "TongDiem": "37.23"
  },
  {
    "SBD": "250560",
    "HoTen": "Lê Anh Thư",
    "NgaySinh": "31/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "2.90",
    "Anh": "8.00",
    "Van": "7.50",
    "MonChuyen": "8.10",
    "TongDiem": "30.55"
  },
  {
    "SBD": "250561",
    "HoTen": "Lê Đinh Anh Thư",
    "NgaySinh": "15/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.70",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "13.25",
    "TongDiem": "43.08"
  },
  {
    "SBD": "250562",
    "HoTen": "Nguyễn Lê Minh Thư",
    "NgaySinh": "05/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "5.75",
    "Van": "6.50",
    "MonChuyen": "3.80",
    "TongDiem": "22.55"
  },
  {
    "SBD": "250563",
    "HoTen": "Nguyễn Thị Anh Thư",
    "NgaySinh": "10/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "7.65",
    "TongDiem": "33.13"
  },
  {
    "SBD": "250564",
    "HoTen": "Nguyễn Thị Thanh Thư",
    "NgaySinh": "07/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "2.80",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "5.85",
    "TongDiem": "26.83"
  },
  {
    "SBD": "250565",
    "HoTen": "Nguyễn Tùng Thư",
    "NgaySinh": "13/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "9.50",
    "Van": "7.75",
    "MonChuyen": "15.10",
    "TongDiem": "45.90"
  },
  {
    "SBD": "250566",
    "HoTen": "Lê Hà Thương",
    "NgaySinh": "03/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "11.50",
    "TongDiem": "39.55"
  },
  {
    "SBD": "250567",
    "HoTen": "Nguyễn Phan Hoài Thương",
    "NgaySinh": "30/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "9.50",
    "Van": "7.25",
    "MonChuyen": "7.65",
    "TongDiem": "33.03"
  },
  {
    "SBD": "250568",
    "HoTen": "Lê Thị Bảo Thy",
    "NgaySinh": "13/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.70",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "9.50",
    "TongDiem": "34.45"
  },
  {
    "SBD": "250569",
    "HoTen": "Phan Vũ Ka Thy",
    "NgaySinh": "03/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "8.50",
    "Van": "8.00",
    "MonChuyen": "6.95",
    "TongDiem": "31.43"
  },
  {
    "SBD": "250570",
    "HoTen": "Nguyễn Bùi Thủy Tiên",
    "NgaySinh": "04/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "8.00",
    "Van": "5.25",
    "MonChuyen": "6.80",
    "TongDiem": "28.25"
  },
  {
    "SBD": "250571",
    "HoTen": "Lê Thị Thu Trà",
    "NgaySinh": "22/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.00",
    "Anh": "8.75",
    "Van": "7.00",
    "MonChuyen": "8.00",
    "TongDiem": "33.75"
  },
  {
    "SBD": "250572",
    "HoTen": "Nguyễn Bảo Trâm",
    "NgaySinh": "02/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "9.05",
    "TongDiem": "34.68"
  },
  {
    "SBD": "250573",
    "HoTen": "Nguyễn Thị Bảo Trâm",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.30",
    "Anh": "6.75",
    "Van": "7.50",
    "MonChuyen": "4.75",
    "TongDiem": "26.68"
  },
  {
    "SBD": "250574",
    "HoTen": "Trịnh Cao Bảo Trâm",
    "NgaySinh": "03/12/2009",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "9.10",
    "TongDiem": "33.75"
  },
  {
    "SBD": "250575",
    "HoTen": "Đào Lê Bảo Trân",
    "NgaySinh": "26/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "11.70",
    "TongDiem": "38.85"
  },
  {
    "SBD": "250576",
    "HoTen": "Bùi Minh Trang",
    "NgaySinh": "29/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.50",
    "Anh": "9.75",
    "Van": "7.50",
    "MonChuyen": "11.15",
    "TongDiem": "40.48"
  },
  {
    "SBD": "250577",
    "HoTen": "Cao Hoàng Hà Trang",
    "NgaySinh": "31/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.00",
    "Anh": "9.50",
    "Van": "7.75",
    "MonChuyen": "10.35",
    "TongDiem": "37.78"
  },
  {
    "SBD": "250578",
    "HoTen": "Đặng Thị Thuỳ Trang",
    "NgaySinh": "14/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.50",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "4.40",
    "TongDiem": "28.10"
  },
  {
    "SBD": "250579",
    "HoTen": "Đặng Thùy Trang",
    "NgaySinh": "24/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "8.15",
    "TongDiem": "33.13"
  },
  {
    "SBD": "250580",
    "HoTen": "Đậu Huyền Trang",
    "NgaySinh": "04/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.20",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "11.80",
    "TongDiem": "40.65"
  },
  {
    "SBD": "250581",
    "HoTen": "Dương Ngô Huyền Trang",
    "NgaySinh": "23/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.20",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "6.95",
    "TongDiem": "29.63"
  },
  {
    "SBD": "250582",
    "HoTen": "Lê Khánh Huyền Trang",
    "NgaySinh": "08/06/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "2.80",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "9.47",
    "TongDiem": "33.26"
  },
  {
    "SBD": "250583",
    "HoTen": "Nguyễn Hà Trang",
    "NgaySinh": "14/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.70",
    "Anh": "10.00",
    "Van": "7.00",
    "MonChuyen": "11.25",
    "TongDiem": "37.58"
  },
  {
    "SBD": "250584",
    "HoTen": "Nguyễn Mai Thảo Trang",
    "NgaySinh": "05/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "7.75",
    "TongDiem": "32.93"
  },
  {
    "SBD": "250585",
    "HoTen": "Nguyễn Thị Quỳnh Trang",
    "NgaySinh": "16/01/2025",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "9.75",
    "Van": "7.75",
    "MonChuyen": "12.85",
    "TongDiem": "41.48"
  },
  {
    "SBD": "250586",
    "HoTen": "Phan Thị Hồng Trang",
    "NgaySinh": "24/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.50",
    "Anh": "8.00",
    "Van": "6.50",
    "MonChuyen": "5.05",
    "TongDiem": "26.58"
  },
  {
    "SBD": "250587",
    "HoTen": "Phạm Ngọc Trọng",
    "NgaySinh": "21/12/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "7.45",
    "TongDiem": "32.48"
  },
  {
    "SBD": "250588",
    "HoTen": "Ngô Thị Oanh Trúc",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.20",
    "Anh": "9.75",
    "Van": "7.50",
    "MonChuyen": "15.40",
    "TongDiem": "46.55"
  },
  {
    "SBD": "250589",
    "HoTen": "Đặng Đình Trung",
    "NgaySinh": "20/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "8.75",
    "Van": "6.00",
    "MonChuyen": "3.20",
    "TongDiem": "25.95"
  },
  {
    "SBD": "250590",
    "HoTen": "Nguyễn Chí Trung",
    "NgaySinh": "11/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.40",
    "Anh": "8.50",
    "Van": "7.25",
    "MonChuyen": "6.05",
    "TongDiem": "31.23"
  },
  {
    "SBD": "250591",
    "HoTen": "Nguyễn Quốc Trung",
    "NgaySinh": "19/09/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.00",
    "Anh": "7.25",
    "Van": "7.00",
    "MonChuyen": "3.55",
    "TongDiem": "23.58"
  },
  {
    "SBD": "250592",
    "HoTen": "Nguyễn Ngọc Trường",
    "NgaySinh": "18/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.50",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "14.00",
    "TongDiem": "44.50"
  },
  {
    "SBD": "250594",
    "HoTen": "Lê Đình Tuấn Tú",
    "NgaySinh": "01/11/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.10",
    "Anh": "8.50",
    "Van": "6.75",
    "MonChuyen": "5.80",
    "TongDiem": "29.05"
  },
  {
    "SBD": "250596",
    "HoTen": "Võ Anh Tuấn",
    "NgaySinh": "27/04/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.80",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "12.47",
    "TongDiem": "41.01"
  },
  {
    "SBD": "250597",
    "HoTen": "Nguyễn Đức Uy",
    "NgaySinh": "16/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.10",
    "Anh": "9.25",
    "Van": "5.50",
    "MonChuyen": "13.47",
    "TongDiem": "39.06"
  },
  {
    "SBD": "250598",
    "HoTen": "Hoàng Nguyễn Thục Uyên",
    "NgaySinh": "12/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "6.50",
    "TongDiem": "29.95"
  },
  {
    "SBD": "250599",
    "HoTen": "Ngô Phương Uyên",
    "NgaySinh": "23/11/2009",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.40",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "5.00",
    "TongDiem": "26.15"
  },
  {
    "SBD": "250600",
    "HoTen": "Phan Mai Hà Uyên",
    "NgaySinh": "30/03/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.40",
    "Anh": "4.25",
    "Van": "6.50",
    "MonChuyen": "3.45",
    "TongDiem": "19.33"
  },
  {
    "SBD": "250601",
    "HoTen": "Bùi Lê Vinh",
    "NgaySinh": "05/10/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "3.60",
    "Anh": "8.50",
    "Van": "6.25",
    "MonChuyen": "3.95",
    "TongDiem": "24.28"
  },
  {
    "SBD": "250602",
    "HoTen": "Trần Thị Hà Vinh",
    "NgaySinh": "11/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.30",
    "Anh": "9.50",
    "Van": "6.25",
    "MonChuyen": "8.55",
    "TongDiem": "34.88"
  },
  {
    "SBD": "250603",
    "HoTen": "Trần Anh Vũ",
    "NgaySinh": "07/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.70",
    "Anh": "7.50",
    "Van": "6.00",
    "MonChuyen": "3.10",
    "TongDiem": "22.85"
  },
  {
    "SBD": "250604",
    "HoTen": "Mai Phương Vy",
    "NgaySinh": "12/07/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.80",
    "Anh": "8.25",
    "Van": "7.50",
    "MonChuyen": "10.20",
    "TongDiem": "35.85"
  },
  {
    "SBD": "250605",
    "HoTen": "Nguyễn Thị Hà Vy",
    "NgaySinh": "08/02/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "5.80",
    "Anh": "7.50",
    "Van": "5.75",
    "MonChuyen": "4.65",
    "TongDiem": "26.03"
  },
  {
    "SBD": "250606",
    "HoTen": "Phạm Hà Vy",
    "NgaySinh": "06/05/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "6.30",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "8.20",
    "TongDiem": "35.60"
  },
  {
    "SBD": "250607",
    "HoTen": "Cao Hải Yến",
    "NgaySinh": "22/01/2010",
    "Chuyen": "Tiếng Anh",
    "Toan": "4.60",
    "Anh": "8.00",
    "Van": "6.50",
    "MonChuyen": "4.40",
    "TongDiem": "25.70"
  },
  {
    "SBD": "250608",
    "HoTen": "Nguyễn Thị Mỹ An",
    "NgaySinh": "26/04/2010",
    "Chuyen": "Toán học",
    "Toan": "6.10",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "7.50",
    "TongDiem": "30.60"
  },
  {
    "SBD": "250609",
    "HoTen": "Trần Thị Hoài An",
    "NgaySinh": "09/02/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "7.50",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "39.90"
  },
  {
    "SBD": "250610",
    "HoTen": "Trần Văn Trường An",
    "NgaySinh": "04/04/2010",
    "Chuyen": "Toán học",
    "Toan": "5.90",
    "Anh": "5.25",
    "Van": "7.00",
    "MonChuyen": "5.50",
    "TongDiem": "26.40"
  },
  {
    "SBD": "250611",
    "HoTen": "Cao Quỳnh Anh",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Toán học",
    "Toan": "5.40",
    "Anh": "7.00",
    "Van": "7.00",
    "MonChuyen": "0",
    "TongDiem": "19.40"
  },
  {
    "SBD": "250612",
    "HoTen": "Chu Quỳnh Anh",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Toán học",
    "Toan": "9.60",
    "Anh": "9.00",
    "Van": "7.50",
    "MonChuyen": "13.75",
    "TongDiem": "46.73"
  },
  {
    "SBD": "250613",
    "HoTen": "Chu Việt Anh",
    "NgaySinh": "28/04/2010",
    "Chuyen": "Toán học",
    "Toan": "9.30",
    "Anh": "6.00",
    "Van": "7.00",
    "MonChuyen": "13.00",
    "TongDiem": "41.80"
  },
  {
    "SBD": "250615",
    "HoTen": "Nguyễn Lê Hà Anh",
    "NgaySinh": "16/02/2010",
    "Chuyen": "Toán học",
    "Toan": "8.90",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "12.00",
    "TongDiem": "43.65"
  },
  {
    "SBD": "250616",
    "HoTen": "Nguyễn Lê Hà Anh",
    "NgaySinh": "26/10/2010",
    "Chuyen": "Toán học",
    "Toan": "6.20",
    "Anh": "5.50",
    "Van": "6.25",
    "MonChuyen": "4.00",
    "TongDiem": "23.95"
  },
  {
    "SBD": "250617",
    "HoTen": "Nguyễn Nam Anh",
    "NgaySinh": "09/09/2010",
    "Chuyen": "Toán học",
    "Toan": "3.60",
    "Anh": "5.00",
    "Van": "6.50",
    "MonChuyen": "1.50",
    "TongDiem": "17.35"
  },
  {
    "SBD": "250618",
    "HoTen": "Nguyễn Phúc Hoàng Anh",
    "NgaySinh": "20/10/2010",
    "Chuyen": "Toán học",
    "Toan": "6.80",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "7.25",
    "TongDiem": "30.68"
  },
  {
    "SBD": "250619",
    "HoTen": "Nguyễn Tất Hoàng Anh",
    "NgaySinh": "07/02/2010",
    "Chuyen": "Toán học",
    "Toan": "7.00",
    "Anh": "7.00",
    "Van": "6.75",
    "MonChuyen": "14.00",
    "TongDiem": "41.75"
  },
  {
    "SBD": "250620",
    "HoTen": "Nguyễn Trâm Anh",
    "NgaySinh": "16/07/2010",
    "Chuyen": "Toán học",
    "Toan": "5.10",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "7.25",
    "TongDiem": "29.23"
  },
  {
    "SBD": "250621",
    "HoTen": "Nguyễn Trần Quỳnh Anh",
    "NgaySinh": "29/12/2010",
    "Chuyen": "Toán học",
    "Toan": "9.40",
    "Anh": "8.75",
    "Van": "7.00",
    "MonChuyen": "13.75",
    "TongDiem": "45.78"
  },
  {
    "SBD": "250622",
    "HoTen": "Phạm Thị Quỳnh Anh",
    "NgaySinh": "29/03/2010",
    "Chuyen": "Toán học",
    "Toan": "7.90",
    "Anh": "8.00",
    "Van": "7.75",
    "MonChuyen": "9.00",
    "TongDiem": "37.15"
  },
  {
    "SBD": "250623",
    "HoTen": "Trần Nữ Minh Anh",
    "NgaySinh": "27/08/2010",
    "Chuyen": "Toán học",
    "Toan": "7.90",
    "Anh": "6.00",
    "Van": "7.00",
    "MonChuyen": "8.50",
    "TongDiem": "33.65"
  },
  {
    "SBD": "250624",
    "HoTen": "Trần Tuấn Anh",
    "NgaySinh": "15/07/2010",
    "Chuyen": "Toán học",
    "Toan": "8.30",
    "Anh": "6.25",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "38.55"
  },
  {
    "SBD": "250625",
    "HoTen": "Trịnh Xuân Tuấn Anh",
    "NgaySinh": "30/10/2010",
    "Chuyen": "Toán học",
    "Toan": "7.10",
    "Anh": "8.25",
    "Van": "6.75",
    "MonChuyen": "9.00",
    "TongDiem": "35.60"
  },
  {
    "SBD": "250626",
    "HoTen": "Nguyễn Hữu Âu",
    "NgaySinh": "07/01/2010",
    "Chuyen": "Toán học",
    "Toan": "10.00",
    "Anh": "10.00",
    "Van": "7.00",
    "MonChuyen": "14.50",
    "TongDiem": "48.75"
  },
  {
    "SBD": "250627",
    "HoTen": "Phan Văn Trần Bách",
    "NgaySinh": "12/03/2010",
    "Chuyen": "Toán học",
    "Toan": "6.40",
    "Anh": "6.75",
    "Van": "5.00",
    "MonChuyen": "6.00",
    "TongDiem": "27.15"
  },
  {
    "SBD": "250628",
    "HoTen": "Thái Việt Bách",
    "NgaySinh": "26/05/2010",
    "Chuyen": "Toán học",
    "Toan": "9.10",
    "Anh": "9.50",
    "Van": "6.25",
    "MonChuyen": "15.00",
    "TongDiem": "47.35"
  },
  {
    "SBD": "250629",
    "HoTen": "Lê Thị Thanh Băng",
    "NgaySinh": "22/11/2010",
    "Chuyen": "Toán học",
    "Toan": "5.80",
    "Anh": "7.50",
    "Van": "7.50",
    "MonChuyen": "4.50",
    "TongDiem": "27.55"
  },
  {
    "SBD": "250630",
    "HoTen": "Hồ Gia Bảo",
    "NgaySinh": "03/04/2010",
    "Chuyen": "Toán học",
    "Toan": "8.30",
    "Anh": "7.00",
    "Van": "6.75",
    "MonChuyen": "8.25",
    "TongDiem": "34.43"
  },
  {
    "SBD": "250631",
    "HoTen": "Hồ Quốc Bảo",
    "NgaySinh": "24/02/2010",
    "Chuyen": "Toán học",
    "Toan": "8.80",
    "Anh": "4.75",
    "Van": "5.75",
    "MonChuyen": "8.25",
    "TongDiem": "31.68"
  },
  {
    "SBD": "250632",
    "HoTen": "Hoàng Ngọc Bảo",
    "NgaySinh": "01/08/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "11.25",
    "TongDiem": "41.48"
  },
  {
    "SBD": "250634",
    "HoTen": "Nguyễn Lưu Thái Bảo",
    "NgaySinh": "07/09/2010",
    "Chuyen": "Toán học",
    "Toan": "6.40",
    "Anh": "4.75",
    "Van": "7.00",
    "MonChuyen": "6.00",
    "TongDiem": "27.15"
  },
  {
    "SBD": "250635",
    "HoTen": "Trần Quốc Bảo",
    "NgaySinh": "07/02/2010",
    "Chuyen": "Toán học",
    "Toan": "6.90",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "8.00",
    "TongDiem": "34.15"
  },
  {
    "SBD": "250636",
    "HoTen": "Bùi Đình Bình",
    "NgaySinh": "07/02/2010",
    "Chuyen": "Toán học",
    "Toan": "6.70",
    "Anh": "7.00",
    "Van": "6.75",
    "MonChuyen": "7.25",
    "TongDiem": "31.33"
  },
  {
    "SBD": "250637",
    "HoTen": "Chu Minh Châu",
    "NgaySinh": "09/05/2010",
    "Chuyen": "Toán học",
    "Toan": "7.70",
    "Anh": "8.50",
    "Van": "6.25",
    "MonChuyen": "5.50",
    "TongDiem": "30.70"
  },
  {
    "SBD": "250638",
    "HoTen": "Lê Bảo Châu",
    "NgaySinh": "19/09/2010",
    "Chuyen": "Toán học",
    "Toan": "6.80",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "12.00",
    "TongDiem": "40.80"
  },
  {
    "SBD": "250639",
    "HoTen": "Trần Thảo Châu",
    "NgaySinh": "26/08/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "7.00",
    "Van": "6.00",
    "MonChuyen": "11.00",
    "TongDiem": "37.90"
  },
  {
    "SBD": "250640",
    "HoTen": "Đặng Quỳnh Chi",
    "NgaySinh": "07/06/2010",
    "Chuyen": "Toán học",
    "Toan": "8.70",
    "Anh": "8.00",
    "Van": "6.75",
    "MonChuyen": "13.00",
    "TongDiem": "42.95"
  },
  {
    "SBD": "250641",
    "HoTen": "Đỗ Tùng Chi",
    "NgaySinh": "01/02/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "9.50",
    "Van": "6.75",
    "MonChuyen": "15.00",
    "TongDiem": "46.75"
  },
  {
    "SBD": "250643",
    "HoTen": "Võ Minh Chiến",
    "NgaySinh": "11/03/2010",
    "Chuyen": "Toán học",
    "Toan": "8.10",
    "Anh": "7.00",
    "Van": "7.25",
    "MonChuyen": "13.50",
    "TongDiem": "42.60"
  },
  {
    "SBD": "250644",
    "HoTen": "Phạm Thành Chương",
    "NgaySinh": "15/11/2010",
    "Chuyen": "Toán học",
    "Toan": "7.80",
    "Anh": "5.75",
    "Van": "6.75",
    "MonChuyen": "9.50",
    "TongDiem": "34.55"
  },
  {
    "SBD": "250645",
    "HoTen": "Võ Minh Cường",
    "NgaySinh": "11/03/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "11.50",
    "TongDiem": "38.35"
  },
  {
    "SBD": "250646",
    "HoTen": "Nguyễn Phúc Dân",
    "NgaySinh": "15/01/2010",
    "Chuyen": "Toán học",
    "Toan": "6.60",
    "Anh": "7.75",
    "Van": "4.50",
    "MonChuyen": "3.50",
    "TongDiem": "24.10"
  },
  {
    "SBD": "250647",
    "HoTen": "Lê Đức Hải Đăng",
    "NgaySinh": "15/09/2010",
    "Chuyen": "Toán học",
    "Toan": "4.70",
    "Anh": "5.75",
    "Van": "6.00",
    "MonChuyen": "1.00",
    "TongDiem": "17.95"
  },
  {
    "SBD": "250648",
    "HoTen": "Nguyễn Hải Đăng",
    "NgaySinh": "30/07/2010",
    "Chuyen": "Toán học",
    "Toan": "7.80",
    "Anh": "6.75",
    "Van": "6.75",
    "MonChuyen": "6.00",
    "TongDiem": "30.30"
  },
  {
    "SBD": "250649",
    "HoTen": "Nguyễn Nhật Đăng",
    "NgaySinh": "07/05/2010",
    "Chuyen": "Toán học",
    "Toan": "9.00",
    "Anh": "8.75",
    "Van": "7.75",
    "MonChuyen": "13.50",
    "TongDiem": "45.75"
  },
  {
    "SBD": "250650",
    "HoTen": "Lưu Đức Đạt",
    "NgaySinh": "29/04/2010",
    "Chuyen": "Toán học",
    "Toan": "5.40",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "4.50",
    "TongDiem": "26.65"
  },
  {
    "SBD": "250651",
    "HoTen": "Nguyễn Hồ Tuấn Đạt",
    "NgaySinh": "09/08/2010",
    "Chuyen": "Toán học",
    "Toan": "4.90",
    "Anh": "5.50",
    "Van": "7.25",
    "MonChuyen": "4.50",
    "TongDiem": "24.40"
  },
  {
    "SBD": "250652",
    "HoTen": "Võ Sơn Đạt",
    "NgaySinh": "02/06/2010",
    "Chuyen": "Toán học",
    "Toan": "9.80",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "13.75",
    "TongDiem": "46.43"
  },
  {
    "SBD": "250653",
    "HoTen": "Võ Thành Đạt",
    "NgaySinh": "22/11/2010",
    "Chuyen": "Toán học",
    "Toan": "4.60",
    "Anh": "3.25",
    "Van": "5.75",
    "MonChuyen": "5.00",
    "TongDiem": "21.10"
  },
  {
    "SBD": "250654",
    "HoTen": "Ngô Phương Đông",
    "NgaySinh": "06/01/2010",
    "Chuyen": "Toán học",
    "Toan": "7.90",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "10.50",
    "TongDiem": "38.65"
  },
  {
    "SBD": "250655",
    "HoTen": "Đậu Minh Đức",
    "NgaySinh": "08/07/2010",
    "Chuyen": "Toán học",
    "Toan": "8.50",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "14.50",
    "TongDiem": "46.75"
  },
  {
    "SBD": "250656",
    "HoTen": "Hoàng Minh Đức",
    "NgaySinh": "27/04/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "5.75",
    "Van": "6.25",
    "MonChuyen": "10.00",
    "TongDiem": "35.40"
  },
  {
    "SBD": "250657",
    "HoTen": "Nguyễn Hồng Đức",
    "NgaySinh": "18/03/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "9.75",
    "Van": "6.25",
    "MonChuyen": "12.00",
    "TongDiem": "42.60"
  },
  {
    "SBD": "250658",
    "HoTen": "Nguyễn Minh Đức",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.90",
    "Anh": "6.75",
    "Van": "6.50",
    "MonChuyen": "8.50",
    "TongDiem": "34.90"
  },
  {
    "SBD": "250659",
    "HoTen": "Trần Đình Đức",
    "NgaySinh": "03/04/2010",
    "Chuyen": "Toán học",
    "Toan": "7.50",
    "Anh": "6.75",
    "Van": "6.00",
    "MonChuyen": "11.50",
    "TongDiem": "37.50"
  },
  {
    "SBD": "250660",
    "HoTen": "Trần Minh Đức",
    "NgaySinh": "05/07/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "7.50",
    "Van": "6.75",
    "MonChuyen": "8.25",
    "TongDiem": "35.03"
  },
  {
    "SBD": "250661",
    "HoTen": "Đặng Thị Phương Dung",
    "NgaySinh": "30/07/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "40.15"
  },
  {
    "SBD": "250662",
    "HoTen": "Bùi Tiến Dũng",
    "NgaySinh": "23/11/2010",
    "Chuyen": "Toán học",
    "Toan": "8.10",
    "Anh": "7.25",
    "Van": "6.25",
    "MonChuyen": "10.50",
    "TongDiem": "37.35"
  },
  {
    "SBD": "250663",
    "HoTen": "Cao Khắc Dũng",
    "NgaySinh": "08/05/2010",
    "Chuyen": "Toán học",
    "Toan": "9.30",
    "Anh": "10.00",
    "Van": "7.00",
    "MonChuyen": "14.75",
    "TongDiem": "48.43"
  },
  {
    "SBD": "250664",
    "HoTen": "Lê Anh Dũng",
    "NgaySinh": "19/02/2010",
    "Chuyen": "Toán học",
    "Toan": "6.80",
    "Anh": "7.50",
    "Van": "5.50",
    "MonChuyen": "9.00",
    "TongDiem": "33.30"
  },
  {
    "SBD": "250665",
    "HoTen": "Lê Việt Dũng",
    "NgaySinh": "11/06/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "12.25",
    "TongDiem": "41.63"
  },
  {
    "SBD": "250666",
    "HoTen": "Nguyễn Đình Anh Dũng",
    "NgaySinh": "09/09/2010",
    "Chuyen": "Toán học",
    "Toan": "3.60",
    "Anh": "4.75",
    "Van": "5.75",
    "MonChuyen": "0.50",
    "TongDiem": "14.85"
  },
  {
    "SBD": "250667",
    "HoTen": "Nguyễn Tiến Dũng",
    "NgaySinh": "02/11/2010",
    "Chuyen": "Toán học",
    "Toan": "5.40",
    "Anh": "6.50",
    "Van": "6.25",
    "MonChuyen": "4.75",
    "TongDiem": "25.28"
  },
  {
    "SBD": "250668",
    "HoTen": "Trần Tiến Dũng",
    "NgaySinh": "20/01/2010",
    "Chuyen": "Toán học",
    "Toan": "9.50",
    "Anh": "8.75",
    "Van": "6.25",
    "MonChuyen": "15.00",
    "TongDiem": "47.00"
  },
  {
    "SBD": "250669",
    "HoTen": "Trần Tuấn Dũng",
    "NgaySinh": "27/07/2010",
    "Chuyen": "Toán học",
    "Toan": "4.80",
    "Anh": "5.25",
    "Van": "6.25",
    "MonChuyen": "4.50",
    "TongDiem": "23.05"
  },
  {
    "SBD": "250670",
    "HoTen": "Tưởng Đăng Trung Dũng",
    "NgaySinh": "12/05/2010",
    "Chuyen": "Toán học",
    "Toan": "6.10",
    "Anh": "5.00",
    "Van": "6.00",
    "MonChuyen": "2.50",
    "TongDiem": "20.85"
  },
  {
    "SBD": "250671",
    "HoTen": "Trần Thuỳ Dương",
    "NgaySinh": "30/08/2010",
    "Chuyen": "Toán học",
    "Toan": "6.20",
    "Anh": "5.75",
    "Van": "7.50",
    "MonChuyen": "2.50",
    "TongDiem": "23.20"
  },
  {
    "SBD": "250672",
    "HoTen": "Nguyễn Đức Duy",
    "NgaySinh": "16/06/2010",
    "Chuyen": "Toán học",
    "Toan": "7.70",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "13.00",
    "TongDiem": "43.20"
  },
  {
    "SBD": "250673",
    "HoTen": "Nguyễn Hoàng Duy",
    "NgaySinh": "19/07/2010",
    "Chuyen": "Toán học",
    "Toan": "9.80",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "16.50",
    "TongDiem": "49.80"
  },
  {
    "SBD": "250674",
    "HoTen": "Nguyễn Minh Duy",
    "NgaySinh": "28/12/2010",
    "Chuyen": "Toán học",
    "Toan": "7.30",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "10.50",
    "TongDiem": "39.05"
  },
  {
    "SBD": "250675",
    "HoTen": "Trần Tuấn Duy",
    "NgaySinh": "27/04/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "11.50",
    "TongDiem": "41.85"
  },
  {
    "SBD": "250676",
    "HoTen": "Cao Thị Phương Hà",
    "NgaySinh": "22/02/2010",
    "Chuyen": "Toán học",
    "Toan": "5.40",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "2.50",
    "TongDiem": "22.40"
  },
  {
    "SBD": "250678",
    "HoTen": "Nguyễn Thị Ngọc Hà",
    "NgaySinh": "18/01/2010",
    "Chuyen": "Toán học",
    "Toan": "7.70",
    "Anh": "7.75",
    "Van": "6.75",
    "MonChuyen": "11.50",
    "TongDiem": "39.45"
  },
  {
    "SBD": "250679",
    "HoTen": "Nguyễn Thị Hiền",
    "NgaySinh": "17/01/2010",
    "Chuyen": "Toán học",
    "Toan": "6.60",
    "Anh": "5.50",
    "Van": "7.25",
    "MonChuyen": "8.50",
    "TongDiem": "32.10"
  },
  {
    "SBD": "250680",
    "HoTen": "Nguyễn Công Hiếu",
    "NgaySinh": "28/08/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "11.00",
    "TongDiem": "40.35"
  },
  {
    "SBD": "250681",
    "HoTen": "Nguyễn Thành Hiếu",
    "NgaySinh": "12/05/2010",
    "Chuyen": "Toán học",
    "Toan": "8.80",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "14.00",
    "TongDiem": "45.30"
  },
  {
    "SBD": "250682",
    "HoTen": "Đinh Xuân Hiệu",
    "NgaySinh": "22/10/2010",
    "Chuyen": "Toán học",
    "Toan": "7.50",
    "Anh": "8.00",
    "Van": "6.00",
    "MonChuyen": "6.00",
    "TongDiem": "30.50"
  },
  {
    "SBD": "250683",
    "HoTen": "Dương Việt Hoàn",
    "NgaySinh": "15/11/2010",
    "Chuyen": "Toán học",
    "Toan": "6.40",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "9.00",
    "TongDiem": "32.40"
  },
  {
    "SBD": "250684",
    "HoTen": "Nguyễn Huy Hoàng",
    "NgaySinh": "14/06/2010",
    "Chuyen": "Toán học",
    "Toan": "5.80",
    "Anh": "5.25",
    "Van": "6.00",
    "MonChuyen": "4.50",
    "TongDiem": "23.80"
  },
  {
    "SBD": "250685",
    "HoTen": "Nguyễn Thức Lê Hoàng",
    "NgaySinh": "09/04/2010",
    "Chuyen": "Toán học",
    "Toan": "6.10",
    "Anh": "5.00",
    "Van": "6.25",
    "MonChuyen": "5.50",
    "TongDiem": "25.60"
  },
  {
    "SBD": "250686",
    "HoTen": "Trần Bảo Hoàng",
    "NgaySinh": "22/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.80",
    "Anh": "7.00",
    "Van": "6.00",
    "MonChuyen": "14.50",
    "TongDiem": "43.55"
  },
  {
    "SBD": "250687",
    "HoTen": "Trịnh Huy Hoàng",
    "NgaySinh": "09/10/2010",
    "Chuyen": "Toán học",
    "Toan": "4.80",
    "Anh": "4.75",
    "Van": "5.75",
    "MonChuyen": "0.50",
    "TongDiem": "16.05"
  },
  {
    "SBD": "250688",
    "HoTen": "Vũ Huy Hoàng",
    "NgaySinh": "02/05/2010",
    "Chuyen": "Toán học",
    "Toan": "7.20",
    "Anh": "4.50",
    "Van": "7.00",
    "MonChuyen": "6.00",
    "TongDiem": "27.70"
  },
  {
    "SBD": "250689",
    "HoTen": "Phan Huy Hoạt",
    "NgaySinh": "02/08/2010",
    "Chuyen": "Toán học",
    "Toan": "8.10",
    "Anh": "7.25",
    "Van": "7.50",
    "MonChuyen": "12.00",
    "TongDiem": "40.85"
  },
  {
    "SBD": "250690",
    "HoTen": "Nguyễn Đức Hùng",
    "NgaySinh": "12/05/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "9.50",
    "Van": "6.25",
    "MonChuyen": "11.50",
    "TongDiem": "41.60"
  },
  {
    "SBD": "250691",
    "HoTen": "Lê Chấn Hưng",
    "NgaySinh": "14/12/2010",
    "Chuyen": "Toán học",
    "Toan": "8.90",
    "Anh": "9.00",
    "Van": "6.50",
    "MonChuyen": "12.00",
    "TongDiem": "42.40"
  },
  {
    "SBD": "250692",
    "HoTen": "Nguyễn Hữu Tấn Hưng",
    "NgaySinh": "14/02/2010",
    "Chuyen": "Toán học",
    "Toan": "6.70",
    "Anh": "8.00",
    "Van": "6.75",
    "MonChuyen": "13.00",
    "TongDiem": "40.95"
  },
  {
    "SBD": "250693",
    "HoTen": "Nguyễn Tuấn Hưng",
    "NgaySinh": "07/08/2010",
    "Chuyen": "Toán học",
    "Toan": "3.80",
    "Anh": "3.00",
    "Van": "4.50",
    "MonChuyen": "2.00",
    "TongDiem": "14.30"
  },
  {
    "SBD": "250694",
    "HoTen": "Đào Việt Huy",
    "NgaySinh": "07/02/2010",
    "Chuyen": "Toán học",
    "Toan": "6.10",
    "Anh": "7.00",
    "Van": "6.25",
    "MonChuyen": "2.00",
    "TongDiem": "22.35"
  },
  {
    "SBD": "250695",
    "HoTen": "Kiều Gia Huy",
    "NgaySinh": "20/07/2010",
    "Chuyen": "Toán học",
    "Toan": "5.40",
    "Anh": "5.00",
    "Van": "6.50",
    "MonChuyen": "2.00",
    "TongDiem": "19.90"
  },
  {
    "SBD": "250696",
    "HoTen": "Nguyễn Chí Huy",
    "NgaySinh": "07/03/2010",
    "Chuyen": "Toán học",
    "Toan": "7.30",
    "Anh": "7.25",
    "Van": "6.75",
    "MonChuyen": "7.25",
    "TongDiem": "32.18"
  },
  {
    "SBD": "250697",
    "HoTen": "Nguyễn Đình Huy",
    "NgaySinh": "14/04/2010",
    "Chuyen": "Toán học",
    "Toan": "3.70",
    "Anh": "7.00",
    "Van": "6.75",
    "MonChuyen": "0.50",
    "TongDiem": "18.20"
  },
  {
    "SBD": "250698",
    "HoTen": "Nguyễn Đình Quang Huy",
    "NgaySinh": "20/02/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "8.25",
    "Van": "7.25",
    "MonChuyen": "14.50",
    "TongDiem": "45.65"
  },
  {
    "SBD": "250699",
    "HoTen": "Nguyễn Đức Huy",
    "NgaySinh": "12/06/2010",
    "Chuyen": "Toán học",
    "Toan": "6.40",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "5.50",
    "TongDiem": "29.90"
  },
  {
    "SBD": "250700",
    "HoTen": "Phan Quang Huy",
    "NgaySinh": "19/07/2010",
    "Chuyen": "Toán học",
    "Toan": "8.20",
    "Anh": "8.25",
    "Van": "6.75",
    "MonChuyen": "6.50",
    "TongDiem": "32.95"
  },
  {
    "SBD": "250701",
    "HoTen": "Trần Chí Huy",
    "NgaySinh": "21/04/2010",
    "Chuyen": "Toán học",
    "Toan": "9.80",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "8.75",
    "TongDiem": "38.43"
  },
  {
    "SBD": "250702",
    "HoTen": "Trần Đình Gia Huy",
    "NgaySinh": "22/10/2010",
    "Chuyen": "Toán học",
    "Toan": "10.00",
    "Anh": "8.50",
    "Van": "7.25",
    "MonChuyen": "13.25",
    "TongDiem": "45.63"
  },
  {
    "SBD": "250703",
    "HoTen": "Nguyễn Thị Ngọc Huyền",
    "NgaySinh": "26/07/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "9.50",
    "TongDiem": "36.75"
  },
  {
    "SBD": "250704",
    "HoTen": "Nguyễn Trần Minh Khang",
    "NgaySinh": "18/08/2010",
    "Chuyen": "Toán học",
    "Toan": "6.50",
    "Anh": "7.00",
    "Van": "6.50",
    "MonChuyen": "2.00",
    "TongDiem": "23.00"
  },
  {
    "SBD": "250705",
    "HoTen": "Phan Thái Khang",
    "NgaySinh": "24/11/2010",
    "Chuyen": "Toán học",
    "Toan": "5.10",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "9.00",
    "TongDiem": "32.10"
  },
  {
    "SBD": "250706",
    "HoTen": "Đặng Nguyễn Vân Khánh",
    "NgaySinh": "19/06/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "6.75",
    "Van": "7.75",
    "MonChuyen": "8.50",
    "TongDiem": "35.25"
  },
  {
    "SBD": "250707",
    "HoTen": "Phạm Nam Khánh",
    "NgaySinh": "07/12/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "5.75",
    "Van": "7.50",
    "MonChuyen": "9.50",
    "TongDiem": "35.50"
  },
  {
    "SBD": "250709",
    "HoTen": "Nguyễn Bùi Minh Khôi",
    "NgaySinh": "31/01/2010",
    "Chuyen": "Toán học",
    "Toan": "9.80",
    "Anh": "8.50",
    "Van": "7.25",
    "MonChuyen": "12.00",
    "TongDiem": "43.55"
  },
  {
    "SBD": "250710",
    "HoTen": "Ngụy Trần Kiên",
    "NgaySinh": "24/05/2010",
    "Chuyen": "Toán học",
    "Toan": "5.70",
    "Anh": "5.25",
    "Van": "6.25",
    "MonChuyen": "11.00",
    "TongDiem": "33.70"
  },
  {
    "SBD": "250711",
    "HoTen": "Lê Đình Trung Kiên",
    "NgaySinh": "20/04/2010",
    "Chuyen": "Toán học",
    "Toan": "3.40",
    "Anh": "6.25",
    "Van": "5.50",
    "MonChuyen": "0.50",
    "TongDiem": "15.90"
  },
  {
    "SBD": "250712",
    "HoTen": "Nguyễn Đình Kiên",
    "NgaySinh": "12/03/2010",
    "Chuyen": "Toán học",
    "Toan": "7.30",
    "Anh": "9.00",
    "Van": "6.25",
    "MonChuyen": "14.50",
    "TongDiem": "44.30"
  },
  {
    "SBD": "250713",
    "HoTen": "Hồ Anh Kiệt",
    "NgaySinh": "23/04/2010",
    "Chuyen": "Toán học",
    "Toan": "5.60",
    "Anh": "4.00",
    "Van": "5.75",
    "MonChuyen": "2.00",
    "TongDiem": "18.35"
  },
  {
    "SBD": "250714",
    "HoTen": "Nguyễn Lê Hoàng Lâm",
    "NgaySinh": "05/02/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "14.50",
    "TongDiem": "46.15"
  },
  {
    "SBD": "250715",
    "HoTen": "Nguyễn Tiến Lâm",
    "NgaySinh": "17/05/2010",
    "Chuyen": "Toán học",
    "Toan": "6.80",
    "Anh": "6.75",
    "Van": "6.75",
    "MonChuyen": "8.50",
    "TongDiem": "33.05"
  },
  {
    "SBD": "250716",
    "HoTen": "Nguyễn Tôn Hoàng Lâm",
    "NgaySinh": "11/03/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "7.25",
    "Van": "6.00",
    "MonChuyen": "10.50",
    "TongDiem": "37.00"
  },
  {
    "SBD": "250717",
    "HoTen": "Phạm Đình Lâm",
    "NgaySinh": "02/05/2010",
    "Chuyen": "Toán học",
    "Toan": "7.10",
    "Anh": "6.50",
    "Van": "6.00",
    "MonChuyen": "5.75",
    "TongDiem": "28.23"
  },
  {
    "SBD": "250718",
    "HoTen": "Phạm Hoàng Lâm",
    "NgaySinh": "04/09/2010",
    "Chuyen": "Toán học",
    "Toan": "6.00",
    "Anh": "5.50",
    "Van": "6.75",
    "MonChuyen": "9.50",
    "TongDiem": "32.50"
  },
  {
    "SBD": "250719",
    "HoTen": "Đậu Hà Nhật Linh",
    "NgaySinh": "27/01/2010",
    "Chuyen": "Toán học",
    "Toan": "6.20",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "9.00",
    "TongDiem": "34.20"
  },
  {
    "SBD": "250720",
    "HoTen": "Đinh Ngọc Linh",
    "NgaySinh": "29/11/2010",
    "Chuyen": "Toán học",
    "Toan": "9.10",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "9.25",
    "TongDiem": "38.73"
  },
  {
    "SBD": "250721",
    "HoTen": "Ngô Thục Linh",
    "NgaySinh": "24/12/2010",
    "Chuyen": "Toán học",
    "Toan": "6.80",
    "Anh": "8.75",
    "Van": "7.75",
    "MonChuyen": "8.00",
    "TongDiem": "35.30"
  },
  {
    "SBD": "250722",
    "HoTen": "Nguyễn Phương Linh",
    "NgaySinh": "25/03/2010",
    "Chuyen": "Toán học",
    "Toan": "7.30",
    "Anh": "6.50",
    "Van": "7.75",
    "MonChuyen": "13.00",
    "TongDiem": "41.05"
  },
  {
    "SBD": "250723",
    "HoTen": "Trần Thuỳ Linh",
    "NgaySinh": "21/02/2010",
    "Chuyen": "Toán học",
    "Toan": "3.30",
    "Anh": "3.50",
    "Van": "6.00",
    "MonChuyen": "0.50",
    "TongDiem": "13.55"
  },
  {
    "SBD": "250724",
    "HoTen": "Nguyễn Bảo Long",
    "NgaySinh": "23/01/2010",
    "Chuyen": "Toán học",
    "Toan": "7.30",
    "Anh": "4.00",
    "Van": "6.50",
    "MonChuyen": "8.50",
    "TongDiem": "30.55"
  },
  {
    "SBD": "250725",
    "HoTen": "Nguyễn Hữu Long",
    "NgaySinh": "14/02/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "9.25",
    "Van": "8.50",
    "MonChuyen": "12.00",
    "TongDiem": "44.15"
  },
  {
    "SBD": "250726",
    "HoTen": "Phạm Bảo Long",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Toán học",
    "Toan": "9.30",
    "Anh": "9.25",
    "Van": "8.00",
    "MonChuyen": "15.50",
    "TongDiem": "49.80"
  },
  {
    "SBD": "250727",
    "HoTen": "Trần Đặng Hải Long",
    "NgaySinh": "05/02/2010",
    "Chuyen": "Toán học",
    "Toan": "10.00",
    "Anh": "9.25",
    "Van": "7.75",
    "MonChuyen": "16.00",
    "TongDiem": "51.00"
  },
  {
    "SBD": "250728",
    "HoTen": "Trần Đức Long",
    "NgaySinh": "20/05/2010",
    "Chuyen": "Toán học",
    "Toan": "4.60",
    "Anh": "7.00",
    "Van": "6.00",
    "MonChuyen": "5.50",
    "TongDiem": "25.85"
  },
  {
    "SBD": "250729",
    "HoTen": "Trần Khánh Ly",
    "NgaySinh": "27/06/2010",
    "Chuyen": "Toán học",
    "Toan": "6.60",
    "Anh": "7.00",
    "Van": "6.25",
    "MonChuyen": "3.00",
    "TongDiem": "24.35"
  },
  {
    "SBD": "250730",
    "HoTen": "Hoàng Nguyễn Quỳnh Mai",
    "NgaySinh": "03/03/2010",
    "Chuyen": "Toán học",
    "Toan": "7.10",
    "Anh": "7.25",
    "Van": "6.75",
    "MonChuyen": "4.50",
    "TongDiem": "27.85"
  },
  {
    "SBD": "250731",
    "HoTen": "Nguyễn Phương Mai",
    "NgaySinh": "21/07/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "6.75",
    "Van": "6.00",
    "MonChuyen": "12.50",
    "TongDiem": "39.90"
  },
  {
    "SBD": "250732",
    "HoTen": "Đặng Đức Mạnh",
    "NgaySinh": "25/05/2010",
    "Chuyen": "Toán học",
    "Toan": "4.90",
    "Anh": "6.75",
    "Van": "5.75",
    "MonChuyen": "2.50",
    "TongDiem": "21.15"
  },
  {
    "SBD": "250733",
    "HoTen": "Ngô Sỹ Mạnh",
    "NgaySinh": "23/05/2010",
    "Chuyen": "Toán học",
    "Toan": "7.30",
    "Anh": "7.75",
    "Van": "6.00",
    "MonChuyen": "13.00",
    "TongDiem": "40.55"
  },
  {
    "SBD": "250734",
    "HoTen": "Nguyễn Công Mạnh",
    "NgaySinh": "04/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "8.75",
    "Van": "6.00",
    "MonChuyen": "15.50",
    "TongDiem": "46.60"
  },
  {
    "SBD": "250735",
    "HoTen": "Nguyễn Đình Mạnh",
    "NgaySinh": "30/03/2010",
    "Chuyen": "Toán học",
    "Toan": "7.40",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "7.50",
    "TongDiem": "32.15"
  },
  {
    "SBD": "250737",
    "HoTen": "Trịnh Đức Mạnh",
    "NgaySinh": "17/02/2010",
    "Chuyen": "Toán học",
    "Toan": "7.60",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "11.75",
    "TongDiem": "38.73"
  },
  {
    "SBD": "250738",
    "HoTen": "Nguyễn Bùi Khánh Minh",
    "NgaySinh": "18/06/2010",
    "Chuyen": "Toán học",
    "Toan": "10.00",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "13.75",
    "TongDiem": "46.13"
  },
  {
    "SBD": "250739",
    "HoTen": "Nguyễn Hoàng Minh",
    "NgaySinh": "12/08/2010",
    "Chuyen": "Toán học",
    "Toan": "10.00",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "17.50",
    "TongDiem": "52.75"
  },
  {
    "SBD": "250741",
    "HoTen": "Nguyễn Tiến Minh",
    "NgaySinh": "10/04/2010",
    "Chuyen": "Toán học",
    "Toan": "4.70",
    "Anh": "5.25",
    "Van": "7.50",
    "MonChuyen": "2.00",
    "TongDiem": "20.45"
  },
  {
    "SBD": "250743",
    "HoTen": "Phạm Bình Minh",
    "NgaySinh": "24/02/2010",
    "Chuyen": "Toán học",
    "Toan": "9.40",
    "Anh": "9.50",
    "Van": "7.75",
    "MonChuyen": "16.00",
    "TongDiem": "50.65"
  },
  {
    "SBD": "250744",
    "HoTen": "Phan Nhật Minh",
    "NgaySinh": "21/11/2010",
    "Chuyen": "Toán học",
    "Toan": "9.40",
    "Anh": "9.00",
    "Van": "7.50",
    "MonChuyen": "13.75",
    "TongDiem": "46.53"
  },
  {
    "SBD": "250745",
    "HoTen": "Trịnh Ngọc Minh",
    "NgaySinh": "15/05/2010",
    "Chuyen": "Toán học",
    "Toan": "10.00",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "13.25",
    "TongDiem": "45.13"
  },
  {
    "SBD": "250747",
    "HoTen": "Lương Hoàng Nam",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Toán học",
    "Toan": "7.10",
    "Anh": "3.50",
    "Van": "7.00",
    "MonChuyen": "11.00",
    "TongDiem": "34.10"
  },
  {
    "SBD": "250748",
    "HoTen": "Nguyễn Quốc Nam",
    "NgaySinh": "24/04/2010",
    "Chuyen": "Toán học",
    "Toan": "5.90",
    "Anh": "4.75",
    "Van": "6.50",
    "MonChuyen": "7.00",
    "TongDiem": "27.65"
  },
  {
    "SBD": "250749",
    "HoTen": "Nguyễn Lưu Trúc Ngân",
    "NgaySinh": "06/02/2010",
    "Chuyen": "Toán học",
    "Toan": "7.40",
    "Anh": "7.25",
    "Van": "7.25",
    "MonChuyen": "12.00",
    "TongDiem": "39.90"
  },
  {
    "SBD": "250750",
    "HoTen": "Ngô Thị Bảo Ngọc",
    "NgaySinh": "04/02/2010",
    "Chuyen": "Toán học",
    "Toan": "7.50",
    "Anh": "8.75",
    "Van": "8.50",
    "MonChuyen": "8.25",
    "TongDiem": "37.13"
  },
  {
    "SBD": "250751",
    "HoTen": "Nguyễn Thị Bảo Ngọc",
    "NgaySinh": "30/04/2010",
    "Chuyen": "Toán học",
    "Toan": "9.30",
    "Anh": "6.75",
    "Van": "7.75",
    "MonChuyen": "8.25",
    "TongDiem": "36.18"
  },
  {
    "SBD": "250752",
    "HoTen": "Nguyễn Thị Bảo Ngọc",
    "NgaySinh": "09/04/2010",
    "Chuyen": "Toán học",
    "Toan": "6.20",
    "Anh": "6.50",
    "Van": "7.50",
    "MonChuyen": "9.50",
    "TongDiem": "34.45"
  },
  {
    "SBD": "250753",
    "HoTen": "Lê Trí Nguyên",
    "NgaySinh": "26/07/2010",
    "Chuyen": "Toán học",
    "Toan": "5.40",
    "Anh": "7.00",
    "Van": "6.50",
    "MonChuyen": "5.50",
    "TongDiem": "27.15"
  },
  {
    "SBD": "250754",
    "HoTen": "Nguyễn Khôi Nguyên",
    "NgaySinh": "20/06/2010",
    "Chuyen": "Toán học",
    "Toan": "7.80",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "13.50",
    "TongDiem": "45.05"
  },
  {
    "SBD": "250755",
    "HoTen": "Nguyễn Nguyên",
    "NgaySinh": "17/01/2010",
    "Chuyen": "Toán học",
    "Toan": "9.50",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "16.50",
    "TongDiem": "51.00"
  },
  {
    "SBD": "250756",
    "HoTen": "Nguyễn Thúc Bảo Nguyên",
    "NgaySinh": "05/01/2010",
    "Chuyen": "Toán học",
    "Toan": "7.40",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "9.25",
    "TongDiem": "37.28"
  },
  {
    "SBD": "250757",
    "HoTen": "Phan Nguyễn Khôi Nguyên",
    "NgaySinh": "24/02/2010",
    "Chuyen": "Toán học",
    "Toan": "6.70",
    "Anh": "5.50",
    "Van": "6.75",
    "MonChuyen": "5.00",
    "TongDiem": "26.45"
  },
  {
    "SBD": "250758",
    "HoTen": "Trần Văn Đức Nguyên",
    "NgaySinh": "27/11/2010",
    "Chuyen": "Toán học",
    "Toan": "7.60",
    "Anh": "5.25",
    "Van": "7.50",
    "MonChuyen": "7.50",
    "TongDiem": "31.60"
  },
  {
    "SBD": "250759",
    "HoTen": "Hoang Đình Anh Nhân",
    "NgaySinh": "11/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.10",
    "Anh": "6.25",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "38.35"
  },
  {
    "SBD": "250760",
    "HoTen": "Bùi Thị Minh Nhi",
    "NgaySinh": "15/10/2010",
    "Chuyen": "Toán học",
    "Toan": "6.60",
    "Anh": "7.25",
    "Van": "7.50",
    "MonChuyen": "3.50",
    "TongDiem": "26.60"
  },
  {
    "SBD": "250761",
    "HoTen": "Hồ Ngọc Bảo Nhi",
    "NgaySinh": "03/03/2010",
    "Chuyen": "Toán học",
    "Toan": "5.60",
    "Anh": "6.00",
    "Van": "8.00",
    "MonChuyen": "0.50",
    "TongDiem": "20.35"
  },
  {
    "SBD": "250762",
    "HoTen": "Hồ Võ Bảo Nhi",
    "NgaySinh": "18/06/2010",
    "Chuyen": "Toán học",
    "Toan": "8.20",
    "Anh": "7.50",
    "Van": "8.50",
    "MonChuyen": "8.50",
    "TongDiem": "36.95"
  },
  {
    "SBD": "250763",
    "HoTen": "Hoàng Võ Yến Nhi",
    "NgaySinh": "13/11/2010",
    "Chuyen": "Toán học",
    "Toan": "6.30",
    "Anh": "9.75",
    "Van": "7.25",
    "MonChuyen": "7.50",
    "TongDiem": "34.55"
  },
  {
    "SBD": "250764",
    "HoTen": "Lê Trần Uyển Nhi",
    "NgaySinh": "14/02/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "7.00",
    "Van": "6.00",
    "MonChuyen": "10.50",
    "TongDiem": "37.35"
  },
  {
    "SBD": "250765",
    "HoTen": "Trần Lê An Nhi",
    "NgaySinh": "08/02/2010",
    "Chuyen": "Toán học",
    "Toan": "8.90",
    "Anh": "8.25",
    "Van": "7.25",
    "MonChuyen": "11.00",
    "TongDiem": "40.90"
  },
  {
    "SBD": "250766",
    "HoTen": "Trần Thị Vân Nhi",
    "NgaySinh": "29/10/2010",
    "Chuyen": "Toán học",
    "Toan": "6.20",
    "Anh": "5.00",
    "Van": "7.00",
    "MonChuyen": "2.00",
    "TongDiem": "21.20"
  },
  {
    "SBD": "250767",
    "HoTen": "Nguyễn Hữu Hồ Phát",
    "NgaySinh": "30/07/2010",
    "Chuyen": "Toán học",
    "Toan": "5.30",
    "Anh": "6.00",
    "Van": "6.75",
    "MonChuyen": "4.50",
    "TongDiem": "24.80"
  },
  {
    "SBD": "250768",
    "HoTen": "Nguyễn Huy Trường Phát",
    "NgaySinh": "02/03/2010",
    "Chuyen": "Toán học",
    "Toan": "7.60",
    "Anh": "6.00",
    "Van": "7.50",
    "MonChuyen": "12.00",
    "TongDiem": "39.10"
  },
  {
    "SBD": "250770",
    "HoTen": "Cao Thanh Phong",
    "NgaySinh": "18/06/2010",
    "Chuyen": "Toán học",
    "Toan": "8.30",
    "Anh": "7.00",
    "Van": "7.00",
    "MonChuyen": "13.00",
    "TongDiem": "41.80"
  },
  {
    "SBD": "250771",
    "HoTen": "Trần Đình Phong",
    "NgaySinh": "29/07/2010",
    "Chuyen": "Toán học",
    "Toan": "5.60",
    "Anh": "5.00",
    "Van": "6.50",
    "MonChuyen": "2.00",
    "TongDiem": "20.10"
  },
  {
    "SBD": "250772",
    "HoTen": "Trần Lê Hùng Phong",
    "NgaySinh": "09/11/2010",
    "Chuyen": "Toán học",
    "Toan": "6.70",
    "Anh": "4.00",
    "Van": "5.50",
    "MonChuyen": "1.25",
    "TongDiem": "18.08"
  },
  {
    "SBD": "250773",
    "HoTen": "Hoàng Trường Phúc",
    "NgaySinh": "25/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.30",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "11.50",
    "TongDiem": "40.80"
  },
  {
    "SBD": "250774",
    "HoTen": "Nguyễn Hữu Phúc",
    "NgaySinh": "09/09/2010",
    "Chuyen": "Toán học",
    "Toan": "5.30",
    "Anh": "5.75",
    "Van": "6.50",
    "MonChuyen": "11.00",
    "TongDiem": "34.05"
  },
  {
    "SBD": "250775",
    "HoTen": "Phạm Hồng Phúc",
    "NgaySinh": "17/09/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "7.75",
    "Van": "6.50",
    "MonChuyen": "5.75",
    "TongDiem": "30.88"
  },
  {
    "SBD": "250776",
    "HoTen": "Phan Hồng Phúc",
    "NgaySinh": "05/05/2010",
    "Chuyen": "Toán học",
    "Toan": "8.70",
    "Anh": "5.25",
    "Van": "5.50",
    "MonChuyen": "8.00",
    "TongDiem": "31.45"
  },
  {
    "SBD": "250777",
    "HoTen": "Vương Đình Phúc",
    "NgaySinh": "19/07/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "8.00",
    "Van": "6.75",
    "MonChuyen": "10.00",
    "TongDiem": "38.35"
  },
  {
    "SBD": "250778",
    "HoTen": "Nguyễn Hữu Phước",
    "NgaySinh": "06/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.30",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "11.00",
    "TongDiem": "40.80"
  },
  {
    "SBD": "250779",
    "HoTen": "Phạm Viết Phước",
    "NgaySinh": "24/04/2010",
    "Chuyen": "Toán học",
    "Toan": "8.70",
    "Anh": "5.50",
    "Van": "7.50",
    "MonChuyen": "8.50",
    "TongDiem": "34.45"
  },
  {
    "SBD": "250780",
    "HoTen": "Lê Minh Phương",
    "NgaySinh": "30/10/2010",
    "Chuyen": "Toán học",
    "Toan": "7.10",
    "Anh": "7.25",
    "Van": "8.50",
    "MonChuyen": "6.00",
    "TongDiem": "31.85"
  },
  {
    "SBD": "250782",
    "HoTen": "Lê Đình Hoàng Quân",
    "NgaySinh": "21/05/2010",
    "Chuyen": "Toán học",
    "Toan": "8.20",
    "Anh": "9.00",
    "Van": "6.50",
    "MonChuyen": "13.00",
    "TongDiem": "43.20"
  },
  {
    "SBD": "250783",
    "HoTen": "Cao Minh Quân",
    "NgaySinh": "06/01/2010",
    "Chuyen": "Toán học",
    "Toan": "7.20",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "11.50",
    "TongDiem": "40.70"
  },
  {
    "SBD": "250784",
    "HoTen": "Hoàng Đình Minh Quân",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.40",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "8.50",
    "TongDiem": "37.40"
  },
  {
    "SBD": "250785",
    "HoTen": "Nguyễn Cảnh Quân",
    "NgaySinh": "08/04/2010",
    "Chuyen": "Toán học",
    "Toan": "6.20",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "7.50",
    "TongDiem": "32.45"
  },
  {
    "SBD": "250786",
    "HoTen": "Nguyễn Đình Bảo Quân",
    "NgaySinh": "13/08/2010",
    "Chuyen": "Toán học",
    "Toan": "7.40",
    "Anh": "6.00",
    "Van": "7.75",
    "MonChuyen": "9.50",
    "TongDiem": "35.40"
  },
  {
    "SBD": "250787",
    "HoTen": "Nguyễn Hoàng Quân",
    "NgaySinh": "16/02/2101",
    "Chuyen": "Toán học",
    "Toan": "7.50",
    "Anh": "8.25",
    "Van": "8.25",
    "MonChuyen": "12.50",
    "TongDiem": "42.75"
  },
  {
    "SBD": "250788",
    "HoTen": "Nguyễn Như Quân",
    "NgaySinh": "02/03/2010",
    "Chuyen": "Toán học",
    "Toan": "8.80",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "13.50",
    "TongDiem": "45.05"
  },
  {
    "SBD": "250789",
    "HoTen": "Phan Anh Quân",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Toán học",
    "Toan": "6.40",
    "Anh": "4.75",
    "Van": "7.25",
    "MonChuyen": "7.25",
    "TongDiem": "29.28"
  },
  {
    "SBD": "250791",
    "HoTen": "Trần Minh Quân",
    "NgaySinh": "20/03/2010",
    "Chuyen": "Toán học",
    "Toan": "5.10",
    "Anh": "7.00",
    "Van": "6.75",
    "MonChuyen": "3.50",
    "TongDiem": "24.10"
  },
  {
    "SBD": "250792",
    "HoTen": "Hà Nhật Quang",
    "NgaySinh": "11/01/2010",
    "Chuyen": "Toán học",
    "Toan": "9.50",
    "Anh": "8.75",
    "Van": "9.00",
    "MonChuyen": "16.50",
    "TongDiem": "52.00"
  },
  {
    "SBD": "250793",
    "HoTen": "Trần Văn Quang",
    "NgaySinh": "07/01/2010",
    "Chuyen": "Toán học",
    "Toan": "7.60",
    "Anh": "7.75",
    "Van": "6.75",
    "MonChuyen": "10.50",
    "TongDiem": "37.85"
  },
  {
    "SBD": "250794",
    "HoTen": "Trần Thục Quyên",
    "NgaySinh": "23/01/2010",
    "Chuyen": "Toán học",
    "Toan": "6.30",
    "Anh": "8.75",
    "Van": "7.00",
    "MonChuyen": "8.00",
    "TongDiem": "34.05"
  },
  {
    "SBD": "250795",
    "HoTen": "Nguyễn Quỳnh Sang",
    "NgaySinh": "05/06/2010",
    "Chuyen": "Toán học",
    "Toan": "8.20",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "12.50",
    "TongDiem": "42.20"
  },
  {
    "SBD": "250796",
    "HoTen": "Đậu Công Sáng",
    "NgaySinh": "26/01/2010",
    "Chuyen": "Toán học",
    "Toan": "7.50",
    "Anh": "5.50",
    "Van": "6.00",
    "MonChuyen": "12.50",
    "TongDiem": "37.75"
  },
  {
    "SBD": "250797",
    "HoTen": "Hà Thái Sơn",
    "NgaySinh": "15/05/2010",
    "Chuyen": "Toán học",
    "Toan": "5.70",
    "Anh": "8.50",
    "Van": "6.50",
    "MonChuyen": "3.00",
    "TongDiem": "25.20"
  },
  {
    "SBD": "250798",
    "HoTen": "Hoàng Thái Sơn",
    "NgaySinh": "10/04/2010",
    "Chuyen": "Toán học",
    "Toan": "7.90",
    "Anh": "8.00",
    "Van": "6.00",
    "MonChuyen": "14.00",
    "TongDiem": "42.90"
  },
  {
    "SBD": "250799",
    "HoTen": "Nguyễn Đăng Sơn",
    "NgaySinh": "22/08/2010",
    "Chuyen": "Toán học",
    "Toan": "7.70",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "6.00",
    "TongDiem": "29.95"
  },
  {
    "SBD": "250800",
    "HoTen": "Trần Thanh Sơn",
    "NgaySinh": "18/04/2010",
    "Chuyen": "Toán học",
    "Toan": "5.50",
    "Anh": "6.00",
    "Van": "5.50",
    "MonChuyen": "5.00",
    "TongDiem": "24.50"
  },
  {
    "SBD": "250801",
    "HoTen": "Nguyễn Thị Băng Tâm",
    "NgaySinh": "20/10/2010",
    "Chuyen": "Toán học",
    "Toan": "9.10",
    "Anh": "9.25",
    "Van": "6.25",
    "MonChuyen": "15.50",
    "TongDiem": "47.85"
  },
  {
    "SBD": "250802",
    "HoTen": "Trần Tâm",
    "NgaySinh": "10/06/2010",
    "Chuyen": "Toán học",
    "Toan": "8.80",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "7.75",
    "TongDiem": "36.18"
  },
  {
    "SBD": "250803",
    "HoTen": "Phạm Nhật Tân",
    "NgaySinh": "02/02/2010",
    "Chuyen": "Toán học",
    "Toan": "6.40",
    "Anh": "5.50",
    "Van": "5.75",
    "MonChuyen": "3.75",
    "TongDiem": "23.28"
  },
  {
    "SBD": "250804",
    "HoTen": "Nguyễn Minh Thắng",
    "NgaySinh": "11/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "13.50",
    "TongDiem": "43.35"
  },
  {
    "SBD": "250805",
    "HoTen": "Phạm Cao Thắng",
    "NgaySinh": "18/02/2010",
    "Chuyen": "Toán học",
    "Toan": "9.60",
    "Anh": "10.00",
    "Van": "7.50",
    "MonChuyen": "12.75",
    "TongDiem": "46.23"
  },
  {
    "SBD": "250806",
    "HoTen": "Trần Thúy Thanh",
    "NgaySinh": "01/10/2010",
    "Chuyen": "Toán học",
    "Toan": "9.30",
    "Anh": "8.50",
    "Van": "7.75",
    "MonChuyen": "13.00",
    "TongDiem": "45.05"
  },
  {
    "SBD": "250807",
    "HoTen": "Võ Quang Thanh",
    "NgaySinh": "04/03/2010",
    "Chuyen": "Toán học",
    "Toan": "8.90",
    "Anh": "7.00",
    "Van": "7.50",
    "MonChuyen": "13.00",
    "TongDiem": "42.90"
  },
  {
    "SBD": "250808",
    "HoTen": "Hoàng Thành",
    "NgaySinh": "14/06/2010",
    "Chuyen": "Toán học",
    "Toan": "9.10",
    "Anh": "8.50",
    "Van": "7.75",
    "MonChuyen": "12.75",
    "TongDiem": "44.48"
  },
  {
    "SBD": "250809",
    "HoTen": "Nguyễn Tiến Thành",
    "NgaySinh": "07/12/2010",
    "Chuyen": "Toán học",
    "Toan": "6.60",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "11.00",
    "TongDiem": "39.10"
  },
  {
    "SBD": "250810",
    "HoTen": "Nguyễn Văn Thành",
    "NgaySinh": "10/11/2010",
    "Chuyen": "Toán học",
    "Toan": "6.90",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "8.50",
    "TongDiem": "35.65"
  },
  {
    "SBD": "250811",
    "HoTen": "Hồ Hữu Thế",
    "NgaySinh": "05/06/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "7.75",
    "Van": "8.75",
    "MonChuyen": "10.25",
    "TongDiem": "39.88"
  },
  {
    "SBD": "250812",
    "HoTen": "Lưu Ngọc Thiện",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.80",
    "Anh": "7.00",
    "Van": "6.25",
    "MonChuyen": "8.00",
    "TongDiem": "34.05"
  },
  {
    "SBD": "250813",
    "HoTen": "Phạm Thị An Thu",
    "NgaySinh": "17/01/2010",
    "Chuyen": "Toán học",
    "Toan": "5.10",
    "Anh": "4.75",
    "Van": "6.50",
    "MonChuyen": "0.50",
    "TongDiem": "17.10"
  },
  {
    "SBD": "250814",
    "HoTen": "Nguyễn Thị Anh Thư",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Toán học",
    "Toan": "7.40",
    "Anh": "5.25",
    "Van": "7.75",
    "MonChuyen": "11.50",
    "TongDiem": "37.65"
  },
  {
    "SBD": "250815",
    "HoTen": "Lê Kim Toàn",
    "NgaySinh": "11/07/2010",
    "Chuyen": "Toán học",
    "Toan": "4.70",
    "Anh": "6.00",
    "Van": "7.50",
    "MonChuyen": "2.00",
    "TongDiem": "21.20"
  },
  {
    "SBD": "250816",
    "HoTen": "Đặng Thị Huyền Trang",
    "NgaySinh": "19/03/2010",
    "Chuyen": "Toán học",
    "Toan": "9.30",
    "Anh": "9.00",
    "Van": "8.50",
    "MonChuyen": "13.00",
    "TongDiem": "46.30"
  },
  {
    "SBD": "250817",
    "HoTen": "Đào Thị Huyền Trang",
    "NgaySinh": "25/05/2010",
    "Chuyen": "Toán học",
    "Toan": "5.60",
    "Anh": "6.00",
    "Van": "7.75",
    "MonChuyen": "4.75",
    "TongDiem": "26.48"
  },
  {
    "SBD": "250818",
    "HoTen": "Nguyễn Thị Huyền Trang",
    "NgaySinh": "18/10/2010",
    "Chuyen": "Toán học",
    "Toan": "6.90",
    "Anh": "5.75",
    "Van": "6.25",
    "MonChuyen": "4.50",
    "TongDiem": "25.65"
  },
  {
    "SBD": "250820",
    "HoTen": "Trần Bảo Trang",
    "NgaySinh": "24/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "15.50",
    "TongDiem": "47.50"
  },
  {
    "SBD": "250821",
    "HoTen": "Nguyễn Minh Trí",
    "NgaySinh": "13/07/2010",
    "Chuyen": "Toán học",
    "Toan": "8.50",
    "Anh": "7.50",
    "Van": "6.25",
    "MonChuyen": "10.50",
    "TongDiem": "38.00"
  },
  {
    "SBD": "250822",
    "HoTen": "Đậu Thành Trung",
    "NgaySinh": "23/09/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "13.00",
    "TongDiem": "43.60"
  },
  {
    "SBD": "250825",
    "HoTen": "Bùi Đức Trường",
    "NgaySinh": "14/05/2010",
    "Chuyen": "Toán học",
    "Toan": "9.60",
    "Anh": "7.75",
    "Van": "7.00",
    "MonChuyen": "12.50",
    "TongDiem": "43.10"
  },
  {
    "SBD": "250826",
    "HoTen": "Hồ Mạnh Trường",
    "NgaySinh": "18/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.90",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "16.50",
    "TongDiem": "48.90"
  },
  {
    "SBD": "250827",
    "HoTen": "Nguyễn Tuấn Tú",
    "NgaySinh": "07/01/2010",
    "Chuyen": "Toán học",
    "Toan": "5.40",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "8.00",
    "TongDiem": "30.90"
  },
  {
    "SBD": "250828",
    "HoTen": "Nguyễn Minh Tuấn",
    "NgaySinh": "29/09/2010",
    "Chuyen": "Toán học",
    "Toan": "8.00",
    "Anh": "6.75",
    "Van": "5.00",
    "MonChuyen": "7.50",
    "TongDiem": "31.00"
  },
  {
    "SBD": "250829",
    "HoTen": "Nguyễn Minh Tuấn",
    "NgaySinh": "04/09/2010",
    "Chuyen": "Toán học",
    "Toan": "7.80",
    "Anh": "8.25",
    "Van": "6.25",
    "MonChuyen": "6.50",
    "TongDiem": "32.05"
  },
  {
    "SBD": "250830",
    "HoTen": "Phạm Anh Tuấn",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Toán học",
    "Toan": "8.70",
    "Anh": "6.75",
    "Van": "6.75",
    "MonChuyen": "11.00",
    "TongDiem": "38.70"
  },
  {
    "SBD": "250832",
    "HoTen": "Nguyễn Minh Tuệ",
    "NgaySinh": "17/05/2010",
    "Chuyen": "Toán học",
    "Toan": "7.80",
    "Anh": "7.00",
    "Van": "6.75",
    "MonChuyen": "10.00",
    "TongDiem": "36.55"
  },
  {
    "SBD": "250833",
    "HoTen": "Trịnh Văn Tài Tuệ",
    "NgaySinh": "11/04/2010",
    "Chuyen": "Toán học",
    "Toan": "6.30",
    "Anh": "6.00",
    "Van": "6.25",
    "MonChuyen": "4.00",
    "TongDiem": "24.55"
  },
  {
    "SBD": "250834",
    "HoTen": "Nguyễn Huy Tùng",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Toán học",
    "Toan": "6.20",
    "Anh": "5.50",
    "Van": "5.25",
    "MonChuyen": "3.00",
    "TongDiem": "21.45"
  },
  {
    "SBD": "250835",
    "HoTen": "Phan Hữu Tùng",
    "NgaySinh": "17/04/2010",
    "Chuyen": "Toán học",
    "Toan": "9.30",
    "Anh": "9.75",
    "Van": "8.50",
    "MonChuyen": "13.50",
    "TongDiem": "47.80"
  },
  {
    "SBD": "250836",
    "HoTen": "Võ Hoàng Việt",
    "NgaySinh": "23/06/2010",
    "Chuyen": "Toán học",
    "Toan": "4.40",
    "Anh": "6.50",
    "Van": "6.00",
    "MonChuyen": "6.00",
    "TongDiem": "25.90"
  },
  {
    "SBD": "250837",
    "HoTen": "Trần Đức Vinh",
    "NgaySinh": "09/05/2010",
    "Chuyen": "Toán học",
    "Toan": "6.60",
    "Anh": "7.50",
    "Van": "6.00",
    "MonChuyen": "5.25",
    "TongDiem": "27.98"
  },
  {
    "SBD": "250839",
    "HoTen": "Nguyễn Hoàng Vũ",
    "NgaySinh": "17/03/2010",
    "Chuyen": "Toán học",
    "Toan": "7.50",
    "Anh": "6.50",
    "Van": "5.25",
    "MonChuyen": "8.25",
    "TongDiem": "31.63"
  },
  {
    "SBD": "250840",
    "HoTen": "Nguyễn Thúc Gia Vũ",
    "NgaySinh": "12/10/2010",
    "Chuyen": "Toán học",
    "Toan": "8.80",
    "Anh": "8.25",
    "Van": "0.0",
    "MonChuyen": "0.0",
    "TongDiem": "0.0"
  },
  {
    "SBD": "250841",
    "HoTen": "Lê Tường Vy",
    "NgaySinh": "24/11/2010",
    "Chuyen": "Toán học",
    "Toan": "9.60",
    "Anh": "8.00",
    "Van": "6.25",
    "MonChuyen": "11.75",
    "TongDiem": "41.48"
  },
  {
    "SBD": "250842",
    "HoTen": "Nguyễn Hà Vy",
    "NgaySinh": "03/10/2010",
    "Chuyen": "Toán học",
    "Toan": "9.10",
    "Anh": "9.50",
    "Van": "7.25",
    "MonChuyen": "13.75",
    "TongDiem": "46.48"
  },
  {
    "SBD": "250843",
    "HoTen": "Nguyễn Khánh Vy",
    "NgaySinh": "10/03/2010",
    "Chuyen": "Toán học",
    "Toan": "7.20",
    "Anh": "9.75",
    "Van": "7.75",
    "MonChuyen": "14.50",
    "TongDiem": "46.45"
  },
  {
    "SBD": "250844",
    "HoTen": "Phạm Thị Hà Vy",
    "NgaySinh": "18/03/2010",
    "Chuyen": "Toán học",
    "Toan": "6.10",
    "Anh": "6.00",
    "Van": "5.50",
    "MonChuyen": "1.00",
    "TongDiem": "19.10"
  },
  {
    "SBD": "250845",
    "HoTen": "Võ Phi Yến",
    "NgaySinh": "28/10/2010",
    "Chuyen": "Toán học",
    "Toan": "8.60",
    "Anh": "8.00",
    "Van": "6.50",
    "MonChuyen": "10.50",
    "TongDiem": "38.85"
  },
  {
    "SBD": "250846",
    "HoTen": "Nguyễn Viết Hùng Anh",
    "NgaySinh": "01/09/2010",
    "Chuyen": "Tin học",
    "Toan": "6.40",
    "Anh": "5.75",
    "Van": "5.50",
    "MonChuyen": "6.75",
    "TongDiem": "27.78"
  },
  {
    "SBD": "250847",
    "HoTen": "Trần Hoàng Bách",
    "NgaySinh": "23/05/2010",
    "Chuyen": "Tin học",
    "Toan": "6.80",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "8.00",
    "TongDiem": "34.80"
  },
  {
    "SBD": "250848",
    "HoTen": "Nguyễn Trọng Bản",
    "NgaySinh": "04/01/2010",
    "Chuyen": "Tin học",
    "Toan": "3.60",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "5.00",
    "TongDiem": "23.60"
  },
  {
    "SBD": "250849",
    "HoTen": "Chu Gia Bảo",
    "NgaySinh": "10/08/2010",
    "Chuyen": "Tin học",
    "Toan": "5.80",
    "Anh": "7.50",
    "Van": "6.25",
    "MonChuyen": "2.00",
    "TongDiem": "22.55"
  },
  {
    "SBD": "250851",
    "HoTen": "Nguyễn Gia Bảo",
    "NgaySinh": "19/02/2010",
    "Chuyen": "Tin học",
    "Toan": "5.40",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "5.00",
    "TongDiem": "26.40"
  },
  {
    "SBD": "250852",
    "HoTen": "Ngô Thành Đạt",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Tin học",
    "Toan": "7.20",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "4.00",
    "TongDiem": "25.95"
  },
  {
    "SBD": "250853",
    "HoTen": "Tạ Đăng Đạt",
    "NgaySinh": "08/05/2010",
    "Chuyen": "Tin học",
    "Toan": "5.40",
    "Anh": "4.25",
    "Van": "6.50",
    "MonChuyen": "2.00",
    "TongDiem": "19.15"
  },
  {
    "SBD": "250854",
    "HoTen": "Hồ Văn Tiến Đức",
    "NgaySinh": "11/10/2010",
    "Chuyen": "Tin học",
    "Toan": "5.40",
    "Anh": "4.50",
    "Van": "6.00",
    "MonChuyen": "3.25",
    "TongDiem": "20.78"
  },
  {
    "SBD": "250855",
    "HoTen": "Hoàng Lê Minh Đức",
    "NgaySinh": "11/11/2010",
    "Chuyen": "Tin học",
    "Toan": "5.80",
    "Anh": "6.00",
    "Van": "6.75",
    "MonChuyen": "2.25",
    "TongDiem": "21.93"
  },
  {
    "SBD": "250856",
    "HoTen": "Hồ Trọng Minh Dũng",
    "NgaySinh": "24/02/2010",
    "Chuyen": "Tin học",
    "Toan": "7.10",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "6.00",
    "TongDiem": "28.85"
  },
  {
    "SBD": "250858",
    "HoTen": "Nguyễn Đức Duy",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Tin học",
    "Toan": "5.90",
    "Anh": "4.50",
    "Van": "7.00",
    "MonChuyen": "5.00",
    "TongDiem": "24.90"
  },
  {
    "SBD": "250859",
    "HoTen": "Nguyễn Đức Hiếu",
    "NgaySinh": "13/05/2010",
    "Chuyen": "Tin học",
    "Toan": "8.90",
    "Anh": "8.25",
    "Van": "6.75",
    "MonChuyen": "7.50",
    "TongDiem": "35.15"
  },
  {
    "SBD": "250860",
    "HoTen": "Phan Trọng Hiếu",
    "NgaySinh": "17/09/2010",
    "Chuyen": "Tin học",
    "Toan": "8.60",
    "Anh": "8.75",
    "Van": "6.00",
    "MonChuyen": "10.00",
    "TongDiem": "38.35"
  },
  {
    "SBD": "250862",
    "HoTen": "Lê Quang Hưng",
    "NgaySinh": "19/02/2010",
    "Chuyen": "Tin học",
    "Toan": "5.90",
    "Anh": "6.75",
    "Van": "6.50",
    "MonChuyen": "5.00",
    "TongDiem": "26.65"
  },
  {
    "SBD": "250863",
    "HoTen": "Phạm Đức Huy",
    "NgaySinh": "28/10/2010",
    "Chuyen": "Tin học",
    "Toan": "6.90",
    "Anh": "8.00",
    "Van": "6.25",
    "MonChuyen": "3.00",
    "TongDiem": "25.65"
  },
  {
    "SBD": "250864",
    "HoTen": "Nguyễn Quốc Khánh",
    "NgaySinh": "24/10/2010",
    "Chuyen": "Tin học",
    "Toan": "6.60",
    "Anh": "8.00",
    "Van": "5.75",
    "MonChuyen": "6.50",
    "TongDiem": "30.10"
  },
  {
    "SBD": "250865",
    "HoTen": "Hồ Minh Khôi",
    "NgaySinh": "02/06/2010",
    "Chuyen": "Tin học",
    "Toan": "7.30",
    "Anh": "5.25",
    "Van": "6.50",
    "MonChuyen": "4.50",
    "TongDiem": "25.80"
  },
  {
    "SBD": "250866",
    "HoTen": "Nguyễn Hàm Trung Kiên",
    "NgaySinh": "09/10/2010",
    "Chuyen": "Tin học",
    "Toan": "5.00",
    "Anh": "5.25",
    "Van": "6.25",
    "MonChuyen": "3.50",
    "TongDiem": "21.75"
  },
  {
    "SBD": "250868",
    "HoTen": "Hoàng Hà Linh",
    "NgaySinh": "23/01/2010",
    "Chuyen": "Tin học",
    "Toan": "5.50",
    "Anh": "6.00",
    "Van": "6.75",
    "MonChuyen": "5.00",
    "TongDiem": "25.75"
  },
  {
    "SBD": "250869",
    "HoTen": "Hoàng Thị Diệu Linh",
    "NgaySinh": "12/10/2010",
    "Chuyen": "Tin học",
    "Toan": "6.00",
    "Anh": "4.50",
    "Van": "7.00",
    "MonChuyen": "2.00",
    "TongDiem": "20.50"
  },
  {
    "SBD": "250870",
    "HoTen": "Phùng Đậu Ngọc Long",
    "NgaySinh": "25/12/2010",
    "Chuyen": "Tin học",
    "Toan": "5.40",
    "Anh": "7.25",
    "Van": "5.75",
    "MonChuyen": "2.00",
    "TongDiem": "21.40"
  },
  {
    "SBD": "250872",
    "HoTen": "Phan Tiến Mạnh",
    "NgaySinh": "24/08/2010",
    "Chuyen": "Tin học",
    "Toan": "5.80",
    "Anh": "5.50",
    "Van": "7.00",
    "MonChuyen": "6.50",
    "TongDiem": "28.05"
  },
  {
    "SBD": "250873",
    "HoTen": "Bùi Phan Bình Minh",
    "NgaySinh": "18/09/2010",
    "Chuyen": "Tin học",
    "Toan": "5.50",
    "Anh": "7.25",
    "Van": "5.00",
    "MonChuyen": "5.00",
    "TongDiem": "25.25"
  },
  {
    "SBD": "250874",
    "HoTen": "Chu Duy Quang Minh",
    "NgaySinh": "02/02/2010",
    "Chuyen": "Tin học",
    "Toan": "8.20",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "8.50",
    "TongDiem": "33.70"
  },
  {
    "SBD": "250875",
    "HoTen": "Ông Vĩnh Bảo Minh",
    "NgaySinh": "16/08/2010",
    "Chuyen": "Tin học",
    "Toan": "3.00",
    "Anh": "5.75",
    "Van": "5.75",
    "MonChuyen": "1.50",
    "TongDiem": "16.75"
  },
  {
    "SBD": "250877",
    "HoTen": "Lê Thanh Nam",
    "NgaySinh": "14/09/2010",
    "Chuyen": "Tin học",
    "Toan": "8.40",
    "Anh": "8.25",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "40.65"
  },
  {
    "SBD": "250878",
    "HoTen": "Lương Đình Tuấn Nghĩa",
    "NgaySinh": "06/08/2010",
    "Chuyen": "Tin học",
    "Toan": "8.30",
    "Anh": "7.50",
    "Van": "6.00",
    "MonChuyen": "9.50",
    "TongDiem": "36.05"
  },
  {
    "SBD": "250879",
    "HoTen": "Trương Nguyễn Khánh Ngọc",
    "NgaySinh": "29/04/2010",
    "Chuyen": "Tin học",
    "Toan": "5.10",
    "Anh": "6.75",
    "Van": "6.00",
    "MonChuyen": "0.75",
    "TongDiem": "18.98"
  },
  {
    "SBD": "250880",
    "HoTen": "Nguyễn Hoàng Nguyên",
    "NgaySinh": "23/04/2010",
    "Chuyen": "Tin học",
    "Toan": "8.30",
    "Anh": "7.25",
    "Van": "6.50",
    "MonChuyen": "15.00",
    "TongDiem": "44.55"
  },
  {
    "SBD": "250881",
    "HoTen": "Cao Thành Phát",
    "NgaySinh": "24/05/2010",
    "Chuyen": "Tin học",
    "Toan": "7.30",
    "Anh": "8.25",
    "Van": "5.75",
    "MonChuyen": "10.50",
    "TongDiem": "37.05"
  },
  {
    "SBD": "250882",
    "HoTen": "Nguyễn Hồ Quân",
    "NgaySinh": "26/01/2010",
    "Chuyen": "Tin học",
    "Toan": "6.00",
    "Anh": "4.75",
    "Van": "6.50",
    "MonChuyen": "6.00",
    "TongDiem": "26.25"
  },
  {
    "SBD": "250884",
    "HoTen": "Nguyễn Duy Quyền",
    "NgaySinh": "02/12/2010",
    "Chuyen": "Tin học",
    "Toan": "4.80",
    "Anh": "7.00",
    "Van": "6.00",
    "MonChuyen": "4.75",
    "TongDiem": "24.93"
  },
  {
    "SBD": "250885",
    "HoTen": "Nguyễn Hoàng Sơn",
    "NgaySinh": "27/08/2010",
    "Chuyen": "Tin học",
    "Toan": "5.80",
    "Anh": "7.00",
    "Van": "7.25",
    "MonChuyen": "3.00",
    "TongDiem": "24.55"
  },
  {
    "SBD": "250886",
    "HoTen": "Bùi Gia Thanh",
    "NgaySinh": "13/04/2010",
    "Chuyen": "Tin học",
    "Toan": "9.00",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "12.50",
    "TongDiem": "43.75"
  },
  {
    "SBD": "250887",
    "HoTen": "Trần Mạnh Trí",
    "NgaySinh": "05/08/2010",
    "Chuyen": "Tin học",
    "Toan": "6.30",
    "Anh": "6.25",
    "Van": "7.25",
    "MonChuyen": "3.50",
    "TongDiem": "25.05"
  },
  {
    "SBD": "250888",
    "HoTen": "Nguyễn Bá Vân Trường",
    "NgaySinh": "26/12/2010",
    "Chuyen": "Tin học",
    "Toan": "7.80",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "13.00",
    "TongDiem": "43.30"
  },
  {
    "SBD": "250889",
    "HoTen": "Hoàng Tùng Nhật Vũ",
    "NgaySinh": "28/02/2010",
    "Chuyen": "Tin học",
    "Toan": "6.00",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "7.50",
    "TongDiem": "29.75"
  },
  {
    "SBD": "250890",
    "HoTen": "Phạm Quang Vũ",
    "NgaySinh": "28/05/2010",
    "Chuyen": "Tin học",
    "Toan": "5.30",
    "Anh": "5.25",
    "Van": "7.00",
    "MonChuyen": "2.00",
    "TongDiem": "20.55"
  },
  {
    "SBD": "250891",
    "HoTen": "Lưu Văn An",
    "NgaySinh": "27/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.60",
    "Anh": "7.25",
    "Van": "6.75",
    "MonChuyen": "7.63",
    "TongDiem": "31.05"
  },
  {
    "SBD": "250892",
    "HoTen": "Nguyễn Văn An",
    "NgaySinh": "19/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.30",
    "Anh": "7.75",
    "Van": "5.75",
    "MonChuyen": "3.63",
    "TongDiem": "25.25"
  },
  {
    "SBD": "250893",
    "HoTen": "Võ Văn Đại An",
    "NgaySinh": "01/06/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.70",
    "Anh": "8.75",
    "Van": "6.25",
    "MonChuyen": "5.25",
    "TongDiem": "28.58"
  },
  {
    "SBD": "250894",
    "HoTen": "Nguyễn Thị Huyền Anh",
    "NgaySinh": "13/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.10",
    "Anh": "5.00",
    "Van": "6.25",
    "MonChuyen": "0.75",
    "TongDiem": "17.48"
  },
  {
    "SBD": "250895",
    "HoTen": "Phạm Thị Lan Anh",
    "NgaySinh": "11/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "4.50",
    "Anh": "6.25",
    "Van": "6.75",
    "MonChuyen": "9.70",
    "TongDiem": "32.05"
  },
  {
    "SBD": "250896",
    "HoTen": "Phan Văn Tuấn Anh",
    "NgaySinh": "13/11/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.30",
    "Anh": "7.50",
    "Van": "5.75",
    "MonChuyen": "14.75",
    "TongDiem": "40.68"
  },
  {
    "SBD": "250897",
    "HoTen": "Trần Thị Thuỳ Anh",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.90",
    "Anh": "5.50",
    "Van": "5.75",
    "MonChuyen": "8.38",
    "TongDiem": "30.72"
  },
  {
    "SBD": "250898",
    "HoTen": "Phạm Huy Bảo",
    "NgaySinh": "14/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.80",
    "Anh": "5.25",
    "Van": "6.50",
    "MonChuyen": "1.50",
    "TongDiem": "19.80"
  },
  {
    "SBD": "250899",
    "HoTen": "Trần Gia Bảo",
    "NgaySinh": "28/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.90",
    "Anh": "8.00",
    "Van": "6.75",
    "MonChuyen": "13.88",
    "TongDiem": "43.47"
  },
  {
    "SBD": "250901",
    "HoTen": "Nguyễn Minh Châu",
    "NgaySinh": "22/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.70",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "11.75",
    "TongDiem": "41.08"
  },
  {
    "SBD": "250902",
    "HoTen": "Nguyễn Phương Chi",
    "NgaySinh": "07/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.10",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "14.38",
    "TongDiem": "44.92"
  },
  {
    "SBD": "250903",
    "HoTen": "Nguyễn Yến Chi",
    "NgaySinh": "07/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.40",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "12.38",
    "TongDiem": "41.22"
  },
  {
    "SBD": "250904",
    "HoTen": "Phan Tùng Chi",
    "NgaySinh": "15/12/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.90",
    "Anh": "8.75",
    "Van": "7.00",
    "MonChuyen": "12.75",
    "TongDiem": "42.78"
  },
  {
    "SBD": "250905",
    "HoTen": "Trần Thị Bảo Chi",
    "NgaySinh": "11/06/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.90",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "11.63",
    "TongDiem": "40.60"
  },
  {
    "SBD": "250906",
    "HoTen": "Võ Thị Quỳnh Chi",
    "NgaySinh": "23/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.20",
    "Anh": "7.25",
    "Van": "6.75",
    "MonChuyen": "7.50",
    "TongDiem": "30.45"
  },
  {
    "SBD": "250907",
    "HoTen": "Nguyễn Phú Cường",
    "NgaySinh": "23/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.90",
    "Anh": "7.75",
    "Van": "7.25",
    "MonChuyen": "11.50",
    "TongDiem": "40.15"
  },
  {
    "SBD": "250908",
    "HoTen": "Kiều Tuấn Đăng",
    "NgaySinh": "30/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.20",
    "Anh": "7.75",
    "Van": "6.25",
    "MonChuyen": "6.75",
    "TongDiem": "31.33"
  },
  {
    "SBD": "250909",
    "HoTen": "Nguyễn Bảo Đông",
    "NgaySinh": "02/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.70",
    "Anh": "7.75",
    "Van": "6.00",
    "MonChuyen": "13.25",
    "TongDiem": "42.33"
  },
  {
    "SBD": "250910",
    "HoTen": "Nguyễn Đình Minh Đức",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "4.60",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "2.63",
    "TongDiem": "21.05"
  },
  {
    "SBD": "250911",
    "HoTen": "Trần Trung Đức",
    "NgaySinh": "05/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.20",
    "Anh": "4.75",
    "Van": "6.50",
    "MonChuyen": "1.50",
    "TongDiem": "18.70"
  },
  {
    "SBD": "250912",
    "HoTen": "Hoàng Lê Dũng",
    "NgaySinh": "25/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.20",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "13.50",
    "TongDiem": "40.20"
  },
  {
    "SBD": "250913",
    "HoTen": "Ngô Việt Dũng",
    "NgaySinh": "27/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.90",
    "Anh": "8.25",
    "Van": "7.25",
    "MonChuyen": "6.88",
    "TongDiem": "33.72"
  },
  {
    "SBD": "250914",
    "HoTen": "Nguyễn Đức Dương",
    "NgaySinh": "14/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.30",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "7.75",
    "TongDiem": "32.18"
  },
  {
    "SBD": "250915",
    "HoTen": "Trần Nhất Duy",
    "NgaySinh": "04/02/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.30",
    "Anh": "6.75",
    "Van": "7.25",
    "MonChuyen": "7.75",
    "TongDiem": "30.93"
  },
  {
    "SBD": "250916",
    "HoTen": "Hoàng Châu Giang",
    "NgaySinh": "13/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.60",
    "Anh": "8.25",
    "Van": "6.50",
    "MonChuyen": "6.75",
    "TongDiem": "30.48"
  },
  {
    "SBD": "250917",
    "HoTen": "Nguyễn Bùi Lam Giang",
    "NgaySinh": "12/11/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.00",
    "Anh": "6.00",
    "Van": "6.75",
    "MonChuyen": "13.50",
    "TongDiem": "39.00"
  },
  {
    "SBD": "250918",
    "HoTen": "Đặng Việt Hà",
    "NgaySinh": "04/04/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.40",
    "Anh": "6.75",
    "Van": "6.25",
    "MonChuyen": "12.50",
    "TongDiem": "38.15"
  },
  {
    "SBD": "250919",
    "HoTen": "Đào Nguyễn Ngọc Hà",
    "NgaySinh": "14/12/2009",
    "Chuyen": "Hoá học",
    "Toan": "4.70",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "1.50",
    "TongDiem": "19.95"
  },
  {
    "SBD": "250920",
    "HoTen": "Hồ Quỳnh Hà",
    "NgaySinh": "06/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "4.30",
    "Anh": "6.25",
    "Van": "7.25",
    "MonChuyen": "11.25",
    "TongDiem": "34.68"
  },
  {
    "SBD": "250921",
    "HoTen": "Lê Quang Hải",
    "NgaySinh": "28/02/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.70",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "10.45",
    "TongDiem": "38.38"
  },
  {
    "SBD": "250922",
    "HoTen": "Nguyễn Minh Hải",
    "NgaySinh": "07/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.40",
    "Anh": "4.50",
    "Van": "5.00",
    "MonChuyen": "4.13",
    "TongDiem": "21.10"
  },
  {
    "SBD": "250923",
    "HoTen": "Trần Phú Hào",
    "NgaySinh": "14/04/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.40",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "16.50",
    "TongDiem": "48.15"
  },
  {
    "SBD": "250924",
    "HoTen": "Trần Nguyên Hiếu",
    "NgaySinh": "21/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "4.80",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "6.88",
    "TongDiem": "27.62"
  },
  {
    "SBD": "250925",
    "HoTen": "Hồ Thị Thanh Hoàn",
    "NgaySinh": "02/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.00",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "10.38",
    "TongDiem": "37.57"
  },
  {
    "SBD": "250927",
    "HoTen": "Ngô Sỹ Hùng",
    "NgaySinh": "31/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.60",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "16.88",
    "TongDiem": "49.17"
  },
  {
    "SBD": "250928",
    "HoTen": "Lê Khánh Hưng",
    "NgaySinh": "31/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.20",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "13.25",
    "TongDiem": "41.08"
  },
  {
    "SBD": "250929",
    "HoTen": "Mai Viết Hưng",
    "NgaySinh": "05/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.40",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "12.75",
    "TongDiem": "40.53"
  },
  {
    "SBD": "250930",
    "HoTen": "Bùi Hoàng Huy",
    "NgaySinh": "07/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.40",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "16.63",
    "TongDiem": "48.60"
  },
  {
    "SBD": "250931",
    "HoTen": "Trần Quốc Huy",
    "NgaySinh": "01/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.30",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "8.25",
    "TongDiem": "33.43"
  },
  {
    "SBD": "250932",
    "HoTen": "Trần Tuấn Khải",
    "NgaySinh": "07/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.30",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "7.38",
    "TongDiem": "29.62"
  },
  {
    "SBD": "250933",
    "HoTen": "Mạnh Xuân Khang",
    "NgaySinh": "14/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.50",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "11.13",
    "TongDiem": "38.20"
  },
  {
    "SBD": "250934",
    "HoTen": "Ngô Hoàng Khánh",
    "NgaySinh": "28/12/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.00",
    "Anh": "7.50",
    "Van": "6.25",
    "MonChuyen": "6.88",
    "TongDiem": "31.07"
  },
  {
    "SBD": "250935",
    "HoTen": "Nguyễn Quang Khánh",
    "NgaySinh": "20/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.00",
    "Anh": "6.00",
    "Van": "6.50",
    "MonChuyen": "4.50",
    "TongDiem": "26.25"
  },
  {
    "SBD": "250936",
    "HoTen": "Trần Duy Khánh",
    "NgaySinh": "30/11/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.30",
    "Anh": "8.00",
    "Van": "6.50",
    "MonChuyen": "9.50",
    "TongDiem": "35.05"
  },
  {
    "SBD": "250937",
    "HoTen": "Nguyễn Anh Khôi",
    "NgaySinh": "13/06/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.30",
    "Anh": "8.25",
    "Van": "6.75",
    "MonChuyen": "15.13",
    "TongDiem": "46.00"
  },
  {
    "SBD": "250938",
    "HoTen": "Nguyễn Trung Kiên",
    "NgaySinh": "19/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.00",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "9.25",
    "TongDiem": "38.13"
  },
  {
    "SBD": "250939",
    "HoTen": "Nguyễn Nguyên Tuấn Kiệt",
    "NgaySinh": "02/12/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.20",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "13.25",
    "TongDiem": "43.58"
  },
  {
    "SBD": "250940",
    "HoTen": "Lê Văn Lam",
    "NgaySinh": "20/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "9.30",
    "Anh": "9.50",
    "Van": "6.50",
    "MonChuyen": "18.00",
    "TongDiem": "52.30"
  },
  {
    "SBD": "250941",
    "HoTen": "Nguyễn Đức Lâm",
    "NgaySinh": "10/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.10",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "5.13",
    "TongDiem": "25.80"
  },
  {
    "SBD": "250942",
    "HoTen": "Nguyễn Hoàng Linh",
    "NgaySinh": "18/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "4.70",
    "Anh": "5.00",
    "Van": "7.00",
    "MonChuyen": "5.25",
    "TongDiem": "24.58"
  },
  {
    "SBD": "250943",
    "HoTen": "Nguyễn Vũ Khánh Linh",
    "NgaySinh": "31/07/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.50",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "8.75",
    "TongDiem": "36.13"
  },
  {
    "SBD": "250944",
    "HoTen": "Nhữ Võ Huyền Diệu Linh",
    "NgaySinh": "27/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.40",
    "Anh": "8.00",
    "Van": "7.50",
    "MonChuyen": "13.13",
    "TongDiem": "41.60"
  },
  {
    "SBD": "250945",
    "HoTen": "Phạm Hà Linh",
    "NgaySinh": "05/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.60",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "15.63",
    "TongDiem": "45.05"
  },
  {
    "SBD": "250946",
    "HoTen": "Phùng Thị Bảo Linh",
    "NgaySinh": "25/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "9.40",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "11.50",
    "TongDiem": "42.15"
  },
  {
    "SBD": "250947",
    "HoTen": "Thái Đức Mạnh",
    "NgaySinh": "09/02/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.50",
    "Anh": "9.25",
    "Van": "6.00",
    "MonChuyen": "8.38",
    "TongDiem": "33.32"
  },
  {
    "SBD": "250948",
    "HoTen": "Vi Văn Mạnh",
    "NgaySinh": "01/11/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.60",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "10.13",
    "TongDiem": "33.55"
  },
  {
    "SBD": "250949",
    "HoTen": "Võ Đức Mạnh",
    "NgaySinh": "21/06/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.40",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "5.75",
    "TongDiem": "28.03"
  },
  {
    "SBD": "250950",
    "HoTen": "Hoàng Tiến Minh",
    "NgaySinh": "11/06/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.20",
    "Anh": "6.50",
    "Van": "6.25",
    "MonChuyen": "13.88",
    "TongDiem": "39.77"
  },
  {
    "SBD": "250951",
    "HoTen": "Lương Bình Minh",
    "NgaySinh": "18/11/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.50",
    "Anh": "5.50",
    "Van": "7.50",
    "MonChuyen": "6.13",
    "TongDiem": "28.70"
  },
  {
    "SBD": "250954",
    "HoTen": "Nguyễn Trần Quốc Minh",
    "NgaySinh": "03/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.50",
    "Anh": "6.75",
    "Van": "6.00",
    "MonChuyen": "12.38",
    "TongDiem": "38.82"
  },
  {
    "SBD": "250955",
    "HoTen": "Phạm Xuân Minh",
    "NgaySinh": "19/02/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.30",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "10.88",
    "TongDiem": "36.12"
  },
  {
    "SBD": "250956",
    "HoTen": "Trịnh Lê Minh",
    "NgaySinh": "03/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.20",
    "Anh": "8.50",
    "Van": "6.25",
    "MonChuyen": "10.25",
    "TongDiem": "36.33"
  },
  {
    "SBD": "250957",
    "HoTen": "Trịnh Nguyễn Trà My",
    "NgaySinh": "25/07/2010",
    "Chuyen": "Hoá học",
    "Toan": "4.40",
    "Anh": "5.25",
    "Van": "7.00",
    "MonChuyen": "4.63",
    "TongDiem": "23.60"
  },
  {
    "SBD": "250958",
    "HoTen": "Biện Thảo Nguyên",
    "NgaySinh": "05/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.70",
    "Anh": "9.00",
    "Van": "7.50",
    "MonChuyen": "17.88",
    "TongDiem": "51.02"
  },
  {
    "SBD": "250959",
    "HoTen": "Đậu Phạm Nhật Nguyên",
    "NgaySinh": "22/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.60",
    "Anh": "9.25",
    "Van": "7.25",
    "MonChuyen": "11.63",
    "TongDiem": "40.55"
  },
  {
    "SBD": "250960",
    "HoTen": "Lê Thảo Nguyên",
    "NgaySinh": "03/02/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.20",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "11.88",
    "TongDiem": "40.02"
  },
  {
    "SBD": "250961",
    "HoTen": "Trần Ngọc Nguyên",
    "NgaySinh": "17/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.00",
    "Anh": "9.00",
    "Van": "7.50",
    "MonChuyen": "13.50",
    "TongDiem": "43.75"
  },
  {
    "SBD": "250962",
    "HoTen": "Nguyễn Gia Tuệ Nhi",
    "NgaySinh": "13/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.30",
    "Anh": "5.50",
    "Van": "6.75",
    "MonChuyen": "4.50",
    "TongDiem": "25.30"
  },
  {
    "SBD": "250963",
    "HoTen": "Nguyễn Thảo Nhi",
    "NgaySinh": "28/04/2010",
    "Chuyen": "Hoá học",
    "Toan": "4.80",
    "Anh": "5.50",
    "Van": "6.75",
    "MonChuyen": "5.50",
    "TongDiem": "25.30"
  },
  {
    "SBD": "250964",
    "HoTen": "Nguyễn Yến Nhi",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.00",
    "Anh": "7.25",
    "Van": "7.00",
    "MonChuyen": "15.13",
    "TongDiem": "43.95"
  },
  {
    "SBD": "250965",
    "HoTen": "Nguyễn Mai Nhung",
    "NgaySinh": "26/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.10",
    "Anh": "7.00",
    "Van": "7.75",
    "MonChuyen": "11.00",
    "TongDiem": "36.35"
  },
  {
    "SBD": "250966",
    "HoTen": "Phạm Trang Nhung",
    "NgaySinh": "25/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.70",
    "Anh": "9.50",
    "Van": "7.75",
    "MonChuyen": "15.25",
    "TongDiem": "46.83"
  },
  {
    "SBD": "250967",
    "HoTen": "Nguyễn Gia Phát",
    "NgaySinh": "10/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.40",
    "Anh": "7.00",
    "Van": "6.25",
    "MonChuyen": "3.00",
    "TongDiem": "23.15"
  },
  {
    "SBD": "250968",
    "HoTen": "Trần Nam Phong",
    "NgaySinh": "21/12/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.00",
    "Anh": "7.50",
    "Van": "6.75",
    "MonChuyen": "12.88",
    "TongDiem": "39.57"
  },
  {
    "SBD": "250969",
    "HoTen": "Bùi Hồng Phúc",
    "NgaySinh": "08/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "3.00",
    "Anh": "3.50",
    "Van": "5.25",
    "MonChuyen": "3.13",
    "TongDiem": "16.45"
  },
  {
    "SBD": "250970",
    "HoTen": "Lê Trọng Phúc",
    "NgaySinh": "21/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.70",
    "Anh": "6.75",
    "Van": "7.00",
    "MonChuyen": "9.25",
    "TongDiem": "34.33"
  },
  {
    "SBD": "250971",
    "HoTen": "Cao Xuân Phước",
    "NgaySinh": "03/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.90",
    "Anh": "9.00",
    "Van": "6.25",
    "MonChuyen": "14.88",
    "TongDiem": "44.47"
  },
  {
    "SBD": "250972",
    "HoTen": "Chu Trọng Phước",
    "NgaySinh": "23/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.00",
    "Anh": "6.00",
    "Van": "7.00",
    "MonChuyen": "12.50",
    "TongDiem": "37.75"
  },
  {
    "SBD": "250973",
    "HoTen": "Nguyễn Hồ Tấn Phước",
    "NgaySinh": "21/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.30",
    "Anh": "6.00",
    "Van": "7.25",
    "MonChuyen": "7.25",
    "TongDiem": "30.43"
  },
  {
    "SBD": "250974",
    "HoTen": "Đặng Hoàng Phương",
    "NgaySinh": "01/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.80",
    "Anh": "5.00",
    "Van": "6.25",
    "MonChuyen": "4.88",
    "TongDiem": "25.37"
  },
  {
    "SBD": "250975",
    "HoTen": "Hồ Minh Quân",
    "NgaySinh": "07/02/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.90",
    "Anh": "5.75",
    "Van": "6.25",
    "MonChuyen": "13.25",
    "TongDiem": "37.78"
  },
  {
    "SBD": "250976",
    "HoTen": "Lê Đức Anh Quân",
    "NgaySinh": "21/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.60",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "16.38",
    "TongDiem": "47.17"
  },
  {
    "SBD": "250977",
    "HoTen": "Lê Mạnh Quân",
    "NgaySinh": "25/11/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.10",
    "Anh": "6.75",
    "Van": "6.50",
    "MonChuyen": "4.00",
    "TongDiem": "27.35"
  },
  {
    "SBD": "250978",
    "HoTen": "Nguyễn Duy Minh Quân",
    "NgaySinh": "26/04/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.40",
    "Anh": "6.00",
    "Van": "7.00",
    "MonChuyen": "7.75",
    "TongDiem": "30.03"
  },
  {
    "SBD": "250979",
    "HoTen": "Nguyễn Trường Quân",
    "NgaySinh": "11/04/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.20",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "12.13",
    "TongDiem": "37.40"
  },
  {
    "SBD": "250980",
    "HoTen": "Phan Đăng Lê Quân",
    "NgaySinh": "20/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.40",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "8.25",
    "TongDiem": "33.78"
  },
  {
    "SBD": "250981",
    "HoTen": "Tạ Hoàng Quân",
    "NgaySinh": "01/02/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.30",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "9.38",
    "TongDiem": "37.62"
  },
  {
    "SBD": "250982",
    "HoTen": "Võ Minh Quân",
    "NgaySinh": "01/04/2010",
    "Chuyen": "Hoá học",
    "Toan": "3.60",
    "Anh": "5.25",
    "Van": "6.00",
    "MonChuyen": "5.75",
    "TongDiem": "23.48"
  },
  {
    "SBD": "250983",
    "HoTen": "Chu Lê Nhật Quang",
    "NgaySinh": "12/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.80",
    "Anh": "6.25",
    "Van": "6.00",
    "MonChuyen": "4.13",
    "TongDiem": "24.25"
  },
  {
    "SBD": "250984",
    "HoTen": "Đặng Tiến Quý",
    "NgaySinh": "19/12/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.80",
    "Anh": "6.75",
    "Van": "6.50",
    "MonChuyen": "5.75",
    "TongDiem": "28.68"
  },
  {
    "SBD": "250985",
    "HoTen": "Phan Văn Quang Sáng",
    "NgaySinh": "29/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.00",
    "Anh": "8.75",
    "Van": "6.25",
    "MonChuyen": "9.50",
    "TongDiem": "36.25"
  },
  {
    "SBD": "250986",
    "HoTen": "Hoàng Minh Sơn",
    "NgaySinh": "28/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.10",
    "Anh": "7.00",
    "Van": "6.75",
    "MonChuyen": "5.88",
    "TongDiem": "29.67"
  },
  {
    "SBD": "250987",
    "HoTen": "Nguyễn Sỹ Sơn",
    "NgaySinh": "28/10/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.20",
    "Anh": "7.25",
    "Van": "7.00",
    "MonChuyen": "9.38",
    "TongDiem": "35.52"
  },
  {
    "SBD": "250988",
    "HoTen": "Chu Thế Tài",
    "NgaySinh": "23/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.40",
    "Anh": "10.00",
    "Van": "7.25",
    "MonChuyen": "16.75",
    "TongDiem": "50.78"
  },
  {
    "SBD": "250989",
    "HoTen": "Hoàng Nguyễn Anh Tài",
    "NgaySinh": "30/07/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.30",
    "Anh": "7.25",
    "Van": "5.75",
    "MonChuyen": "12.88",
    "TongDiem": "39.62"
  },
  {
    "SBD": "250990",
    "HoTen": "Hồ Thị Minh Tâm",
    "NgaySinh": "12/08/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.60",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "13.88",
    "TongDiem": "43.42"
  },
  {
    "SBD": "250991",
    "HoTen": "Ngô Thị Mỹ Tâm",
    "NgaySinh": "04/06/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.80",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "11.25",
    "TongDiem": "40.18"
  },
  {
    "SBD": "250992",
    "HoTen": "Lê Đình Thắng",
    "NgaySinh": "08/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.10",
    "Anh": "6.25",
    "Van": "7.00",
    "MonChuyen": "14.25",
    "TongDiem": "40.73"
  },
  {
    "SBD": "250993",
    "HoTen": "Trần Công Thành",
    "NgaySinh": "23/07/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.00",
    "Anh": "4.25",
    "Van": "5.25",
    "MonChuyen": "10.63",
    "TongDiem": "31.45"
  },
  {
    "SBD": "250994",
    "HoTen": "Trần Hữu Thành",
    "NgaySinh": "14/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.00",
    "Anh": "5.25",
    "Van": "6.75",
    "MonChuyen": "10.38",
    "TongDiem": "34.57"
  },
  {
    "SBD": "250995",
    "HoTen": "Vũ Nguyễn Nhật Thành",
    "NgaySinh": "28/09/2010",
    "Chuyen": "Hoá học",
    "Toan": "4.20",
    "Anh": "3.25",
    "Van": "6.25",
    "MonChuyen": "4.00",
    "TongDiem": "19.70"
  },
  {
    "SBD": "250996",
    "HoTen": "Nguyễn Lâm Thiên",
    "NgaySinh": "17/04/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.90",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "12.25",
    "TongDiem": "42.78"
  },
  {
    "SBD": "250999",
    "HoTen": "Trần Phương Thủy",
    "NgaySinh": "27/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.00",
    "Anh": "7.75",
    "Van": "7.25",
    "MonChuyen": "4.63",
    "TongDiem": "27.95"
  },
  {
    "SBD": "251000",
    "HoTen": "Nguyễn Đặng Minh Trang",
    "NgaySinh": "28/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.20",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "16.88",
    "TongDiem": "48.52"
  },
  {
    "SBD": "251001",
    "HoTen": "Nguyễn Hoàng Quỳnh Trang",
    "NgaySinh": "23/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.00",
    "Anh": "7.25",
    "Van": "7.75",
    "MonChuyen": "11.88",
    "TongDiem": "40.82"
  },
  {
    "SBD": "251002",
    "HoTen": "Võ Hoàng Minh Trang",
    "NgaySinh": "24/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "4.60",
    "Anh": "8.00",
    "Van": "6.75",
    "MonChuyen": "4.13",
    "TongDiem": "25.55"
  },
  {
    "SBD": "251003",
    "HoTen": "Hoàng Viết Triều",
    "NgaySinh": "08/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.20",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "17.25",
    "TongDiem": "50.08"
  },
  {
    "SBD": "251004",
    "HoTen": "Hoàng Nghĩa Việt Trung",
    "NgaySinh": "03/01/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.10",
    "Anh": "7.00",
    "Van": "6.50",
    "MonChuyen": "4.13",
    "TongDiem": "25.80"
  },
  {
    "SBD": "251005",
    "HoTen": "Nguyễn Đình Trung",
    "NgaySinh": "22/02/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.10",
    "Anh": "7.25",
    "Van": "7.00",
    "MonChuyen": "7.88",
    "TongDiem": "32.17"
  },
  {
    "SBD": "251006",
    "HoTen": "Phạm Minh Trung",
    "NgaySinh": "09/02/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.50",
    "Anh": "8.00",
    "Van": "6.75",
    "MonChuyen": "14.88",
    "TongDiem": "45.57"
  },
  {
    "SBD": "251007",
    "HoTen": "Đặng Quốc Trường",
    "NgaySinh": "07/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "7.70",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "16.25",
    "TongDiem": "48.08"
  },
  {
    "SBD": "251008",
    "HoTen": "Nguyễn Văn Anh Tuấn",
    "NgaySinh": "15/12/2010",
    "Chuyen": "Hoá học",
    "Toan": "8.20",
    "Anh": "9.50",
    "Van": "7.50",
    "MonChuyen": "12.75",
    "TongDiem": "44.33"
  },
  {
    "SBD": "251010",
    "HoTen": "Nguyễn Thị Khánh Vân",
    "NgaySinh": "14/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.70",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "14.75",
    "TongDiem": "44.33"
  },
  {
    "SBD": "251011",
    "HoTen": "Nguyễn Ngọc Tường Vi",
    "NgaySinh": "08/07/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.50",
    "Anh": "7.50",
    "Van": "7.50",
    "MonChuyen": "5.25",
    "TongDiem": "29.38"
  },
  {
    "SBD": "251012",
    "HoTen": "Nguyễn Hữu Thành Vinh",
    "NgaySinh": "04/04/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.80",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "8.50",
    "TongDiem": "35.55"
  },
  {
    "SBD": "251013",
    "HoTen": "Hoàng Minh Vũ",
    "NgaySinh": "21/03/2010",
    "Chuyen": "Hoá học",
    "Toan": "5.50",
    "Anh": "5.75",
    "Van": "6.75",
    "MonChuyen": "8.00",
    "TongDiem": "30.00"
  },
  {
    "SBD": "251014",
    "HoTen": "Lê Hoàng Vũ",
    "NgaySinh": "03/05/2010",
    "Chuyen": "Hoá học",
    "Toan": "6.30",
    "Anh": "7.75",
    "Van": "6.25",
    "MonChuyen": "3.88",
    "TongDiem": "26.12"
  },
  {
    "SBD": "251015",
    "HoTen": "Đậu Bình An",
    "NgaySinh": "05/08/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.60",
    "Anh": "7.75",
    "Van": "6.00",
    "MonChuyen": "13.00",
    "TongDiem": "39.85"
  },
  {
    "SBD": "251016",
    "HoTen": "Từ Thái An",
    "NgaySinh": "16/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.30",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "10.50",
    "TongDiem": "39.80"
  },
  {
    "SBD": "251017",
    "HoTen": "Lê Đức Anh",
    "NgaySinh": "25/11/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.70",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "4.75",
    "TongDiem": "29.83"
  },
  {
    "SBD": "251018",
    "HoTen": "Nguyễn Tuấn Anh",
    "NgaySinh": "21/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.90",
    "Anh": "5.25",
    "Van": "7.50",
    "MonChuyen": "6.75",
    "TongDiem": "29.78"
  },
  {
    "SBD": "251019",
    "HoTen": "Phan Đình Bách",
    "NgaySinh": "29/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.50",
    "Anh": "9.00",
    "Van": "6.25",
    "MonChuyen": "5.25",
    "TongDiem": "28.63"
  },
  {
    "SBD": "251020",
    "HoTen": "Đặng Đình Thái Bảo",
    "NgaySinh": "26/05/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.90",
    "Anh": "9.50",
    "Van": "6.75",
    "MonChuyen": "5.00",
    "TongDiem": "29.65"
  },
  {
    "SBD": "251021",
    "HoTen": "Đặng Lê Gia Bảo",
    "NgaySinh": "01/05/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.90",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "3.75",
    "TongDiem": "28.78"
  },
  {
    "SBD": "251022",
    "HoTen": "Lê Đình Bảo",
    "NgaySinh": "01/06/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.20",
    "Anh": "6.00",
    "Van": "6.00",
    "MonChuyen": "2.50",
    "TongDiem": "20.95"
  },
  {
    "SBD": "251023",
    "HoTen": "Nguyễn Hữu Gia Bảo",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.30",
    "Anh": "8.75",
    "Van": "7.50",
    "MonChuyen": "11.00",
    "TongDiem": "41.05"
  },
  {
    "SBD": "251024",
    "HoTen": "Nguyễn Võ Hoài Bảo",
    "NgaySinh": "27/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.40",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "11.25",
    "TongDiem": "42.03"
  },
  {
    "SBD": "251025",
    "HoTen": "Phan Thiện Bảo",
    "NgaySinh": "17/02/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.70",
    "Anh": "9.00",
    "Van": "7.50",
    "MonChuyen": "10.00",
    "TongDiem": "40.20"
  },
  {
    "SBD": "251026",
    "HoTen": "Đặng Vương Đăng",
    "NgaySinh": "08/06/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.80",
    "Anh": "8.75",
    "Van": "7.50",
    "MonChuyen": "9.50",
    "TongDiem": "38.30"
  },
  {
    "SBD": "251027",
    "HoTen": "Nguyễn Trần Khánh Đăng",
    "NgaySinh": "28/11/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.80",
    "Anh": "7.25",
    "Van": "5.50",
    "MonChuyen": "11.25",
    "TongDiem": "36.43"
  },
  {
    "SBD": "251028",
    "HoTen": "Trần Quang Đạo",
    "NgaySinh": "02/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.20",
    "Anh": "7.50",
    "Van": "6.75",
    "MonChuyen": "13.75",
    "TongDiem": "43.08"
  },
  {
    "SBD": "251029",
    "HoTen": "Võ Tuấn Đạt",
    "NgaySinh": "13/09/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.20",
    "Anh": "5.00",
    "Van": "6.50",
    "MonChuyen": "9.25",
    "TongDiem": "32.58"
  },
  {
    "SBD": "251030",
    "HoTen": "Đinh Nhật Đức",
    "NgaySinh": "28/06/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.80",
    "Anh": "5.75",
    "Van": "5.50",
    "MonChuyen": "4.25",
    "TongDiem": "23.43"
  },
  {
    "SBD": "251031",
    "HoTen": "Hồ Minh Đức",
    "NgaySinh": "13/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.30",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "7.50",
    "TongDiem": "30.05"
  },
  {
    "SBD": "251032",
    "HoTen": "Trần Đình Đức",
    "NgaySinh": "09/08/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.60",
    "Anh": "6.75",
    "Van": "8.00",
    "MonChuyen": "3.25",
    "TongDiem": "25.23"
  },
  {
    "SBD": "251033",
    "HoTen": "Hồ Thanh Dũng",
    "NgaySinh": "11/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "4.10",
    "Anh": "4.00",
    "Van": "6.25",
    "MonChuyen": "1.75",
    "TongDiem": "16.98"
  },
  {
    "SBD": "251034",
    "HoTen": "Nguyễn Anh Dũng",
    "NgaySinh": "13/08/2010",
    "Chuyen": "Vật lí",
    "Toan": "4.80",
    "Anh": "4.75",
    "Van": "6.50",
    "MonChuyen": "3.00",
    "TongDiem": "20.55"
  },
  {
    "SBD": "251035",
    "HoTen": "Thái Đình Anh Dũng",
    "NgaySinh": "10/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "4.80",
    "Anh": "4.75",
    "Van": "6.50",
    "MonChuyen": "2.25",
    "TongDiem": "19.43"
  },
  {
    "SBD": "251036",
    "HoTen": "Trần Trung Dũng",
    "NgaySinh": "12/11/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.90",
    "Anh": "8.00",
    "Van": "6.75",
    "MonChuyen": "10.50",
    "TongDiem": "37.40"
  },
  {
    "SBD": "251037",
    "HoTen": "Võ Tấn Dũng",
    "NgaySinh": "20/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "9.50",
    "Anh": "9.50",
    "Van": "6.25",
    "MonChuyen": "15.25",
    "TongDiem": "48.13"
  },
  {
    "SBD": "251038",
    "HoTen": "Hồ Bảo Duy",
    "NgaySinh": "27/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.60",
    "Anh": "7.25",
    "Van": "6.50",
    "MonChuyen": "11.00",
    "TongDiem": "36.85"
  },
  {
    "SBD": "251039",
    "HoTen": "Phạm Ngọc Duy",
    "NgaySinh": "25/02/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.00",
    "Anh": "4.75",
    "Van": "6.00",
    "MonChuyen": "5.25",
    "TongDiem": "24.63"
  },
  {
    "SBD": "251040",
    "HoTen": "Lê Trọng Hải",
    "NgaySinh": "17/02/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.50",
    "Anh": "7.75",
    "Van": "6.50",
    "MonChuyen": "4.75",
    "TongDiem": "27.88"
  },
  {
    "SBD": "251041",
    "HoTen": "Hồ Minh Hiếu",
    "NgaySinh": "23/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.50",
    "Anh": "5.50",
    "Van": "6.75",
    "MonChuyen": "7.50",
    "TongDiem": "32.00"
  },
  {
    "SBD": "251042",
    "HoTen": "Hoàng Nhật Minh Hiếu",
    "NgaySinh": "07/05/2010",
    "Chuyen": "Vật lí",
    "Toan": "9.80",
    "Anh": "8.75",
    "Van": "7.50",
    "MonChuyen": "15.00",
    "TongDiem": "48.55"
  },
  {
    "SBD": "251044",
    "HoTen": "Hồ Xuân Hùng",
    "NgaySinh": "27/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.10",
    "Anh": "8.25",
    "Van": "7.50",
    "MonChuyen": "7.25",
    "TongDiem": "33.73"
  },
  {
    "SBD": "251045",
    "HoTen": "Nguyễn Gia Hưng",
    "NgaySinh": "12/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.30",
    "Anh": "8.25",
    "Van": "6.75",
    "MonChuyen": "12.50",
    "TongDiem": "42.05"
  },
  {
    "SBD": "251046",
    "HoTen": "Thái Gia Hưng",
    "NgaySinh": "01/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.40",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "14.00",
    "TongDiem": "45.40"
  },
  {
    "SBD": "251047",
    "HoTen": "Bùi Gia Huy",
    "NgaySinh": "26/09/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.00",
    "Anh": "5.00",
    "Van": "7.00",
    "MonChuyen": "4.50",
    "TongDiem": "23.75"
  },
  {
    "SBD": "251048",
    "HoTen": "Trần Doãn Quang Huy",
    "NgaySinh": "04/02/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.30",
    "Anh": "5.50",
    "Van": "5.50",
    "MonChuyen": "6.50",
    "TongDiem": "28.05"
  },
  {
    "SBD": "251049",
    "HoTen": "Bùi Danh Khang",
    "NgaySinh": "25/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.00",
    "Anh": "8.50",
    "Van": "7.25",
    "MonChuyen": "3.75",
    "TongDiem": "26.38"
  },
  {
    "SBD": "251050",
    "HoTen": "Nguyễn Duy Khánh",
    "NgaySinh": "26/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.50",
    "Anh": "8.50",
    "Van": "7.75",
    "MonChuyen": "14.00",
    "TongDiem": "44.75"
  },
  {
    "SBD": "251051",
    "HoTen": "Đinh Ngọc Khôi",
    "NgaySinh": "02/07/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.70",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "7.25",
    "TongDiem": "33.08"
  },
  {
    "SBD": "251052",
    "HoTen": "Nguyễn Minh Khôi",
    "NgaySinh": "10/02/2010",
    "Chuyen": "Vật lí",
    "Toan": "4.30",
    "Anh": "5.75",
    "Van": "5.00",
    "MonChuyen": "6.50",
    "TongDiem": "24.80"
  },
  {
    "SBD": "251053",
    "HoTen": "Nguyễn Đặng Bá Kiên",
    "NgaySinh": "09/12/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.30",
    "Anh": "10.00",
    "Van": "7.00",
    "MonChuyen": "10.50",
    "TongDiem": "41.05"
  },
  {
    "SBD": "251054",
    "HoTen": "Nguyễn Vũ Trúc Lâm",
    "NgaySinh": "10/09/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.60",
    "Anh": "8.25",
    "Van": "8.25",
    "MonChuyen": "16.75",
    "TongDiem": "50.23"
  },
  {
    "SBD": "251055",
    "HoTen": "Nguyễn Xuân Lâm",
    "NgaySinh": "17/09/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.70",
    "Anh": "6.75",
    "Van": "6.75",
    "MonChuyen": "9.25",
    "TongDiem": "34.08"
  },
  {
    "SBD": "251056",
    "HoTen": "Nguyễn Công Liêm",
    "NgaySinh": "01/06/2010",
    "Chuyen": "Vật lí",
    "Toan": "9.30",
    "Anh": "8.00",
    "Van": "6.75",
    "MonChuyen": "12.50",
    "TongDiem": "42.80"
  },
  {
    "SBD": "251057",
    "HoTen": "Võ Khánh Linh",
    "NgaySinh": "22/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.10",
    "Anh": "8.25",
    "Van": "7.75",
    "MonChuyen": "11.50",
    "TongDiem": "41.35"
  },
  {
    "SBD": "251058",
    "HoTen": "Phạm Thành Luân",
    "NgaySinh": "02/06/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.60",
    "Anh": "6.25",
    "Van": "6.00",
    "MonChuyen": "8.75",
    "TongDiem": "30.98"
  },
  {
    "SBD": "251059",
    "HoTen": "Trần Hà Mạnh",
    "NgaySinh": "12/04/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.10",
    "Anh": "4.50",
    "Van": "6.50",
    "MonChuyen": "12.75",
    "TongDiem": "35.23"
  },
  {
    "SBD": "251060",
    "HoTen": "Giao Minh",
    "NgaySinh": "20/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.70",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "11.75",
    "TongDiem": "41.33"
  },
  {
    "SBD": "251061",
    "HoTen": "Hồ Phan Nhật Minh",
    "NgaySinh": "24/02/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.80",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "13.50",
    "TongDiem": "41.80"
  },
  {
    "SBD": "251062",
    "HoTen": "Hoàng Hồ Nhật Minh",
    "NgaySinh": "05/04/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.20",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "4.50",
    "TongDiem": "27.45"
  },
  {
    "SBD": "251063",
    "HoTen": "Nguyễn Hiếu Minh",
    "NgaySinh": "30/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.40",
    "Anh": "9.00",
    "Van": "7.75",
    "MonChuyen": "7.25",
    "TongDiem": "34.03"
  },
  {
    "SBD": "251064",
    "HoTen": "Nguyễn Hoàng Minh",
    "NgaySinh": "09/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.00",
    "Anh": "7.50",
    "Van": "7.25",
    "MonChuyen": "10.00",
    "TongDiem": "37.75"
  },
  {
    "SBD": "251065",
    "HoTen": "Phan Anh Minh",
    "NgaySinh": "10/06/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.40",
    "Anh": "6.50",
    "Van": "5.75",
    "MonChuyen": "10.50",
    "TongDiem": "34.40"
  },
  {
    "SBD": "251067",
    "HoTen": "Tăng Hùng Minh",
    "NgaySinh": "26/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.80",
    "Anh": "8.00",
    "Van": "8.25",
    "MonChuyen": "7.00",
    "TongDiem": "34.55"
  },
  {
    "SBD": "251068",
    "HoTen": "Trịnh Phạm Bảo Minh",
    "NgaySinh": "01/12/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.80",
    "Anh": "6.75",
    "Van": "7.25",
    "MonChuyen": "9.50",
    "TongDiem": "35.05"
  },
  {
    "SBD": "251070",
    "HoTen": "Võ Văn Nhật Minh",
    "NgaySinh": "23/05/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.20",
    "Anh": "7.25",
    "Van": "7.00",
    "MonChuyen": "10.00",
    "TongDiem": "37.45"
  },
  {
    "SBD": "251071",
    "HoTen": "Mai Trần Khôi Nguyên",
    "NgaySinh": "08/09/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.30",
    "Anh": "6.00",
    "Van": "5.75",
    "MonChuyen": "1.75",
    "TongDiem": "20.68"
  },
  {
    "SBD": "251072",
    "HoTen": "Nguyễn Phan Khôi Nguyên",
    "NgaySinh": "30/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "2.40",
    "Anh": "4.00",
    "Van": "5.25",
    "MonChuyen": "6.00",
    "TongDiem": "20.65"
  },
  {
    "SBD": "251073",
    "HoTen": "Nguyễn Xuân Nguyên",
    "NgaySinh": "12/04/2010",
    "Chuyen": "Vật lí",
    "Toan": "9.30",
    "Anh": "9.75",
    "Van": "7.50",
    "MonChuyen": "18.75",
    "TongDiem": "54.68"
  },
  {
    "SBD": "251074",
    "HoTen": "Võ Đình Khai Nguyên",
    "NgaySinh": "19/11/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.60",
    "Anh": "6.00",
    "Van": "6.00",
    "MonChuyen": "5.00",
    "TongDiem": "26.10"
  },
  {
    "SBD": "251075",
    "HoTen": "Bùi Thiện Nhân",
    "NgaySinh": "29/08/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.50",
    "Anh": "7.25",
    "Van": "7.00",
    "MonChuyen": "6.50",
    "TongDiem": "31.50"
  },
  {
    "SBD": "251076",
    "HoTen": "Đặng Phúc Lê Nhât",
    "NgaySinh": "02/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.60",
    "Anh": "6.00",
    "Van": "6.00",
    "MonChuyen": "6.75",
    "TongDiem": "28.73"
  },
  {
    "SBD": "251077",
    "HoTen": "Nguyễn Hữu Long Nhật",
    "NgaySinh": "21/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.20",
    "Anh": "6.75",
    "Van": "6.00",
    "MonChuyen": "6.00",
    "TongDiem": "27.95"
  },
  {
    "SBD": "251078",
    "HoTen": "Nguyễn Công Nguyên Phát",
    "NgaySinh": "29/05/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.30",
    "Anh": "5.75",
    "Van": "5.00",
    "MonChuyen": "5.50",
    "TongDiem": "24.30"
  },
  {
    "SBD": "251079",
    "HoTen": "Nguyễn Hoàng Phát",
    "NgaySinh": "12/05/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.80",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "12.25",
    "TongDiem": "41.93"
  },
  {
    "SBD": "251080",
    "HoTen": "Luyện Khánh Phong",
    "NgaySinh": "29/06/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.50",
    "Anh": "9.25",
    "Van": "5.00",
    "MonChuyen": "11.25",
    "TongDiem": "39.63"
  },
  {
    "SBD": "251081",
    "HoTen": "Trần Bảo Phú",
    "NgaySinh": "06/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.70",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "12.00",
    "TongDiem": "42.45"
  },
  {
    "SBD": "251082",
    "HoTen": "Nguyễn Lương Phúc",
    "NgaySinh": "20/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.30",
    "Anh": "7.25",
    "Van": "7.50",
    "MonChuyen": "10.75",
    "TongDiem": "38.18"
  },
  {
    "SBD": "251083",
    "HoTen": "Hồ Mai Phương",
    "NgaySinh": "06/04/2010",
    "Chuyen": "Vật lí",
    "Toan": "9.10",
    "Anh": "9.00",
    "Van": "7.75",
    "MonChuyen": "14.25",
    "TongDiem": "47.23"
  },
  {
    "SBD": "251084",
    "HoTen": "Trần Thị Mai Phương",
    "NgaySinh": "12/08/2010",
    "Chuyen": "Vật lí",
    "Toan": "4.60",
    "Anh": "3.75",
    "Van": "7.00",
    "MonChuyen": "4.25",
    "TongDiem": "21.73"
  },
  {
    "SBD": "251085",
    "HoTen": "Lê Tiến Quang",
    "NgaySinh": "29/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.60",
    "Anh": "8.75",
    "Van": "7.00",
    "MonChuyen": "5.25",
    "TongDiem": "31.23"
  },
  {
    "SBD": "251086",
    "HoTen": "Đinh Văn Quyết",
    "NgaySinh": "04/02/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.00",
    "Anh": "4.25",
    "Van": "6.00",
    "MonChuyen": "2.00",
    "TongDiem": "19.25"
  },
  {
    "SBD": "251087",
    "HoTen": "Trần Hải Quỳnh",
    "NgaySinh": "31/08/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.00",
    "Anh": "8.25",
    "Van": "7.75",
    "MonChuyen": "14.50",
    "TongDiem": "45.75"
  },
  {
    "SBD": "251088",
    "HoTen": "Nguyễn Hoàng Sang",
    "NgaySinh": "04/11/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.20",
    "Anh": "8.00",
    "Van": "7.50",
    "MonChuyen": "4.25",
    "TongDiem": "29.08"
  },
  {
    "SBD": "251089",
    "HoTen": "Nguyễn Viết Đức Sáng",
    "NgaySinh": "10/02/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.60",
    "Anh": "5.50",
    "Van": "6.75",
    "MonChuyen": "7.50",
    "TongDiem": "30.10"
  },
  {
    "SBD": "251090",
    "HoTen": "Hồ Xuân Sơn",
    "NgaySinh": "07/07/2010",
    "Chuyen": "Vật lí",
    "Toan": "4.50",
    "Anh": "5.50",
    "Van": "0.0",
    "MonChuyen": "0.0",
    "TongDiem": "0.0"
  },
  {
    "SBD": "251091",
    "HoTen": "Lê Bảo Sơn",
    "NgaySinh": "11/10/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.10",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "14.25",
    "TongDiem": "44.48"
  },
  {
    "SBD": "251092",
    "HoTen": "Nguyễn Tất Sơn",
    "NgaySinh": "13/08/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.20",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "5.25",
    "TongDiem": "26.58"
  },
  {
    "SBD": "251093",
    "HoTen": "Nguyễn Quốc Thắng",
    "NgaySinh": "13/12/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.50",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "9.50",
    "TongDiem": "37.75"
  },
  {
    "SBD": "251094",
    "HoTen": "Vũ Tiến Thành",
    "NgaySinh": "07/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.80",
    "Anh": "8.50",
    "Van": "6.25",
    "MonChuyen": "4.25",
    "TongDiem": "26.93"
  },
  {
    "SBD": "251095",
    "HoTen": "Nguyễn Thị Như Thảo",
    "NgaySinh": "07/08/2010",
    "Chuyen": "Vật lí",
    "Toan": "8.00",
    "Anh": "6.75",
    "Van": "6.00",
    "MonChuyen": "5.00",
    "TongDiem": "28.25"
  },
  {
    "SBD": "251096",
    "HoTen": "Nguyễn Ngọc Thọ",
    "NgaySinh": "29/06/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.80",
    "Anh": "2.75",
    "Van": "5.50",
    "MonChuyen": "6.25",
    "TongDiem": "24.43"
  },
  {
    "SBD": "251097",
    "HoTen": "Dương Võ Bảo Thư",
    "NgaySinh": "11/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.20",
    "Anh": "8.50",
    "Van": "6.50",
    "MonChuyen": "4.50",
    "TongDiem": "28.95"
  },
  {
    "SBD": "251098",
    "HoTen": "Nguyễn Hồ Thương",
    "NgaySinh": "10/11/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.00",
    "Anh": "6.75",
    "Van": "6.50",
    "MonChuyen": "4.50",
    "TongDiem": "26.00"
  },
  {
    "SBD": "251099",
    "HoTen": "Ngô Trí Toàn",
    "NgaySinh": "09/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "4.50",
    "Anh": "4.75",
    "Van": "6.00",
    "MonChuyen": "3.25",
    "TongDiem": "20.13"
  },
  {
    "SBD": "251100",
    "HoTen": "Nguyễn Đức Trọng",
    "NgaySinh": "15/01/2010",
    "Chuyen": "Vật lí",
    "Toan": "6.70",
    "Anh": "7.75",
    "Van": "6.50",
    "MonChuyen": "10.50",
    "TongDiem": "36.70"
  },
  {
    "SBD": "251101",
    "HoTen": "Lê Quốc Trung",
    "NgaySinh": "07/11/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.60",
    "Anh": "7.50",
    "Van": "6.50",
    "MonChuyen": "13.00",
    "TongDiem": "41.10"
  },
  {
    "SBD": "251102",
    "HoTen": "Phan Hoàng Tuấn",
    "NgaySinh": "01/03/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.30",
    "Anh": "9.00",
    "Van": "7.50",
    "MonChuyen": "7.25",
    "TongDiem": "34.68"
  },
  {
    "SBD": "251103",
    "HoTen": "Hoàng Việt",
    "NgaySinh": "21/12/2010",
    "Chuyen": "Vật lí",
    "Toan": "5.40",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "4.75",
    "TongDiem": "27.78"
  },
  {
    "SBD": "251104",
    "HoTen": "Võ Hùng Vương",
    "NgaySinh": "19/04/2010",
    "Chuyen": "Vật lí",
    "Toan": "7.90",
    "Anh": "8.50",
    "Van": "8.00",
    "MonChuyen": "11.25",
    "TongDiem": "41.28"
  },
  {
    "SBD": "251105",
    "HoTen": "Nguyễn Trường An",
    "NgaySinh": "23/01/2010",
    "Chuyen": "Sinh học",
    "Toan": "7.30",
    "Anh": "6.25",
    "Van": "7.50",
    "MonChuyen": "5.75",
    "TongDiem": "29.68"
  },
  {
    "SBD": "251106",
    "HoTen": "Trần Thị Khánh An",
    "NgaySinh": "18/04/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.20",
    "Anh": "9.00",
    "Van": "7.75",
    "MonChuyen": "12.75",
    "TongDiem": "42.08"
  },
  {
    "SBD": "251107",
    "HoTen": "Bùi Trần Kiều Anh",
    "NgaySinh": "26/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.30",
    "Anh": "9.25",
    "Van": "8.00",
    "MonChuyen": "13.25",
    "TongDiem": "42.43"
  },
  {
    "SBD": "251108",
    "HoTen": "Nguyễn Thị Việt Anh",
    "NgaySinh": "15/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.10",
    "Anh": "3.75",
    "Van": "7.75",
    "MonChuyen": "5.00",
    "TongDiem": "24.10"
  },
  {
    "SBD": "251109",
    "HoTen": "Vũ Kim Anh",
    "NgaySinh": "13/09/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.80",
    "Anh": "8.75",
    "Van": "6.75",
    "MonChuyen": "8.00",
    "TongDiem": "32.30"
  },
  {
    "SBD": "251110",
    "HoTen": "Trần Phúc Bách",
    "NgaySinh": "21/03/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.60",
    "Anh": "4.00",
    "Van": "7.25",
    "MonChuyen": "9.75",
    "TongDiem": "31.48"
  },
  {
    "SBD": "251111",
    "HoTen": "Nguyễn Chiêu Ban",
    "NgaySinh": "09/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "3.00",
    "Anh": "7.25",
    "Van": "4.25",
    "MonChuyen": "3.00",
    "TongDiem": "19.00"
  },
  {
    "SBD": "251112",
    "HoTen": "Đinh Văn Gia Bảo",
    "NgaySinh": "21/07/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.70",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "15.00",
    "TongDiem": "45.20"
  },
  {
    "SBD": "251113",
    "HoTen": "Nguyễn Gia Bảo",
    "NgaySinh": "07/07/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.00",
    "Anh": "5.00",
    "Van": "7.25",
    "MonChuyen": "8.25",
    "TongDiem": "29.63"
  },
  {
    "SBD": "251114",
    "HoTen": "Trần Khánh Chi",
    "NgaySinh": "08/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.50",
    "Anh": "7.25",
    "Van": "7.50",
    "MonChuyen": "14.75",
    "TongDiem": "41.38"
  },
  {
    "SBD": "251115",
    "HoTen": "Ngô Đức Chuẩn",
    "NgaySinh": "06/05/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.60",
    "Anh": "6.50",
    "Van": "6.75",
    "MonChuyen": "4.75",
    "TongDiem": "25.98"
  },
  {
    "SBD": "251116",
    "HoTen": "Nguyễn Thảo Đan",
    "NgaySinh": "05/07/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.30",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "15.00",
    "TongDiem": "43.30"
  },
  {
    "SBD": "251117",
    "HoTen": "Nguyễn Trần Linh Đan",
    "NgaySinh": "28/01/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.10",
    "Anh": "8.50",
    "Van": "7.50",
    "MonChuyen": "12.50",
    "TongDiem": "39.85"
  },
  {
    "SBD": "251118",
    "HoTen": "Chu Hoàng Đức",
    "NgaySinh": "02/08/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.80",
    "Anh": "3.50",
    "Van": "5.50",
    "MonChuyen": "6.00",
    "TongDiem": "23.80"
  },
  {
    "SBD": "251119",
    "HoTen": "Lê Anh Đức",
    "NgaySinh": "29/06/2010",
    "Chuyen": "Sinh học",
    "Toan": "7.70",
    "Anh": "5.25",
    "Van": "6.75",
    "MonChuyen": "13.25",
    "TongDiem": "39.58"
  },
  {
    "SBD": "251120",
    "HoTen": "Hoàng Thế Dũng",
    "NgaySinh": "20/04/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.20",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "17.25",
    "TongDiem": "44.08"
  },
  {
    "SBD": "251121",
    "HoTen": "Doãn Tùng Dương",
    "NgaySinh": "21/09/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.40",
    "Anh": "5.25",
    "Van": "6.00",
    "MonChuyen": "10.75",
    "TongDiem": "32.78"
  },
  {
    "SBD": "251122",
    "HoTen": "Hồ Lê Hoài Giang",
    "NgaySinh": "11/04/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.40",
    "Anh": "6.25",
    "Van": "6.25",
    "MonChuyen": "15.25",
    "TongDiem": "39.78"
  },
  {
    "SBD": "251123",
    "HoTen": "Nguyễn Đặng Khánh Hà",
    "NgaySinh": "07/05/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.00",
    "Anh": "5.25",
    "Van": "5.75",
    "MonChuyen": "12.00",
    "TongDiem": "35.00"
  },
  {
    "SBD": "251124",
    "HoTen": "Đặng Cao Hoàng Hà",
    "NgaySinh": "09/07/2010",
    "Chuyen": "Sinh học",
    "Toan": "3.90",
    "Anh": "5.00",
    "Van": "5.50",
    "MonChuyen": "14.50",
    "TongDiem": "36.15"
  },
  {
    "SBD": "251125",
    "HoTen": "Vũ Ngọc Bảo Hân",
    "NgaySinh": "16/07/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.30",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "6.50",
    "TongDiem": "28.80"
  },
  {
    "SBD": "251126",
    "HoTen": "Lê Đức Hiếu",
    "NgaySinh": "02/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.90",
    "Anh": "7.25",
    "Van": "6.00",
    "MonChuyen": "11.75",
    "TongDiem": "37.78"
  },
  {
    "SBD": "251127",
    "HoTen": "Lê Việt Hoàng",
    "NgaySinh": "13/08/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.60",
    "Anh": "5.75",
    "Van": "5.75",
    "MonChuyen": "13.25",
    "TongDiem": "36.98"
  },
  {
    "SBD": "251129",
    "HoTen": "Bùi Anh Gia Hưng",
    "NgaySinh": "04/00/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.80",
    "Anh": "7.25",
    "Van": "6.75",
    "MonChuyen": "11.00",
    "TongDiem": "35.30"
  },
  {
    "SBD": "251131",
    "HoTen": "Đặng Gia Huy",
    "NgaySinh": "19/04/2025",
    "Chuyen": "Sinh học",
    "Toan": "5.80",
    "Anh": "5.50",
    "Van": "6.25",
    "MonChuyen": "12.25",
    "TongDiem": "35.93"
  },
  {
    "SBD": "251132",
    "HoTen": "Lê Văn Hoàng Huy",
    "NgaySinh": "02/12/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.00",
    "Anh": "4.50",
    "Van": "7.25",
    "MonChuyen": "9.50",
    "TongDiem": "30.00"
  },
  {
    "SBD": "251133",
    "HoTen": "Trần Nhật Huy",
    "NgaySinh": "28/11/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.80",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "7.25",
    "TongDiem": "30.43"
  },
  {
    "SBD": "251134",
    "HoTen": "Bùi Nguyễn Gia Khánh",
    "NgaySinh": "28/12/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.20",
    "Anh": "8.00",
    "Van": "7.75",
    "MonChuyen": "14.50",
    "TongDiem": "43.70"
  },
  {
    "SBD": "251135",
    "HoTen": "Nguyễn Tư Khôi",
    "NgaySinh": "13/07/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.70",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "8.25",
    "TongDiem": "33.33"
  },
  {
    "SBD": "251136",
    "HoTen": "Nguyễn Nhật Khương",
    "NgaySinh": "27/04/2010",
    "Chuyen": "Sinh học",
    "Toan": "7.50",
    "Anh": "9.00",
    "Van": "6.75",
    "MonChuyen": "15.00",
    "TongDiem": "45.75"
  },
  {
    "SBD": "251137",
    "HoTen": "Ngô Văn Lâm",
    "NgaySinh": "02/11/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.60",
    "Anh": "5.00",
    "Van": "6.50",
    "MonChuyen": "12.50",
    "TongDiem": "35.85"
  },
  {
    "SBD": "251138",
    "HoTen": "Trần Thị Tuệ Lâm",
    "NgaySinh": "27/01/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.10",
    "Anh": "5.50",
    "Van": "7.00",
    "MonChuyen": "3.25",
    "TongDiem": "22.48"
  },
  {
    "SBD": "251139",
    "HoTen": "Bùi Hà Linh",
    "NgaySinh": "03/07/2010",
    "Chuyen": "Sinh học",
    "Toan": "7.40",
    "Anh": "5.50",
    "Van": "7.00",
    "MonChuyen": "15.50",
    "TongDiem": "43.15"
  },
  {
    "SBD": "251140",
    "HoTen": "Nguyễn Tùng Linh",
    "NgaySinh": "16/01/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.90",
    "Anh": "6.75",
    "Van": "7.25",
    "MonChuyen": "12.75",
    "TongDiem": "40.03"
  },
  {
    "SBD": "251141",
    "HoTen": "Hoàng Khánh Lộc",
    "NgaySinh": "07/04/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.20",
    "Anh": "6.75",
    "Van": "7.00",
    "MonChuyen": "16.00",
    "TongDiem": "42.95"
  },
  {
    "SBD": "251142",
    "HoTen": "Hồ Như Mai",
    "NgaySinh": "14/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.40",
    "Anh": "5.75",
    "Van": "7.50",
    "MonChuyen": "11.75",
    "TongDiem": "36.28"
  },
  {
    "SBD": "251143",
    "HoTen": "Nguyễn Tất Nhật Minh",
    "NgaySinh": "11/05/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.00",
    "Anh": "8.50",
    "Van": "6.50",
    "MonChuyen": "13.25",
    "TongDiem": "39.88"
  },
  {
    "SBD": "251144",
    "HoTen": "Lê Nguyễn Hoàng Nam",
    "NgaySinh": "02/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "7.00",
    "Anh": "6.75",
    "Van": "6.50",
    "MonChuyen": "13.50",
    "TongDiem": "40.50"
  },
  {
    "SBD": "251145",
    "HoTen": "Nguyễn Thành Nam",
    "NgaySinh": "08/07/2010",
    "Chuyen": "Sinh học",
    "Toan": "7.00",
    "Anh": "8.75",
    "Van": "6.50",
    "MonChuyen": "14.50",
    "TongDiem": "44.00"
  },
  {
    "SBD": "251146",
    "HoTen": "Nguyễn Quỳnh Nga",
    "NgaySinh": "30/08/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.30",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "8.25",
    "TongDiem": "31.18"
  },
  {
    "SBD": "251147",
    "HoTen": "Lê Hà Ngân",
    "NgaySinh": "04/03/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.50",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "14.00",
    "TongDiem": "41.00"
  },
  {
    "SBD": "251148",
    "HoTen": "Lê Trần Khánh Ngọc",
    "NgaySinh": "12/03/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.20",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "10.50",
    "TongDiem": "33.45"
  },
  {
    "SBD": "251149",
    "HoTen": "Phạm Đình Nguyên",
    "NgaySinh": "10/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.80",
    "Anh": "5.50",
    "Van": "7.75",
    "MonChuyen": "19.50",
    "TongDiem": "47.30"
  },
  {
    "SBD": "251150",
    "HoTen": "Phan Khôi Nguyên",
    "NgaySinh": "07/07/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.20",
    "Anh": "7.25",
    "Van": "6.75",
    "MonChuyen": "12.50",
    "TongDiem": "36.95"
  },
  {
    "SBD": "251151",
    "HoTen": "Ngô Minh Nhật",
    "NgaySinh": "09/12/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.40",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "12.00",
    "TongDiem": "39.65"
  },
  {
    "SBD": "251152",
    "HoTen": "Nguyễn Bảo Nhi",
    "NgaySinh": "10/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.40",
    "Anh": "8.75",
    "Van": "7.75",
    "MonChuyen": "9.25",
    "TongDiem": "34.78"
  },
  {
    "SBD": "251153",
    "HoTen": "Nguyễn Nam Phong",
    "NgaySinh": "21/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "2.60",
    "Anh": "3.50",
    "Van": "6.75",
    "MonChuyen": "9.25",
    "TongDiem": "26.73"
  },
  {
    "SBD": "251154",
    "HoTen": "Nguyễn Văn Hoàng Phúc",
    "NgaySinh": "21/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "3.20",
    "Anh": "6.75",
    "Van": "7.75",
    "MonChuyen": "8.00",
    "TongDiem": "29.70"
  },
  {
    "SBD": "251155",
    "HoTen": "Nguyên Minh Quân",
    "NgaySinh": "02/08/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.60",
    "Anh": "5.00",
    "Van": "7.00",
    "MonChuyen": "14.00",
    "TongDiem": "37.60"
  },
  {
    "SBD": "251156",
    "HoTen": "Nguyễn Minh Quân",
    "NgaySinh": "22/05/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.40",
    "Anh": "6.25",
    "Van": "6.75",
    "MonChuyen": "8.50",
    "TongDiem": "32.15"
  },
  {
    "SBD": "251157",
    "HoTen": "Nguyễn Tiến Quân",
    "NgaySinh": "20/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.60",
    "Anh": "6.00",
    "Van": "6.75",
    "MonChuyen": "14.25",
    "TongDiem": "39.73"
  },
  {
    "SBD": "251158",
    "HoTen": "Võ Huy Quân",
    "NgaySinh": "15/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "3.60",
    "Anh": "5.50",
    "Van": "0.0",
    "MonChuyen": "0.0",
    "TongDiem": "0.0"
  },
  {
    "SBD": "251159",
    "HoTen": "Trần Đình Quang",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.60",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "17.00",
    "TongDiem": "46.35"
  },
  {
    "SBD": "251160",
    "HoTen": "Hoàng Lưu Thuý Quỳnh",
    "NgaySinh": "01/08/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.80",
    "Anh": "8.75",
    "Van": "7.50",
    "MonChuyen": "10.75",
    "TongDiem": "38.18"
  },
  {
    "SBD": "251161",
    "HoTen": "Nguyễn Thị Lê Quỳnh",
    "NgaySinh": "09/11/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.60",
    "Anh": "7.75",
    "Van": "6.50",
    "MonChuyen": "7.25",
    "TongDiem": "30.73"
  },
  {
    "SBD": "251162",
    "HoTen": "Nguyễn Thị Huyền Tâm",
    "NgaySinh": "22/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.60",
    "Anh": "8.25",
    "Van": "6.25",
    "MonChuyen": "12.00",
    "TongDiem": "38.10"
  },
  {
    "SBD": "251163",
    "HoTen": "Nguyễn Quốc Thái",
    "NgaySinh": "25/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.00",
    "Anh": "8.25",
    "Van": "6.00",
    "MonChuyen": "14.75",
    "TongDiem": "42.38"
  },
  {
    "SBD": "251164",
    "HoTen": "Nguyễn Viết Thái",
    "NgaySinh": "27/08/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.20",
    "Anh": "5.25",
    "Van": "6.50",
    "MonChuyen": "11.75",
    "TongDiem": "34.58"
  },
  {
    "SBD": "251165",
    "HoTen": "Nguyễn Chân Nhật Thành",
    "NgaySinh": "17/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.60",
    "Anh": "7.00",
    "Van": "7.00",
    "MonChuyen": "11.75",
    "TongDiem": "36.23"
  },
  {
    "SBD": "251166",
    "HoTen": "Nguyễn Thị Thạch Thảo",
    "NgaySinh": "24/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.90",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "13.00",
    "TongDiem": "40.40"
  },
  {
    "SBD": "251167",
    "HoTen": "Lê Thị Thiết",
    "NgaySinh": "30/03/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.40",
    "Anh": "7.50",
    "Van": "7.25",
    "MonChuyen": "15.25",
    "TongDiem": "44.03"
  },
  {
    "SBD": "251168",
    "HoTen": "Nguyễn Văn Thinh",
    "NgaySinh": "18/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.80",
    "Anh": "6.50",
    "Van": "7.25",
    "MonChuyen": "13.00",
    "TongDiem": "39.05"
  },
  {
    "SBD": "251169",
    "HoTen": "Hoàng Thông",
    "NgaySinh": "28/11/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.30",
    "Anh": "9.50",
    "Van": "7.00",
    "MonChuyen": "14.25",
    "TongDiem": "44.18"
  },
  {
    "SBD": "251170",
    "HoTen": "Lữ Thị Hoàng Thu",
    "NgaySinh": "17/08/2010",
    "Chuyen": "Sinh học",
    "Toan": "3.60",
    "Anh": "3.25",
    "Van": "6.25",
    "MonChuyen": "5.00",
    "TongDiem": "20.60"
  },
  {
    "SBD": "251171",
    "HoTen": "Lê Ngọc Huyền Thư",
    "NgaySinh": "10/08/2010",
    "Chuyen": "Sinh học",
    "Toan": "7.40",
    "Anh": "8.00",
    "Van": "7.50",
    "MonChuyen": "16.25",
    "TongDiem": "47.28"
  },
  {
    "SBD": "251172",
    "HoTen": "Phạm Lê Anh Thư",
    "NgaySinh": "07/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.50",
    "Anh": "8.75",
    "Van": "7.25",
    "MonChuyen": "9.00",
    "TongDiem": "36.00"
  },
  {
    "SBD": "251173",
    "HoTen": "Đậu Mai Thuỳ",
    "NgaySinh": "23/10/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.50",
    "Anh": "6.25",
    "Van": "7.75",
    "MonChuyen": "13.25",
    "TongDiem": "39.38"
  },
  {
    "SBD": "251174",
    "HoTen": "Trần Thị Quỳnh Trang",
    "NgaySinh": "20/12/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.10",
    "Anh": "7.00",
    "Van": "6.58",
    "MonChuyen": "14.50",
    "TongDiem": "41.43"
  },
  {
    "SBD": "251175",
    "HoTen": "Nguyễn Tiến Trình",
    "NgaySinh": "13/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "6.60",
    "Anh": "8.00",
    "Van": "6.25",
    "MonChuyen": "16.50",
    "TongDiem": "45.60"
  },
  {
    "SBD": "251176",
    "HoTen": "Nguyễn Văn Tuấn Tú",
    "NgaySinh": "02/11/2010",
    "Chuyen": "Sinh học",
    "Toan": "8.30",
    "Anh": "9.00",
    "Van": "6.25",
    "MonChuyen": "13.25",
    "TongDiem": "43.43"
  },
  {
    "SBD": "251177",
    "HoTen": "Hoàng Minh Tuấn",
    "NgaySinh": "16/02/2010",
    "Chuyen": "Sinh học",
    "Toan": "8.00",
    "Anh": "7.00",
    "Van": "7.25",
    "MonChuyen": "17.00",
    "TongDiem": "47.75"
  },
  {
    "SBD": "251178",
    "HoTen": "Nguyễn Thanh Uyên",
    "NgaySinh": "31/08/2010",
    "Chuyen": "Sinh học",
    "Toan": "8.20",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "16.25",
    "TongDiem": "49.33"
  },
  {
    "SBD": "251179",
    "HoTen": "Phan Phương Uyên",
    "NgaySinh": "28/01/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.80",
    "Anh": "8.50",
    "Van": "6.75",
    "MonChuyen": "11.50",
    "TongDiem": "38.30"
  },
  {
    "SBD": "251180",
    "HoTen": "Hoàng Anh Vinh",
    "NgaySinh": "03/11/2010",
    "Chuyen": "Sinh học",
    "Toan": "4.50",
    "Anh": "8.00",
    "Van": "6.25",
    "MonChuyen": "11.75",
    "TongDiem": "36.38"
  },
  {
    "SBD": "251181",
    "HoTen": "Lê Tường Vy",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Sinh học",
    "Toan": "3.70",
    "Anh": "6.50",
    "Van": "7.00",
    "MonChuyen": "12.25",
    "TongDiem": "35.58"
  },
  {
    "SBD": "251182",
    "HoTen": "Nguyễn Thị Hải Yến",
    "NgaySinh": "15/03/2010",
    "Chuyen": "Sinh học",
    "Toan": "5.50",
    "Anh": "7.00",
    "Van": "7.50",
    "MonChuyen": "14.75",
    "TongDiem": "42.13"
  },
  {
    "SBD": "251183",
    "HoTen": "Nguyễn Đình An",
    "NgaySinh": "04/01/2010",
    "Chuyen": "Tin học",
    "Toan": "4.40",
    "Anh": "4.25",
    "Van": "6.00",
    "MonChuyen": "3.00",
    "TongDiem": "19.15"
  },
  {
    "SBD": "251184",
    "HoTen": "Nguyễn Phước An",
    "NgaySinh": "16/12/2010",
    "Chuyen": "Tin học",
    "Toan": "5.90",
    "Anh": "5.75",
    "Van": "6.75",
    "MonChuyen": "1.25",
    "TongDiem": "20.28"
  },
  {
    "SBD": "251185",
    "HoTen": "Võ Văn An",
    "NgaySinh": "05/05/2010",
    "Chuyen": "Tin học",
    "Toan": "8.00",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "15.25",
    "TongDiem": "45.88"
  },
  {
    "SBD": "251186",
    "HoTen": "Trần Ngọc Thiên Ân",
    "NgaySinh": "07/09/2010",
    "Chuyen": "Tin học",
    "Toan": "5.30",
    "Anh": "7.00",
    "Van": "6.25",
    "MonChuyen": "0",
    "TongDiem": "18.55"
  },
  {
    "SBD": "251189",
    "HoTen": "Trần Ngọc Ánh",
    "NgaySinh": "03/03/2010",
    "Chuyen": "Tin học",
    "Toan": "5.30",
    "Anh": "6.50",
    "Van": "5.50",
    "MonChuyen": "6.00",
    "TongDiem": "26.30"
  },
  {
    "SBD": "251190",
    "HoTen": "Đặng Gia Bảo",
    "NgaySinh": "01/06/2010",
    "Chuyen": "Tin học",
    "Toan": "6.40",
    "Anh": "7.50",
    "Van": "7.00",
    "MonChuyen": "11.25",
    "TongDiem": "37.78"
  },
  {
    "SBD": "251191",
    "HoTen": "Lê Nguyên Bảo",
    "NgaySinh": "02/11/2010",
    "Chuyen": "Tin học",
    "Toan": "7.40",
    "Anh": "8.25",
    "Van": "6.25",
    "MonChuyen": "12.00",
    "TongDiem": "39.90"
  },
  {
    "SBD": "251192",
    "HoTen": "Nguyễn Duy Gia Bảo",
    "NgaySinh": "16/09/2010",
    "Chuyen": "Tin học",
    "Toan": "5.60",
    "Anh": "9.75",
    "Van": "6.75",
    "MonChuyen": "7.00",
    "TongDiem": "32.60"
  },
  {
    "SBD": "251193",
    "HoTen": "Trần Văn Quốc Bảo",
    "NgaySinh": "10/08/2010",
    "Chuyen": "Tin học",
    "Toan": "6.40",
    "Anh": "9.25",
    "Van": "7.50",
    "MonChuyen": "2.00",
    "TongDiem": "26.15"
  },
  {
    "SBD": "251194",
    "HoTen": "Trần Xuyến Chi",
    "NgaySinh": "31/10/2010",
    "Chuyen": "Tin học",
    "Toan": "7.10",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "4.25",
    "TongDiem": "29.73"
  },
  {
    "SBD": "251195",
    "HoTen": "Nguyễn Xuân Trung Cường",
    "NgaySinh": "22/02/2010",
    "Chuyen": "Tin học",
    "Toan": "7.20",
    "Anh": "7.25",
    "Van": "7.25",
    "MonChuyen": "11.75",
    "TongDiem": "39.33"
  },
  {
    "SBD": "251196",
    "HoTen": "Trần Minh Đức",
    "NgaySinh": "30/09/2010",
    "Chuyen": "Tin học",
    "Toan": "7.30",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "10.25",
    "TongDiem": "38.18"
  },
  {
    "SBD": "251197",
    "HoTen": "Võ Quang Đức",
    "NgaySinh": "07/02/2010",
    "Chuyen": "Tin học",
    "Toan": "5.50",
    "Anh": "8.25",
    "Van": "7.00",
    "MonChuyen": "6.75",
    "TongDiem": "30.88"
  },
  {
    "SBD": "251198",
    "HoTen": "Lê Lâm Dũng",
    "NgaySinh": "18/03/2010",
    "Chuyen": "Tin học",
    "Toan": "6.70",
    "Anh": "7.00",
    "Van": "6.50",
    "MonChuyen": "11.75",
    "TongDiem": "37.83"
  },
  {
    "SBD": "251199",
    "HoTen": "Vương Đình Dũng",
    "NgaySinh": "08/07/2010",
    "Chuyen": "Tin học",
    "Toan": "7.00",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "11.75",
    "TongDiem": "39.88"
  },
  {
    "SBD": "251200",
    "HoTen": "Vũ Văn Hải",
    "NgaySinh": "03/07/2010",
    "Chuyen": "Tin học",
    "Toan": "5.30",
    "Anh": "6.25",
    "Van": "7.75",
    "MonChuyen": "15.00",
    "TongDiem": "41.80"
  },
  {
    "SBD": "251201",
    "HoTen": "Thái Việt Hiếu",
    "NgaySinh": "23/07/2010",
    "Chuyen": "Tin học",
    "Toan": "5.80",
    "Anh": "6.75",
    "Van": "5.75",
    "MonChuyen": "14.00",
    "TongDiem": "39.30"
  },
  {
    "SBD": "251202",
    "HoTen": "Trần Duy Hoàn",
    "NgaySinh": "02/03/2010",
    "Chuyen": "Tin học",
    "Toan": "7.20",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "10.75",
    "TongDiem": "39.08"
  },
  {
    "SBD": "251203",
    "HoTen": "Nguyễn Huy Hoàng",
    "NgaySinh": "14/11/2010",
    "Chuyen": "Tin học",
    "Toan": "5.90",
    "Anh": "8.00",
    "Van": "7.00",
    "MonChuyen": "4.25",
    "TongDiem": "27.28"
  },
  {
    "SBD": "251204",
    "HoTen": "Đặng Thái Hưng",
    "NgaySinh": "13/08/2010",
    "Chuyen": "Tin học",
    "Toan": "5.10",
    "Anh": "6.75",
    "Van": "6.25",
    "MonChuyen": "0.25",
    "TongDiem": "18.48"
  },
  {
    "SBD": "251205",
    "HoTen": "Nguyễn Khánh Hưng",
    "NgaySinh": "30/11/2010",
    "Chuyen": "Tin học",
    "Toan": "6.00",
    "Anh": "8.25",
    "Van": "6.50",
    "MonChuyen": "5.50",
    "TongDiem": "29.00"
  },
  {
    "SBD": "251206",
    "HoTen": "Nguyễn Tiến Hưng",
    "NgaySinh": "16/08/2010",
    "Chuyen": "Tin học",
    "Toan": "4.30",
    "Anh": "6.50",
    "Van": "5.00",
    "MonChuyen": "4.00",
    "TongDiem": "21.80"
  },
  {
    "SBD": "251207",
    "HoTen": "Đào Quang Khải",
    "NgaySinh": "30/11/2010",
    "Chuyen": "Tin học",
    "Toan": "4.90",
    "Anh": "7.50",
    "Van": "6.50",
    "MonChuyen": "9.00",
    "TongDiem": "32.40"
  },
  {
    "SBD": "251209",
    "HoTen": "Chu Minh Khánh",
    "NgaySinh": "03/04/2010",
    "Chuyen": "Tin học",
    "Toan": "7.00",
    "Anh": "6.25",
    "Van": "7.75",
    "MonChuyen": "14.00",
    "TongDiem": "42.00"
  },
  {
    "SBD": "251211",
    "HoTen": "Lã Thị Vân Khánh",
    "NgaySinh": "16/05/2010",
    "Chuyen": "Tin học",
    "Toan": "7.60",
    "Anh": "8.25",
    "Van": "6.00",
    "MonChuyen": "10.50",
    "TongDiem": "37.60"
  },
  {
    "SBD": "251212",
    "HoTen": "Nguyễn Công Khánh",
    "NgaySinh": "31/03/2010",
    "Chuyen": "Tin học",
    "Toan": "5.50",
    "Anh": "6.25",
    "Van": "6.00",
    "MonChuyen": "8.25",
    "TongDiem": "30.13"
  },
  {
    "SBD": "251213",
    "HoTen": "Nguyễn Sỹ Khánh",
    "NgaySinh": "17/05/2010",
    "Chuyen": "Tin học",
    "Toan": "5.90",
    "Anh": "9.25",
    "Van": "6.25",
    "MonChuyen": "4.75",
    "TongDiem": "28.53"
  },
  {
    "SBD": "251214",
    "HoTen": "Trần Văn Đăng Khoa",
    "NgaySinh": "10/02/2010",
    "Chuyen": "Tin học",
    "Toan": "5.70",
    "Anh": "6.00",
    "Van": "7.00",
    "MonChuyen": "6.75",
    "TongDiem": "28.83"
  },
  {
    "SBD": "251215",
    "HoTen": "Đậu Đăng Khôi",
    "NgaySinh": "20/09/2010",
    "Chuyen": "Tin học",
    "Toan": "8.40",
    "Anh": "9.50",
    "Van": "6.50",
    "MonChuyen": "18.50",
    "TongDiem": "52.15"
  },
  {
    "SBD": "251216",
    "HoTen": "Phạm Đình Nguyên Khôi",
    "NgaySinh": "04/02/2010",
    "Chuyen": "Tin học",
    "Toan": "5.50",
    "Anh": "9.75",
    "Van": "6.00",
    "MonChuyen": "11.75",
    "TongDiem": "38.88"
  },
  {
    "SBD": "251217",
    "HoTen": "Nguyễn Đức Kiên",
    "NgaySinh": "11/07/2010",
    "Chuyen": "Tin học",
    "Toan": "7.50",
    "Anh": "9.25",
    "Van": "7.00",
    "MonChuyen": "5.50",
    "TongDiem": "32.00"
  },
  {
    "SBD": "251218",
    "HoTen": "Trần Quang Kiệt",
    "NgaySinh": "12/05/2010",
    "Chuyen": "Tin học",
    "Toan": "6.10",
    "Anh": "8.50",
    "Van": "6.50",
    "MonChuyen": "8.25",
    "TongDiem": "33.48"
  },
  {
    "SBD": "251219",
    "HoTen": "Nguyễn Quang Lâm",
    "NgaySinh": "20/07/2010",
    "Chuyen": "Tin học",
    "Toan": "7.50",
    "Anh": "6.00",
    "Van": "6.25",
    "MonChuyen": "2.25",
    "TongDiem": "23.13"
  },
  {
    "SBD": "251220",
    "HoTen": "Phạm Tùng Lâm",
    "NgaySinh": "05/01/2010",
    "Chuyen": "Tin học",
    "Toan": "6.70",
    "Anh": "8.50",
    "Van": "7.00",
    "MonChuyen": "3.75",
    "TongDiem": "27.83"
  },
  {
    "SBD": "251221",
    "HoTen": "Hoàng Đình Lộc",
    "NgaySinh": "13/01/2010",
    "Chuyen": "Tin học",
    "Toan": "6.20",
    "Anh": "7.00",
    "Van": "7.50",
    "MonChuyen": "11.75",
    "TongDiem": "38.33"
  },
  {
    "SBD": "251222",
    "HoTen": "Lê Hữu Đình Long",
    "NgaySinh": "01/01/2010",
    "Chuyen": "Tin học",
    "Toan": "6.00",
    "Anh": "9.75",
    "Van": "6.75",
    "MonChuyen": "14.00",
    "TongDiem": "43.50"
  },
  {
    "SBD": "251223",
    "HoTen": "Lê Đình Mạnh",
    "NgaySinh": "04/01/2010",
    "Chuyen": "Tin học",
    "Toan": "7.80",
    "Anh": "9.00",
    "Van": "7.25",
    "MonChuyen": "11.00",
    "TongDiem": "40.55"
  },
  {
    "SBD": "251224",
    "HoTen": "Nguyễn Đức Mạnh",
    "NgaySinh": "22/01/2010",
    "Chuyen": "Tin học",
    "Toan": "6.50",
    "Anh": "7.25",
    "Van": "7.25",
    "MonChuyen": "11.50",
    "TongDiem": "38.25"
  },
  {
    "SBD": "251225",
    "HoTen": "Hoàng Thái Minh",
    "NgaySinh": "30/08/2010",
    "Chuyen": "Tin học",
    "Toan": "7.50",
    "Anh": "8.00",
    "Van": "7.25",
    "MonChuyen": "16.00",
    "TongDiem": "46.75"
  },
  {
    "SBD": "251226",
    "HoTen": "Lê Đình Quang Minh",
    "NgaySinh": "03/05/2010",
    "Chuyen": "Tin học",
    "Toan": "7.80",
    "Anh": "8.50",
    "Van": "6.00",
    "MonChuyen": "0.25",
    "TongDiem": "22.68"
  },
  {
    "SBD": "251227",
    "HoTen": "Nguyễn Văn Minh",
    "NgaySinh": "08/01/2010",
    "Chuyen": "Tin học",
    "Toan": "6.90",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "17.25",
    "TongDiem": "48.03"
  },
  {
    "SBD": "251228",
    "HoTen": "Phan Công Minh",
    "NgaySinh": "20/02/2010",
    "Chuyen": "Tin học",
    "Toan": "8.60",
    "Anh": "9.75",
    "Van": "7.75",
    "MonChuyen": "18.50",
    "TongDiem": "53.85"
  },
  {
    "SBD": "251229",
    "HoTen": "Trần Nhật Minh",
    "NgaySinh": "24/02/2010",
    "Chuyen": "Tin học",
    "Toan": "5.30",
    "Anh": "5.50",
    "Van": "5.75",
    "MonChuyen": "0",
    "TongDiem": "16.55"
  },
  {
    "SBD": "251230",
    "HoTen": "Hoàng Đức Khải Nam",
    "NgaySinh": "05/12/2010",
    "Chuyen": "Tin học",
    "Toan": "5.60",
    "Anh": "5.25",
    "Van": "6.50",
    "MonChuyen": "9.75",
    "TongDiem": "31.98"
  },
  {
    "SBD": "251231",
    "HoTen": "Trịnh Bảo Nam",
    "NgaySinh": "13/12/2010",
    "Chuyen": "Tin học",
    "Toan": "7.30",
    "Anh": "9.00",
    "Van": "7.00",
    "MonChuyen": "6.25",
    "TongDiem": "32.68"
  },
  {
    "SBD": "251232",
    "HoTen": "Nguyễn Hữu Khôi Nguyên",
    "NgaySinh": "21/09/2010",
    "Chuyen": "Tin học",
    "Toan": "8.00",
    "Anh": "9.75",
    "Van": "7.00",
    "MonChuyen": "10.25",
    "TongDiem": "40.13"
  },
  {
    "SBD": "251233",
    "HoTen": "Phan Minh Nhật",
    "NgaySinh": "22/10/2010",
    "Chuyen": "Tin học",
    "Toan": "7.90",
    "Anh": "9.50",
    "Van": "6.75",
    "MonChuyen": "19.00",
    "TongDiem": "52.65"
  },
  {
    "SBD": "251234",
    "HoTen": "Nguyễn Đặng Xuân Nhi",
    "NgaySinh": "16/02/2010",
    "Chuyen": "Tin học",
    "Toan": "5.40",
    "Anh": "7.50",
    "Van": "7.75",
    "MonChuyen": "4.25",
    "TongDiem": "27.03"
  },
  {
    "SBD": "251235",
    "HoTen": "Nguyễn Minh Phương",
    "NgaySinh": "15/06/2010",
    "Chuyen": "Tin học",
    "Toan": "10.00",
    "Anh": "8.75",
    "Van": "5.25",
    "MonChuyen": "19.50",
    "TongDiem": "53.25"
  },
  {
    "SBD": "251236",
    "HoTen": "Hồ Lê Anh Quân",
    "NgaySinh": "01/08/2010",
    "Chuyen": "Tin học",
    "Toan": "5.60",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "11.00",
    "TongDiem": "34.85"
  },
  {
    "SBD": "251237",
    "HoTen": "Nguyễn Hoàng Quân",
    "NgaySinh": "21/01/2010",
    "Chuyen": "Tin học",
    "Toan": "4.90",
    "Anh": "6.50",
    "Van": "5.50",
    "MonChuyen": "1.25",
    "TongDiem": "18.78"
  },
  {
    "SBD": "251238",
    "HoTen": "Vương Đình Quân",
    "NgaySinh": "05/02/2010",
    "Chuyen": "Tin học",
    "Toan": "7.70",
    "Anh": "9.25",
    "Van": "6.50",
    "MonChuyen": "7.00",
    "TongDiem": "33.95"
  },
  {
    "SBD": "251239",
    "HoTen": "Nguyễn Nhật Quang",
    "NgaySinh": "29/05/2010",
    "Chuyen": "Tin học",
    "Toan": "7.20",
    "Anh": "6.75",
    "Van": "7.00",
    "MonChuyen": "2.00",
    "TongDiem": "23.95"
  },
  {
    "SBD": "251240",
    "HoTen": "Nguyễn Nhật Quang",
    "NgaySinh": "17/04/2010",
    "Chuyen": "Tin học",
    "Toan": "8.60",
    "Anh": "7.75",
    "Van": "6.75",
    "MonChuyen": "17.50",
    "TongDiem": "49.35"
  },
  {
    "SBD": "251242",
    "HoTen": "Nguyễn Cảnh Quyền",
    "NgaySinh": "16/02/2010",
    "Chuyen": "Tin học",
    "Toan": "5.20",
    "Anh": "8.50",
    "Van": "6.25",
    "MonChuyen": "12.25",
    "TongDiem": "38.33"
  },
  {
    "SBD": "251243",
    "HoTen": "Nguyễn Đình Quyết",
    "NgaySinh": "21/04/2010",
    "Chuyen": "Tin học",
    "Toan": "5.20",
    "Anh": "7.00",
    "Van": "5.50",
    "MonChuyen": "4.00",
    "TongDiem": "23.70"
  },
  {
    "SBD": "251244",
    "HoTen": "Trần Hoàng Sơn",
    "NgaySinh": "06/08/2010",
    "Chuyen": "Tin học",
    "Toan": "7.40",
    "Anh": "10.00",
    "Van": "4.00",
    "MonChuyen": "12.00",
    "TongDiem": "39.40"
  },
  {
    "SBD": "251245",
    "HoTen": "Lê Anh Tuấn Tài",
    "NgaySinh": "22/07/2010",
    "Chuyen": "Tin học",
    "Toan": "4.40",
    "Anh": "4.50",
    "Van": "5.75",
    "MonChuyen": "3.75",
    "TongDiem": "20.28"
  },
  {
    "SBD": "251246",
    "HoTen": "Lê Phạm Đức Tài",
    "NgaySinh": "27/06/2010",
    "Chuyen": "Tin học",
    "Toan": "6.70",
    "Anh": "7.75",
    "Van": "6.50",
    "MonChuyen": "3.25",
    "TongDiem": "25.83"
  },
  {
    "SBD": "251247",
    "HoTen": "Hoàng Nghĩa Thắng",
    "NgaySinh": "08/01/2020",
    "Chuyen": "Tin học",
    "Toan": "6.80",
    "Anh": "7.00",
    "Van": "7.00",
    "MonChuyen": "0",
    "TongDiem": "20.80"
  },
  {
    "SBD": "251248",
    "HoTen": "Võ Quang Thanh",
    "NgaySinh": "22/08/2010",
    "Chuyen": "Tin học",
    "Toan": "6.80",
    "Anh": "9.25",
    "Van": "6.75",
    "MonChuyen": "8.75",
    "TongDiem": "35.93"
  },
  {
    "SBD": "251249",
    "HoTen": "Nguyễn Đại Thành",
    "NgaySinh": "30/10/2010",
    "Chuyen": "Tin học",
    "Toan": "5.80",
    "Anh": "7.25",
    "Van": "6.00",
    "MonChuyen": "9.50",
    "TongDiem": "33.30"
  },
  {
    "SBD": "251250",
    "HoTen": "Võ Công Thành",
    "NgaySinh": "30/07/2010",
    "Chuyen": "Tin học",
    "Toan": "7.00",
    "Anh": "6.25",
    "Van": "7.00",
    "MonChuyen": "11.50",
    "TongDiem": "37.50"
  },
  {
    "SBD": "251251",
    "HoTen": "Cao Minh Thiên",
    "NgaySinh": "29/11/2010",
    "Chuyen": "Tin học",
    "Toan": "6.20",
    "Anh": "6.25",
    "Van": "6.50",
    "MonChuyen": "16.00",
    "TongDiem": "42.95"
  },
  {
    "SBD": "251253",
    "HoTen": "Nguyễn Trọng Toàn",
    "NgaySinh": "18/03/2010",
    "Chuyen": "Tin học",
    "Toan": "8.00",
    "Anh": "9.75",
    "Van": "8.00",
    "MonChuyen": "11.75",
    "TongDiem": "43.38"
  },
  {
    "SBD": "251254",
    "HoTen": "Nguyễn Hữu Nhất Trung",
    "NgaySinh": "28/02/2010",
    "Chuyen": "Tin học",
    "Toan": "6.40",
    "Anh": "7.75",
    "Van": "7.50",
    "MonChuyen": "5.50",
    "TongDiem": "29.90"
  },
  {
    "SBD": "251255",
    "HoTen": "Trần Thành Trung",
    "NgaySinh": "30/01/2010",
    "Chuyen": "Tin học",
    "Toan": "6.40",
    "Anh": "8.50",
    "Van": "6.75",
    "MonChuyen": "5.75",
    "TongDiem": "30.28"
  },
  {
    "SBD": "251256",
    "HoTen": "Bùi Thanh Tú",
    "NgaySinh": "07/10/2010",
    "Chuyen": "Tin học",
    "Toan": "7.20",
    "Anh": "6.50",
    "Van": "6.25",
    "MonChuyen": "12.50",
    "TongDiem": "38.70"
  },
  {
    "SBD": "251257",
    "HoTen": "Bùi Huy Tuấn",
    "NgaySinh": "21/09/2010",
    "Chuyen": "Tin học",
    "Toan": "7.50",
    "Anh": "7.50",
    "Van": "6.00",
    "MonChuyen": "6.25",
    "TongDiem": "30.38"
  },
  {
    "SBD": "251258",
    "HoTen": "Đoàn Minh Tuấn",
    "NgaySinh": "12/03/2010",
    "Chuyen": "Tin học",
    "Toan": "5.20",
    "Anh": "5.25",
    "Van": "7.25",
    "MonChuyen": "4.00",
    "TongDiem": "23.70"
  },
  {
    "SBD": "251259",
    "HoTen": "Nguyễn Thái Tuấn",
    "NgaySinh": "12/10/2010",
    "Chuyen": "Tin học",
    "Toan": "6.90",
    "Anh": "7.25",
    "Van": "6.25",
    "MonChuyen": "11.00",
    "TongDiem": "36.90"
  },
  {
    "SBD": "251260",
    "HoTen": "Võ Văn Tuấn",
    "NgaySinh": "27/05/2010",
    "Chuyen": "Tin học",
    "Toan": "7.20",
    "Anh": "7.00",
    "Van": "6.00",
    "MonChuyen": "11.25",
    "TongDiem": "37.08"
  },
  {
    "SBD": "251261",
    "HoTen": "Đồng Quang Tùng",
    "NgaySinh": "09/09/2010",
    "Chuyen": "Tin học",
    "Toan": "7.50",
    "Anh": "4.75",
    "Van": "6.25",
    "MonChuyen": "8.00",
    "TongDiem": "30.50"
  },
  {
    "SBD": "251262",
    "HoTen": "Nguyễn Thị Thảo Vy",
    "NgaySinh": "12/01/2010",
    "Chuyen": "Tin học",
    "Toan": "8.00",
    "Anh": "6.50",
    "Van": "6.50",
    "MonChuyen": "5.75",
    "TongDiem": "29.63"
  }
]

async def chk1(nmtId: str = ""):
    global password_typelocal
    if not f"{nmtId}" in password_typelocal:
        password_typelocal[f"{nmtId}"] = "!NULL"

async def refresh_code(idStr: str = ""):
    global password_typelocal
    await chk1(idStr)
    chars = []
    for itp in range(0, 10):
        chars.append(f"{itp}")
    chars += ['a', 'b', 'd', 'e', 'f', 'm', 'n', 't', 's', 'x', 'z']
    length_001 = random.randint(6, 7) + 1
    password_typelocal[f"{idStr}"] = ""
    for tp01 in range(1, length_001):
        password_typelocal[f"{idStr}"] += f"{chars[random.randint(0, len(chars) - 1)]}"
    # return base64.b64encode(password_typelocal[f"{idStr}"]).decode("utf-8")



# async def create_captcha(text, font_size=40, font_path="arial.ttf", height=80):
    # try:
        # font = ImageFont.truetype(font_path, font_size)
    # except IOError:
        # font = ImageFont.load_default()

    # # Ước lượng chính xác chiều rộng ảnh bằng tổng độ rộng từng ký tự + padding
    # dummy_img = Image.new("RGB", (1, 1))
    # dummy_draw = ImageDraw.Draw(dummy_img)
    # char_widths = [dummy_draw.textbbox((0, 0), c, font=font)[2] for c in text]
    # spacing = 8  # khoảng cách giữa các ký tự
    # total_width = sum(char_widths) + spacing * (len(text) - 1) + 20  # thêm padding trái/phải

    # # Tạo ảnh trắng với kích thước chính xác
    # image = Image.new("RGB", (total_width, height), (255, 255, 255))
    # draw = ImageDraw.Draw(image)

    # # Vẽ nhiễu tĩnh (phía sau chữ)
    # for _ in range(300):
        # draw.point(
            # (random.randint(0, total_width - 1), random.randint(0, height - 1)),
            # fill=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        # )

    # # Vẽ từng ký tự với hiệu ứng nghiêng riêng
    # current_x = -11  # padding trái
    # for i, char in enumerate(text):
        # char_img = Image.new("RGBA", (font_size * 2, font_size * 2), (255, 255, 255, 0))
        # char_draw = ImageDraw.Draw(char_img)
        # char_draw.text((font_size // 2, font_size // 4), char, font=font,
                       # fill=(random.randint(0, 100), 0, 0))
        # angle = random.uniform(-20, 20)
        # rotated_char = char_img.rotate(angle, resample=Image.BICUBIC, expand=1)

        # # Dán vào ảnh chính
        # y_pos = (height - rotated_char.size[1]) // 2 + random.randint(-2, 2)
        # image.paste(rotated_char, (current_x, y_pos), rotated_char)

        # current_x += char_widths[i] + spacing

    # # Làm mịn
    # image = image.filter(ImageFilter.SMOOTH)
    # return image.convert("RGB")


async def create_captcha(text, font_size=40, font_path="arial.ttf", height=80):
    font_path = os.path.join(os.path.dirname(__file__), "Roboto-Regular.ttf")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Ước lượng chiều rộng ảnh chính xác
    dummy_img = Image.new("RGB", (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)
    char_widths = [dummy_draw.textbbox((0, 0), c, font=font)[2] for c in text]
    spacing = 8
    total_width = sum(char_widths) + spacing * (len(text) - 1) + 20

    # Tạo ảnh và đối tượng vẽ
    image = Image.new("RGB", (total_width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Thêm rất nhiều điểm nhiễu (tăng từ 300 lên ~1500+)
    noise_count = int(total_width * height * 1)  # 100% diện tích là điểm nhiễu
    for _ in range(noise_count):
        x = random.randint(0, total_width - 1)
        y = random.randint(0, height - 1)
        color = (
            random.randint(120, 220),
            random.randint(120, 220),
            random.randint(120, 220)
        )
        draw.point((x, y), fill=color)

    # Vẽ từng ký tự với hiệu ứng xoay và màu ngẫu nhiên
    current_x = -11
    for i, char in enumerate(text):
        char_img = Image.new("RGBA", (font_size * 2, font_size * 2), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((font_size // 2, font_size // 4), char, font=font,
                       fill=(random.randint(0, 100), 0, 0))
        angle = random.uniform(-20, 20)
        rotated_char = char_img.rotate(angle, resample=Image.BICUBIC, expand=1)

        y_pos = (height - rotated_char.size[1]) // 2 + random.randint(-2, 2)
        image.paste(rotated_char, (current_x, y_pos), rotated_char)

        current_x += char_widths[i] + spacing

    image = image.filter(ImageFilter.SMOOTH)
    return image.convert("RGB")





@app.post('/getCaptCode')
async def get_captcha_base64(request: Request): #(text: str = Query(default="abc123"))
    global password_typelocal
    try:
        data = await request.json()
    except:
        return JSONResponse({
            "d": "Error Reading NULL Property",
            "message": "Error"
        })
    if not "nmtId" in data:
        return JSONResponse({
            "d": "Error Reading NULL Property",
            "message": "Error"
        })
    await refresh_code(data["nmtId"])
    img = await create_captcha(password_typelocal[f'{data["nmtId"]}'])
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    img_bytes = buffer.getvalue()

    # Chuyển sang base64
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    base64_url = f"data:image/jpeg;base64,{img_base64}"
    return JSONResponse(content={
        "d": {
            "img": base64_url,
            "sizeW": "200"
        }
    })

# @app.post("/getPass")
# async def getPass():
    # global password_typelocal
    # await refresh_code()
    # print(password_typelocal)
    # return {"dpss": f"{password_typelocal}"}

@app.post("/LayDotXem")
async def getViewData(request: Request):
    global password_typelocal
    try:
        data = await request.json()
    except:
        return JSONResponse({
            "d": "Error Reading NULL Property",
            "message": "Error"
        })
    if not "nmtId" in data:
        return JSONResponse({
            "d": "Error Reading NULL Property",
            "message": "Error"
        })
    await refresh_code(data["nmtId"])
    return_data_getView = []
    return_data_getView.append(
        {
            "__type": "HMHWeb.Models.DiemThi.TraCuuDot",
            "ID": 18,
            "HieuLuc": 0,
            "KyHieu": "KQCHUYEN2025",
            "DienGiai": "KẾT QUẢ THI TUYỂN VÀO LỚP 10 TRƯỜNG THPT CHUYÊN NĂM 2025",
            "GhiChu": "",
            "dataRequestWith": data
        }
    )
    return {
            "message": f"Data getting with: {data}",
            "d": return_data_getView
    }


@app.post("/LayTimKiem")
async def getSearchData(request: Request):
    global password_typelocal
    try:
        data = await request.json()
    except:
        return JSONResponse({
            "d": "Error Reading NULL Property",
            "message": "Error"
        })
    if not "nmtId" in data:
        return JSONResponse({
            "d": "Error Reading NULL Property",
            "message": "Error"
        })
    await refresh_code(data["nmtId"])
    return_data_getSearch_tmp1 = ""
    return_data_getSearch_tmp2 = ""
    if "viewType" in data:
        if f"{data["viewType"]}" == "ngan":
            return_data_getSearch_tmp1 = "SBD"
            return_data_getSearch_tmp2 = "Captcha"
        else:
            return_data_getSearch_tmp1 = "Nhập số báo danh thí sinh"
            return_data_getSearch_tmp2 = "Nhập mã bảo mật"
    else:
        return_data_getSearch_tmp1 = "SBD"
        return_data_getSearch_tmp2 = "Captcha"
    return {
            "message": f"Data getting with: {data}",
            "d": {
                "searchlbl": f"{return_data_getSearch_tmp1}",
                "captchalbl": f"{return_data_getSearch_tmp2}",
            },
            "dataRequestWith": data
    }


@app.post("/LayDuLieu")
async def tra_cuu(request: Request):
    global password_typelocal
    # Tìm thí sinh theo SBD
    try:
        data = await request.json()
    except:
        return JSONResponse({
            "d": "Error Reading NULL Property",
            "message": "Error"
        })
    if not "nmtId" in data:
        return JSONResponse({
            "d": "Error Reading NULL Property",
            "message": "Error"
        })
    await chk1(data["nmtId"])
    try:
        print(data)
        if(not f"{data["mnt"]}" == f"{password_typelocal[f'{data["nmtId"]}']}"):
            print(f"{data["mnt"]}")
            print(f"{data['nmtId']}: {password_typelocal[f'{data["nmtId"]}']}")
            await refresh_code(data["nmtId"])
            return {
                    "message": "Password WRONG!",
                    "d": [{
                        "__type": "HMHWeb.Models.DiemThi.TraCuuXem",
                        "ID": 0000,
                        "DotXem": "null",
                        "Cot01": "Không thể xác nhận mã bảo mật!",
                        "Cot02": "",
                        "Cot03": "",
                        "Cot04": "",
                        "Cot05": "",
                        "Cot06": "",
                        "Cot07": "",
                        "Cot08": "",
                        "Cot09": "",
                        "Cot10": "",
                        "Ten01": "Lỗi",
                        "Ten02": "",
                        "Ten03": "",
                        "Ten04": "",
                        "Ten05": "",
                        "Ten06": "",
                        "Ten07": "",
                        "Ten08": "",
                        "Ten09": "",
                        "Ten10": "",
                        "Hien01": 1,
                        "Hien02": 0,
                        "Hien03": 0,
                        "Hien04": 0,
                        "Hien05": 0,
                        "Hien06": 0,
                        "Hien07": 0,
                        "Hien08": 0,
                        "Hien09": 0,
                        "Hien10": 0
                    }]
            }
        for i, ts in enumerate(students, start=1):
            if ts["SBD"] == data["timKiem"]:
                return_data = [{
                    "__type": "HMHWeb.Models.DiemThi.TraCuuXem",
                    "ID": 3900 + i,
                    "DotXem": data["dotXem"],
                    "Cot01": ts["SBD"],
                    "Cot02": ts["HoTen"],
                    "Cot03": ts["NgaySinh"],
                    "Cot04": ts["Chuyen"],
                    "Cot05": f" {ts['Toan']} ",
                    "Cot06": f" {ts['Anh']} ",
                    "Cot07": f" {ts['Van']} ",
                    "Cot08": f" {ts['MonChuyen']} ",
                    "Cot09": f" {ts['TongDiem']} ",
                    "Cot10": "",
                    "Ten01": "SBD",
                    "Ten02": "Họ và tên",
                    "Ten03": "Ngày sinh",
                    "Ten04": "Chuyên",
                    "Ten05": "Toán vòng 1",
                    "Ten06": "Anh vòng 1",
                    "Ten07": "Văn vòng 1",
                    "Ten08": "Môn chuyên",
                    "Ten09": "Tổng điểm",
                    "Ten10": "",
                    "Hien01": 1,
                    "Hien02": 1,
                    "Hien03": 1,
                    "Hien04": 1,
                    "Hien05": 1,
                    "Hien06": 1,
                    "Hien07": 1,
                    "Hien08": 1,
                    "Hien09": 1,
                    "Hien10": 0
                }]
                await refresh_code(data["nmtId"])
                return {"message": f"Data Found With 'SBD' '{ts["SBD"]}'", "d": return_data}

        await refresh_code(data["nmtId"])
        return {"message": "Not Found", "d": []}#, status_code=200)
    except:
        try:
            await refresh_code(data["nmtId"])
        except:
            print("NULL001|LNT")
        return {"message": "Err", "d": []}
