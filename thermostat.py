import requests
import json
import os


# get nest credentials from file
def getcredentials():

    try:
        #go into json directory
        current_dir = os.getcwd()
        os.chdir('json')

        #load credentials file
        fileObject = open("credentials.json", "r")
        jsonContent = fileObject.read()
        fileObject.close()
        data = json.loads(jsonContent)

        #retrieve information using data.get()
        client_id = data.get('web').get('client_id')
        client_secret = data.get('web').get('client_secret')

        #load token file
        fileObject = open("refreshtoken.json", "r")
        jsonContent = fileObject.read()
        fileObject.close()
        data = json.loads(jsonContent)

        #retrieve information using data.get()
        refresh_token = data.get('refresh_token')

        #load projectid file
        fileObject = open("projectid.json", "r")
        jsonContent = fileObject.read()
        fileObject.close()
        data = json.loads(jsonContent)

        #retrieve information using data.get()
        project_id = data.get('project_id')

        #put data in a dict
        credentials = dict(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            project_id=project_id
            )

        #go back to parent directory
        os.chdir(current_dir)

    except FileNotFoundError as not_found:
        print('File not found: ' + not_found.filename)
        credentials = None

    finally:
        #return dict
        return credentials


# generate 1-hour access token
def generatetoken():

    # obtain nest credentials from file
    credentials = getcredentials()

    CLIENT_ID = credentials.get('client_id')
    CLIENT_SECRET = credentials.get('client_secret')
    REFRESH_TOKEN = credentials.get('refresh_token')

    #post to refresh the access_token
    refresh_url = (
        'https://www.googleapis.com/oauth2/v4/token?'
        f'client_id={CLIENT_ID}&'
        f'client_secret={CLIENT_SECRET}&'
        f'refresh_token={REFRESH_TOKEN}&'
        'grant_type=refresh_token'
        )

    print(f'Posting to: https://www.googleapis.com/oauth2/v4/token')
    response = requests.post(refresh_url)
    print(f'Token response: {response}')
    return response.json().get('access_token')


# contact thermostat and return heat status as either 'HEATING' or 'OFF'
def probethermostat():

    # obtain projectid from file
    credentials = getcredentials()
    PROJECT_ID = credentials.get('project_id')

    # uses refresh token to generate 1-hour token
    token = generatetoken()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
        }

    url = (
        'https://smartdevicemanagement.googleapis.com/'
        f'v1/enterprises/{PROJECT_ID}/devices'
        )

    #probe the thermostat
    print('Posting to: https://smartdevicemanagement.googleapis.com')
    response = requests.get(url, headers=headers)
    print(f'Thermostat response: {response}')

    #formatted response
    response = response.json().get('devices')
    if response:
        response = response[0]['traits']
        response = response['sdm.devices.traits.ThermostatHvac']['status']

    print(f'Status: {response}')
    return response
