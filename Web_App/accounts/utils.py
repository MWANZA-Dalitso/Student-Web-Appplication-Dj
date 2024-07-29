# accounts/utils.py
import datetime
def get_academic_years():
    current_year = datetime.date.today().year
    return [(f"{year}/{year + 1}", f"{year}/{year + 1}") for year in range(2020, current_year + 1)]
