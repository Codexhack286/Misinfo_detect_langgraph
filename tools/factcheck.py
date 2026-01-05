import requests
from config import GOOGLE_FACTCHECK_KEY

FACTCHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def google_fact_check(headline: str):
    params = {
        "query": headline,
        "key": GOOGLE_FACTCHECK_KEY
    }
    response = requests.get(FACTCHECK_URL, params=params)
    return response.json()
