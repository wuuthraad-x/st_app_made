import streamlit as st
import datetime
import requests
import json
import time
import http.client
import json
import pandas as pd

st.header('Madibana API endpoint xero invoice creator')
st.image('madibana_logo.png')

st.subheader('Invoices will automatically be created at 00:00:00 SAST')
st.subheader(f'Current Time : {datetime.datetime.now()}')
# st.write(f' Current Time : {datetime.datetime.now()}')


if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True
st.write("Click button below to run Xero invoice creation")
st.button('Invoice Creation', on_click=click_button)

import time
import streamlit as st

# with st.status("Creating Invoices...", expanded=True) as status:
#     st.write("Searching for data...")
#     time.sleep(2)
#     st.write("Found URL.")
#     time.sleep(1)
#     st.write("Downloading data...")
#     time.sleep(1)
#     status.update(label="Download complete!", state="complete", expanded=False)

# st.button('Rerun')

# Replace this with your own API endpoint URL
api_endpoint_url = "https://bot.sa.madibana.com/API/fetchInvoices.php"
if st.session_state.clicked:
    
    with st.status('Creating Invoices...' , expanded=True) as status:
        time.sleep(2)
        ##############################################################################
        st.write(f'collecting Data from {api_endpoint_url}')
        
        # Send a GET request to the API endpoint
        response = requests.get(api_endpoint_url)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()

            # Save the data in a JSON file
            with open("invoices.json", "w") as file:
                json.dump(data, file, indent=4)

            print("Data saved successfully")
        else:
            print("Request failed with status code:", response.status_code)
        time.sleep(2)
        ###################################################################################    
        st.write('Savaing data...')

        data = pd.read_json('invoices.json')

        z = []
        for i in range(len(data)):
            z.append(data['data'][i].values())

        pd.DataFrame(z , columns=data['data'][0].keys()).to_csv('invoices.csv' , index=False)
        # print("Excel file created in working directory!")
        
        st.write(f'saved {data.info}')
        st.write(f'Writing invoices to Xero')

        conn = http.client.HTTPSConnection("api.xero.com")
        payload = json.dumps({
          "Type": "ACCREC",
          "Contact": {
            "ContactID": "bfc98c28-34de-4d92-8af6-1e61264948e0"
          },
          "Date": "/Date(1518685950940+0000)/",
          "DueDate": "/Date(1518685950940+0000)/",
          "DateString": str(data.loc[data['id'] == 40]['payment_date']).split(' ')[4],
          "DueDateString": str(data.loc[data['id'] == 40]['payment_date']).split(' ')[4],
          "LineAmountTypes": "Exclusive",
          "LineItems": [
            {
              "Description": "Consulting services as agreed (20% off standard rate)",
              "Quantity": "10",
              "UnitAmount": "100.00",
              "AccountCode": "200",
              "DiscountRate": "20"
            }
          ]
        })
        headers = {
          'xero-tenant-id': '0796c933-f6b5-493d-bda4-7c2bc0e58fa2',
          'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjFDQUY4RTY2NzcyRDZEQzAyOEQ2NzI2RkQwMjYxNTgxNTcwRUZDMTkiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJISy1PWm5jdGJjQW8xbkp2MENZVmdWY09fQmsifQ.eyJuYmYiOjE3MDY5NDc3NzYsImV4cCI6MTcwNjk0OTU3NiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS54ZXJvLmNvbSIsImF1ZCI6Imh0dHBzOi8vaWRlbnRpdHkueGVyby5jb20vcmVzb3VyY2VzIiwiY2xpZW50X2lkIjoiQjk3MkYyQkIxN0ExNDA2MjhBMUU3RTc0MDQwODgzOTQiLCJzdWIiOiI5ZDEyYWZhMzFlN2U1NmM2ODJjODNhZjYyY2M0MzM1NSIsImF1dGhfdGltZSI6MTcwNjc1NzAxMywieGVyb191c2VyaWQiOiJmMzhhMTlhOS1kODhhLTRmZmYtOTQxMC0wNTA3NDVmOTQyZGQiLCJnbG9iYWxfc2Vzc2lvbl9pZCI6IjEyNjMxMThjZjAwNDQ2OWViMzliOTU1MzgzZGZhMGQyIiwic2lkIjoiMTI2MzExOGNmMDA0NDY5ZWIzOWI5NTUzODNkZmEwZDIiLCJqdGkiOiJCREFFQTJDODE1NTJEMkZGNTg1QkY4MTBEMUNFN0E2QSIsImF1dGhlbnRpY2F0aW9uX2V2ZW50X2lkIjoiMjFkZGFmMWUtZjM1Yy00Zjg4LThiYzAtN2Y2ZjI1OTg5MTVhIiwic2NvcGUiOlsiZW1haWwiLCJwcm9maWxlIiwib3BlbmlkIiwiYWNjb3VudGluZy50cmFuc2FjdGlvbnMiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsibGVnYWN5Il19.uY4lW76Ip2_Um9Vs9Jo8oAsLz60YwHfUD737b1haqEkKyXcgPS-UxTrEsib1OL9TY8GdkS0GU7GOnsrsc_2xuDMev7HmuuxJLEDE1bnq6uNGjyX1gwT1YKf9Tp6ZWQBmwAb0_Q85DaG9bV_kb0OqjfPNm__mbbQ2g1a3fhdMzhm4AcZh3amR6twLMOh_WGjMMJ4AEW9Bi9ae4oS4Yc85M7HR0jV_HZQeEZqR95XA_vTv-18m8Ar_RFfvPfybsgG7PX_db1YwQ4WpntS8VjEnus4gbTGhPHEqECOL-7s4bvAzEOL-trUcI3TzTsvsDLwGsfrJphbPOJ1FlyiMEmfHLQ',
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Cookie': '_abck=0AEC21C3C592F4152A18BA217DBB3957~-1~YAAQxp82F6Q2i2qNAQAAoBEEbgsfDA422NNHx/QOMRdYHJqaOMnmd+FABcpfmphlqtRIsXYylR4gHAFNjVj03X2o88kz/wb4dlHMKKJPptCLkIMHjB1gavZs4VLQouEhFWVlig6nik/7VM9s1cm9evnbv0aCtZ8B+RyxwXjt4NJRck2fXmgbzxzp6/UR7aXayEfIb/9105zfUc/f6avnsbyVgeqK2laGv0EvhIUeZvcyAKX6nAcBWuvnX5znwb3gxeMW6RdpBRRyIliQmC0mj5KASmBHrG4H1eXyfhtizcKHBRIfGaHqXBHdnGYOdlwVtyv87HD3GzoMTm8bk0HIhXOBhLV06DskOuOtQaQuRMXi7YtExCSQNT8pyhitZflIfQ7UEHo=~-1~-1~-1; ak_bmsc=9D40F5AC9246F2DE42B4BFBF6418A182~000000000000000000000000000000~YAAQxp82F6U2i2qNAQAAoBEEbhZ6Mr1bVwDTULkWdYCQRtgkZ536waxhvFIUKe8RfDDzwPSsizyRuz4BWdJdG9rDplFd4/RLOA41dKiCDzFxdAdaMPgsioD+RxiSAZpqDTSccLmM29g1TYLSNTAhtmwI89Qh6DHfZ5iIWbMph+kyYArmQDAzGDkWrZoZwTPnjza3ewoLcAwZ9SUrFcLy9FgutdmHaED0gxtpbKs6Vdo5kT1sTe0PpIDbNgS6xOHHUkm4i4AeonkbKZyWAcXLgDr1A2icglmK9xtlZSQaZ8t7DC8UhSS+Dyf2yKSkghXW12g2l/3YQWOU5tEKrkycaJc02nEyeunGNNzO6dUJ6tQNvrUBRuilL3E2rA==; bm_sv=4198744F0647D6A20660825B66AADBEB~YAAQCqQRAj1NflmNAQAAIxYEbhZCmxNxnM3GaWvzoXPZHSjy3K1j4Ds/CwW97xejNkAvv5XkIFxEUxUrxS6d8pmFJ90Fkue80ZsaK0qhe7jXAXt4qGIs86pewVpfztKrFifTJfe2doe5ftxeTWejoIXvHswo0hgtf3+N2g2gQUWlMGge9w2EENripFt2Y+uWZD8eIJh8+Mg4sn9PFxiJ64zrwUk3LquY5E7nEf/M9KMwBTqtBfcYBXvffCVwoA==~1; bm_sz=3D4D9A329F50C15275794877BE175A72~YAAQxp82F6Y2i2qNAQAAoBEEbhbicV/2uxR02rZMvR/t69baBY7jrXQPqHTS+mUsQ0wbALJGokZRcDkup5YfTSBIfWRHm/wx2T5qE8wYm0Tpoe3BGDjtye1VuCilu1MY0Jj0eKIxRx9mZsxDMryXrCj1BZrcsJrmGNq2EGopLZePSMipluJpBlsmXv0qsgzKsvZsfRXWuHMVwswlW+/eJ3YZWCJibrmHFzYC0UNZEj6CrkZeZZLK3kJDtKFCDId5GE5dyMCo+FLS1dy9kjJyMsVveTuCYr6JovmeY7mvtFCHMZl0usEWsi9V+MINtVnXTV/qQg4u+zMEz399sQ==~4539701~3551792'
        }
        conn.request("PUT", "/api.xro/2.0/Invoices", payload, headers)
        res = conn.getresponse()
        data = res.read()
        # print(data.decode("utf-8"))
        status.update(label="Invoices complete!", state="complete", expanded=False)
        time.sleep(2)
    st.button('Rerun')
