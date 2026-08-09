import requests
import pandas as pd
import os
from datetime import datetime

currentLane = None

def get_port_data(port_code, port_name):

    url = f"https://bwt.cbp.gov/api/bwtrss/rssbyportnum/HTML/ALL/{port_code}"
    response = requests.get(url)

    description = response.text.split("<description>")[2]
    description = description.split("</description>")[0]
    lines = description.split("<br/>")

    results = []

    current_category = None

    for line in lines:

        if ("<h4>") in line:
            temp = line.split("</b")[0].split("<b>")
            current_category = temp[1].strip()
            
        elif ("Lanes:") in line:
            temp = line.split("Lanes:")
            lane_type = temp[0].strip()
            currentLane = temp[1]

            wait_minutes = None

            if "Lanes Closed" in currentLane:
                status = "closed"

            elif "N/A" in currentLane: 
                status = "not applicable"

            else: 
                status = "reported"

                before_min = currentLane.split("min delay")[0]
                wait_minutes = int(before_min.split()[-1])

            
                            
            results.append({
                "port_name": port_name,
                "category": current_category,
                "lane_type": lane_type,
                "status": status,
                "wait_minutes": wait_minutes    
            })

    return results


ports = {
    "240201": "Bridge of the Americas",
    "240202": "Paso Del Norte",
    "240203": "Ysleta",
    "240204": "Stanton",
}

final_result = []

for code, name in ports.items():
    port_data = get_port_data(code, name)
    final_result.extend(port_data)
    

df = pd.DataFrame(final_result)
df["timestamp"] = datetime.now()

script_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_folder, "..", "data", "raw", "wait_times.csv")
file_exists = os.path.exists(csv_path)
df.to_csv(csv_path, mode="a", header=not file_exists, index=False)
print("Done")


    

    

