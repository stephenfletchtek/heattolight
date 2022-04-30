import base64
import requests
import json
import os
import pyperclip
import time
import webbrowser


# open file and read contents
# returns None if file could not be read
# will return empty contents if file is empty
def readfromfile(filename):

    try:
        #go into json directory
        current_dir = os.getcwd()

        if os.path.basename(current_dir) != 'json':
            os.chdir('json')

        if filename:
            #read from file
            fileObject = open(filename, "r")
            jsonContent = fileObject.read()
            fileObject.close()

    except FileNotFoundError:
        jsonContent = None

    finally:
        #back to parent directory
        os.chdir(current_dir)
        return jsonContent


# write file to json folder
# convert data to json
# doesnt throw an error if data is empty
def writefile(name, data):

    try:
        #go into json directory
        current_dir = os.getcwd()
        if os.path.basename(current_dir) != 'json':
            os.chdir('json')

        json_string = json.dumps(data)
        print(json_string)

        json_file = open(name, 'w')
        json_file.write(json_string)
        json_file.close()

    except FileNotFoundError:
        print('File not found')
        return False

    finally:
        os.chdir(current_dir)

    return True


# read json file and return token
def gettoken():

    content = readfromfile('token.json')

    if content:
        data = json.loads(content)
        data = data.get('access_token')
        return data
    else:
        return None


# read json file and return username
def getuser():

    content = readfromfile('username.json')

    if content:
        data = json.loads(content)
        data = data[0]['success']['username']
        return data
    else:
        return None


# Authorization request followed by get token
# call this to get a new token without a refresh token
# hue issues a code that needs to be entered manually at the prompt
# the code must be entered within 10 minutes of being issued
def authorize():

    #input box to wait for localhost server
    filetorun = 'cd /Users/stephenfletcher/Documents/Django/codesnatcher'
    pyperclip.copy(filetorun)
    input("Start localhost:4001 for code snatcher and authorise Phillips use")

    #remove existing code file
    try:
        current_dir = os.getcwd()
        if os.path.basename(current_dir) != 'json':
            os.chdir('json')
        os.remove('huecode.json')
    except FileNotFoundError:
        print('File not found')
    finally:
        os.chdir(current_dir)

    # pull client id and clientsecret from file
    jsonContent = readfromfile('myapps.json')
    data = json.loads(jsonContent)
    ClientId =  data.get('ClientId')
    ClientSecret = data.get('ClientSecret')

    # base64 encode 'ClientId:ClientSecret'
    enc_string = ClientId + ':' + ClientSecret
    enc_string_bytes = enc_string.encode("ascii")
    base64_bytes = base64.b64encode(enc_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    #make get request
    url = 'https://api.meethue.com/v2/oauth2/authorize?'
    params = {'client_id':ClientId, 'response_type':'code'}
    response = requests.get(url, params=params)

    #open up chrome and launch url
    web_path = 'open -a /Applications/Google\ Chrome.app %s'
    web_url = response.url
    webbrowser.get(web_path).open(web_url)

    #Django project 'code snatcher' will write auth code to file
    #Read code from 'huecode.json' once it exists!
    #This is horrific but will do just to prove a point
    secs = 59
    print(f'Waiting for authorisation: {secs}')
    while readfromfile('huecode.json') == None:
        time.sleep(1)
        secs -= 1
        #this clears the last line for the count down
        print ("\033[A \033[A")
        print(f'Waiting for authorisation: {secs}')

        if readfromfile('huecode.json') != None:
            content = readfromfile('huecode.json')
            code = json.loads(content)
            code = code.get('code')
            print(f'The code is: {code}')
            break
        elif secs == 0:
            print('Timed out waiting for authorisation!')
            code = ''
            break
        else:
            pass

    #make post request
    url = 'https://api.meethue.com/v2/oauth2/token'
    data = {'grant_type':'authorization_code', 'code':code}

    headers = {
        'Authorization': f'Basic {base64_string}',
        'Content-type':'application/x-www-form-urlencoded'
        }

    print('Getting token')
    response = requests.post(url, data=data, headers=headers)
    print(response)

    # save response to file
    response = response.json()
    result = writefile('token.json', response)


# call this to get a new username for the bridge
# obtains bridge username and saves to json file
def getusername():
    put_url = 'https://api.meethue.com/route/api/0/config'
    put_data = json.dumps({'linkbutton':True})

    post_url = 'https://api.meethue.com/route/api'
    post_data = json.dumps({'devicetype':'light_controller'})

    token = gettoken()
    headers = {
        'Content-Type':'application/json',
        'Authorization':f'Bearer {token}'
        }

    print(f'Requests to: {post_url}')
    response = requests.put(put_url, data=put_data, headers=headers)
    response = requests.post(post_url, data=post_data, headers=headers)
    print(response)

    # write file
    response = response.json()
    result = writefile('username.json', response)


# call this to refresh the access token if it has expired
# refreshes access_token and saves to file
def refresh():

    # pull refresh token from file
    jsonContent = readfromfile('token.json')
    data = json.loads(jsonContent)
    refresh_token =  data.get('refresh_token')

    # pull client id and clientsecret from file
    jsonContent = readfromfile('myapps.json')
    data = json.loads(jsonContent)
    ClientId =  data.get('ClientId')
    ClientSecret = data.get('ClientSecret')

    # base64 encode 'ClientId:ClientSecret'
    enc_string = ClientId + ':' + ClientSecret
    enc_string_bytes = enc_string.encode("ascii")
    base64_bytes = base64.b64encode(enc_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    # define url to post
    url = 'https://api.meethue.com/v2/oauth2/token'
    data = {'grant_type':'refresh_token', 'refresh_token':refresh_token}
    headers = {
        'Authorization': f'Basic {base64_string}',
        'Content-type':'application/x-www-form-urlencoded'
        }

    # make post
    print('Refresh token')
    print(f'Post to: {url}')
    response = requests.post(url, data=data, headers=headers)
    print(response)

    # save response to file
    response = response.json()
    result = writefile('token.json', response)


# switch on light identified by lightId and xy colour
def lightOn(lightId, xy):
    # token
    token = gettoken()

    headers = {
        'Content-Type':'application/json',
        'Authorization':f'Bearer {token}'
        }

    data = {"on": True, "bri": 254, "xy": xy}
    data = json.dumps(data)

    # username
    WHITELIST_IDENTIFIER = getuser()

    # build url
    put_state_url = (
        'https://api.meethue.com/route/api/'
        f'{WHITELIST_IDENTIFIER}/lights/{lightId}/state'
        )

    # the put
    print('Put to https://api.meethue.com/route/api')
    r = requests.put(put_state_url, data=data, headers=headers)
    print(r)


# switch light on with defined blue colour
def bluelight(lightId):
    xy = [0.167, 0.04]
    lightOn(lightId, xy)


# switch light on with defined red colour
def redlight(lightId):
    xy = [0.7006, 0.2993]
    lightOn(lightId, xy)


# Use this to get a new token if it all went south!
# Run Django localhost:4001 'code snatcher'
# Must run from terminal where it will launch Chrome
# Philips will ask 'do you trust this application?'
# Must answer 'yes' to get the code allowing a fresh token
#************
# authorize()
#************

# use this to refresh access token
###########
# refresh()
###########

# swtich on numbered light as colour red
##############
# redlight(12)
##############

# switch on numbered light as colour blue
#############
#bluelight(3)
#############

# switch on numbered light as colour white
#############################
#lightOn(11,[0.4576, 0.4099])
#############################
