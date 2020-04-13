import time
from flask import Flask, request, Response
from dicttoxml import dicttoxml
from src.estimator import estimator, format_time_logs

app = Flask(__name__)


@app.route("/api/v1/on-covid-19", methods=["POST"])
def estimate_covid19_impact():
    """Estimate Covid-19 Impact based on given data"""
    start = time.clock()
    data = request.json
    response = estimator(data)
    request_time = time.clock() - start
    request_time_data = {"path": "covid-19", "time": request_time}
    format_time_logs(request_time_data)
    return response


@app.route("/api/v1/on-covid-19/json", methods=["POST"])
def estimate_covid19_impact_json():
    """Estimate Covid-19 Impact based on given data and return json format"""
    start = time.clock()
    data = request.json
    response = estimator(data)
    request_time = time.clock() - start
    request_time_data = {"path": "covid-19/json", "time": request_time}
    format_time_logs(request_time_data)
    return response


@app.route("/api/v1/on-covid-19/xml", methods=["POST"])
def estimate_covid19_impact_xml():
    """Estimate Covid-19 Impact based on given data and return xml format"""
    start = time.clock()
    data = request.json
    result = estimator(data)
    xml = dicttoxml(result)
    xml = xml.decode()
    result = Response(response=xml, status=200, mimetype="application/xml")
    result.headers["Content-Type"] = "text/xml; charset=utf-8"
    request_time = time.clock() - start
    request_time_data = {"path": "covid-19/xml", "time": request_time}
    format_time_logs(request_time_data)
    return result


@app.route("/api/v1/on-covid-19/logs", methods=["GET"])
def get_time_logs():
    with open("src/logs.txt", "r") as logs_file:
        return logs_file.read()


if __name__ == "__main__":
    app.run(debug=True)
