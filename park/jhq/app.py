import ast
import hashlib
import logging
import os
import random
import re
import string
import time
from collections import defaultdict

import requests
from flask import Flask, jsonify, render_template, request


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "parking_management.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = Flask(__name__)

open_id_list = [
    'MrUO3W6kwbGV4i7DOskcb6rVkpQc', 's5zxaNybXfT7fS2rSOb68x4UiDTR', 'CnpmngvcvItm8RFtoiNwJyurnXPH',
    'RUN3PtbieqhatzsS1PN0zzC0D8kQ', 'qVsmYCx87ddx8A2FueYIEKNOftAX', 'C13nGeJXwiqZjMqdwRCHIi28dOIF',
    'v49mhppTjFgx0Nhyqh9QWp7QVdNH', 'uzZEEOldGzAK6wUFaFQkwahZb1AW', 'hnXfMKXzH9KFlro9Ty6Gg7xGGTXc',
    'amkVUTIPMkG7zrvZn48y8JRkmu9e', 'XERWxSV0NAJjhnto8Aql9RR9UklJ', 'ZcMCsfxHltZNA5mcQWkflXCMy8pg',
]

PLATE_ALLOWED_CHARS = set("挂学警港澳领使")


def generate_random_number(seed_string, max_value=299):
    hash_object = hashlib.md5(seed_string.encode())
    seed = int(hash_object.hexdigest(), 16)
    random.seed(seed)
    return random.randint(0, max_value)


def generate_random_open_id(length=28):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def sanitize_plate_number(raw_text):
    cleaned = []
    for char in str(raw_text).upper():
        if char.isspace():
            continue
        if '\u4e00' <= char <= '\u9fff' or char.isalnum() or char in PLATE_ALLOWED_CHARS:
            cleaned.append(char)
    return ''.join(cleaned)


def is_valid_plate_number(plate):
    if not (6 <= len(plate) <= 8):
        return False
    if not any('\u4e00' <= char <= '\u9fff' for char in plate):
        return False
    return bool(re.fullmatch(r'[\u4e00-\u9fff][A-Z0-9挂学警港澳领使]{5,7}', plate))


def jhq_query(plate, open_id=None):
    url = "https://m.mallcoo.cn/api/park/ParkFee/GetParkFeeV3"
    open_id = open_id or generate_random_open_id(16)
    headers = {
        "Host": "m.mallcoo.cn",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Accept": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://servicewechat.com/wx{open_id}/2/page-frame.html",
    }
    data = {
        "UID": "0",
        "MallID": 12931,
        "ParkID": 1777,
        "PlateNo": plate,
        "Barcode": "",
        "FreeMinutes": 0,
        "FreeAmount": 2000,
        "timetip": int(time.time() * 1000),
        "Header": {"Token": ""},
    }
    response = requests.post(url, headers=headers, json=data, timeout=8)
    response.raise_for_status()
    body = response.json().get("d", {})
    return {
        "入场时间": body.get("EntryTime", ""),
        "停车时长": body.get("ParkingMinutes", 0),
        "需要支付的费用": body.get("ParkingFee", 0.0),
    }


def jhq_discount(plate, random_open_id=False):
    if random_open_id:
        open_id = generate_random_open_id()
    else:
        open_id = open_id_list[generate_random_number(plate, len(open_id_list) - 1)]

    query_result = jhq_query(plate, open_id)
    if not query_result or query_result.get("需要支付的费用", 0) <= 0:
        return "待支付费用为0", query_result

    url = "http://app.archshanghai.com/jhq/app/discount/shopDiscount/discountByPlate"
    headers = {
        "Host": "app.archshanghai.com",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer null",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "http://app.archshanghai.com",
        "User-Agent": "Mozilla/5.0",
        "Connection": "keep-alive",
        "Referer": "http://app.archshanghai.com/jhq/mobile/",
    }
    data = {
        "status": 0,
        "parking_coupon_number": plate,
        "idx": "63b0d1fcce8b686558bfc43c",
        "flag": "1",
        "disTime": 2,
        "EntryTime": query_result.get("入场时间", ""),
        "disNo": "NO.shop088",
        "openid": open_id,
        "organization": "59688d03798e5004d69dab47",
        "page": "shopDiscount",
    }
    response = requests.post(
        url,
        headers=headers,
        json=data,
        params={"Timestamp": int(time.time() * 1000)},
        timeout=8,
    )
    response.raise_for_status()
    return response.text, query_result


def log_parking_info(plate_number, info, log_type):
    logging.info(f"Plate: {plate_number}, Type: {log_type}, Info: {info}")


def parse_log_message(message):
    match = re.match(r"Plate: (?P<plate>.*?), Type: (?P<type>.*?), Info: (?P<info>.*)", message)
    if not match:
        return None

    try:
        info = ast.literal_eval(match.group("info"))
    except (SyntaxError, ValueError):
        info = {"原始信息": match.group("info")}

    return {
        "plate": match.group("plate"),
        "type": match.group("type"),
        "info": info,
    }


def load_daily_log_summary(log_file):
    summary = defaultdict(lambda: {
        "query_records": 0,
        "query_plates": set(),
        "discount_success_records": 0,
        "discount_success_plates": set(),
    })

    if not os.path.exists(log_file):
        return []

    with open(log_file, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if " - INFO - Plate: " not in line:
                continue

            parts = line.split(" - ", 2)
            if len(parts) != 3:
                continue

            day = parts[0].split(" ")[0]
            payload = parse_log_message(parts[2])
            if not payload:
                continue

            daily = summary[day]
            plate = payload["plate"]
            log_type = payload["type"]
            info = payload["info"]

            if log_type.startswith("query_"):
                daily["query_records"] += 1
                daily["query_plates"].add(plate)

            if log_type.startswith("discount_"):
                discount_text = str(info.get("折扣信息", ""))
                if "折扣成功" in discount_text:
                    daily["discount_success_records"] += 1
                    daily["discount_success_plates"].add(plate)

    rows = []
    for day in sorted(summary.keys(), reverse=True):
        daily = summary[day]
        rows.append({
            "date": day,
            "query_records": daily["query_records"],
            "query_plate_count": len(daily["query_plates"]),
            "discount_success_records": daily["discount_success_records"],
            "discount_success_plate_count": len(daily["discount_success_plates"]),
        })
    return rows


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/log")
def log_page():
    return render_template("log.html", rows=load_daily_log_summary(LOG_FILE))


@app.route("/api/query", methods=["POST"])
def api_query():
    payload = request.get_json(silent=True) or {}
    plate = sanitize_plate_number(payload.get("plate", ""))
    if not plate:
        return jsonify({"error": "车牌号不能为空"}), 400
    if not is_valid_plate_number(plate):
        return jsonify({"error": "请输入有效的中国车牌号", "plate": plate}), 400

    try:
        result = jhq_query(plate)
        result["状态"] = "未抵扣"
        log_parking_info(plate, result, "query_金虹桥")
        return jsonify({"plate": plate, "result": result})
    except Exception as exc:
        logging.error(f"JHQ query error for plate {plate}: {exc}")
        return jsonify({"error": str(exc), "plate": plate}), 500


@app.route("/api/discount", methods=["POST"])
def api_discount():
    payload = request.get_json(silent=True) or {}
    plate = sanitize_plate_number(payload.get("plate", ""))
    random_open_id = bool(payload.get("random_open_id"))
    if not plate:
        return jsonify({"error": "车牌号不能为空"}), 400
    if not is_valid_plate_number(plate):
        return jsonify({"error": "请输入有效的中国车牌号", "plate": plate}), 400

    try:
        discount_result, before_query = jhq_discount(plate, random_open_id=random_open_id)
        log_parking_info(plate, {"折扣信息": discount_result}, "discount_金虹桥")

        refreshed_result = jhq_query(plate)
        refreshed_result["状态"] = "已抵扣" if "折扣成功" in discount_result else "抵扣后已刷新"
        log_parking_info(plate, refreshed_result, "query_金虹桥")

        return jsonify({
            "plate": plate,
            "discount_result": discount_result,
            "before_query": before_query,
            "result": refreshed_result,
        })
    except Exception as exc:
        logging.error(f"JHQ discount error for plate {plate}: {exc}")
        return jsonify({"error": str(exc), "plate": plate}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8001)
