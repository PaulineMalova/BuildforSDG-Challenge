import time
from flask import Flask, request, Response, jsonify
from dicttoxml import dicttoxml
from src.estimator import estimator, format_time_logs

app = Flask(__name__)


@app.route("/api/v1/on-covid-19", methods=["POST"])
def estimate_covid19_impact():
    """Estimate Covid-19 Impact based on given data"""
    start = time.clock()
    data = request.json
    response = estimator(data)
    resp = jsonify(response)
    resp.status_code = 200
    request_time = time.clock() - start
    request_time_data = {
        "path": "/api/v1/on-covid-19",
        "time": request_time,
        "method": "POST",
        "status_code": resp.status_code,
    }
    format_time_logs(request_time_data)
    return resp


@app.route("/api/v1/on-covid-19/json", methods=["POST"])
def estimate_covid19_impact_json():
    """Estimate Covid-19 Impact based on given data and return json format"""
    if request.headers["Content-Type"] == "application/json":
        start = time.clock()
        data = request.json
        response = estimator(data)
        resp = jsonify(response)
        resp.status_code = 200
        request_time = time.clock() - start
        request_time_data = {
            "path": "/api/v1/on-covid-19/json",
            "time": request_time,
            "method": "POST",
            "status_code": resp.status_code,
        }
        format_time_logs(request_time_data)
        return resp


@app.route("/api/v1/on-covid-19/xml", methods=["POST"])
def estimate_covid19_impact_xml():
    """Estimate Covid-19 Impact based on given data and return xml format"""
    start = time.clock()
    data = request.json
    result = estimator(data)
    xml = dicttoxml(result)
    xml = xml.decode()
    resp = Response(xml, status=200, mimetype="application/xml")
    request_time = time.clock() - start
    request_time_data = {
        "path": "/api/v1/on-covid-19/xml",
        "time": request_time,
        "method": "POST",
        "status_code": resp.status_code,
    }
    format_time_logs(request_time_data)
    return resp


@app.route("/api/v1/on-covid-19/logs", methods=["GET"])
def get_time_logs():
    start = time.clock()
    with open("src/logs.txt", "r") as logs_file:
        result = logs_file.read()
        resp = Response(result, status=200, mimetype="text/plain")
        request_time = time.clock() - start
        request_time_data = {
            "path": "/api/v1/on-covid-19/logs",
            "time": request_time,
            "method": "GET",
            "status_code": resp.status_code,
        }
        format_time_logs(request_time_data)
        return resp


if __name__ == "__main__":
    app.run(debug=True)
