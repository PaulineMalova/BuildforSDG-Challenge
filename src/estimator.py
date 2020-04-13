import math
from datetime import datetime


def estimator(data):
    data = format_final_result(data)
    return data


def format_final_result(data):
    result = {}
    impact_data = calculate_impact(data)
    severe_impact_data = calculate_severe_impact(data)
    result["data"] = data
    result["impact"] = impact_data
    result["severeImpact"] = severe_impact_data
    return result


def calculate_impact(data):
    impact = {}
    impact["currentlyInfected"] = data["reportedCases"] * 10
    days = get_period_type_in_days(data)
    factor = int(days / 3)
    impact["infectionsByRequestedTime"] = int(
        impact["currentlyInfected"] * (2 ** factor)
    )
    impact["severeCasesByRequestedTime"] = int(
        0.15 * impact["infectionsByRequestedTime"]
    )
    impact[
        "hospitalBedsByRequestedTime"
    ] = get_hospital_beds_by_requested_time(
        data, impact["severeCasesByRequestedTime"]
    )
    impact["casesForICUByRequestedTime"] = (
        0.05 * impact["infectionsByRequestedTime"]
    )
    impact["casesForVentilatorsByRequestedTime"] = (
        0.02 * impact["infectionsByRequestedTime"]
    )
    impact["dollarsInFlight"] = calculate_dollars_in_flight(
        data, impact["infectionsByRequestedTime"], days
    )
    return impact


def calculate_severe_impact(data):
    severeImpact = {}
    severeImpact["currentlyInfected"] = data["reportedCases"] * 50
    days = get_period_type_in_days(data)
    factor = int(days / 3)
    severeImpact["infectionsByRequestedTime"] = int(
        severeImpact["currentlyInfected"] * (2 ** factor)
    )
    severeImpact["severeCasesByRequestedTime"] = int(
        0.15 * severeImpact["infectionsByRequestedTime"]
    )
    severeImpact[
        "hospitalBedsByRequestedTime"
    ] = get_hospital_beds_by_requested_time(
        data, severeImpact["severeCasesByRequestedTime"]
    )
    severeImpact["casesForICUByRequestedTime"] = (
        0.05 * severeImpact["infectionsByRequestedTime"]
    )
    severeImpact["casesForVentilatorsByRequestedTime"] = (
        0.02 * severeImpact["infectionsByRequestedTime"]
    )
    severeImpact["dollarsInFlight"] = calculate_dollars_in_flight(
        data, severeImpact["infectionsByRequestedTime"], days
    )
    return severeImpact


def get_period_type_in_days(data):
    # Assuming a week has 7 days and a month 30 days
    if data["periodType"] == "days":
        days = data["timeToElapse"]
    elif data["periodType"] == "weeks":
        days = data["timeToElapse"] * 7
    elif data["periodType"] == "months":
        days = data["timeToElapse"] * 30
    return days


def get_hospital_beds_by_requested_time(data, cases):
    available_beds_for_covid = data["totalHospitalBeds"] * 0.35
    return int(available_beds_for_covid - cases)


def calculate_dollars_in_flight(data, infections_by_requested_time, days):
    infected_income_population = (
        infections_by_requested_time
        * data["region"]["avgDailyIncomePopulation"]
    )
    return math.trunc(
        (
            infected_income_population
            * data["region"]["avgDailyIncomeInUSD"]
            * days
        )
    )


def format_time_logs(request_time_data):
    time_stamp = int(datetime.now().timestamp())
    url = request_time_data["path"]
    time = round(request_time_data["time"], 5)
    request_time = f"{time_stamp} \t\t on-{url} \t\t done in {time} seconds"
    with open("src/logs.txt", "a") as logs_file:
        logs_file.write(f"{request_time}\n")
