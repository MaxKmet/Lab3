
import requests
import sys
from requests_oauthlib import OAuth1


def navigate(original_data, cur_data, prev_steps):
    '''
    original_data - json data got from the Twitter request
    cur_data - a part of the data currently worked on(=original data at the beginning)
    prev_steps - list of steps to add possibility of step back([] at the beginning)
    '''
    val = ""
    if(isinstance(cur_data, list)):
        if(len(cur_data) > 0):
            print("\n\n\nYou are in the chosen list\n")
            print('Input the index of the list element to navigate to: \n')
            print('The integer must be between 0 and ' + str(len(cur_data) - 1))
            print('Input ".." to navigate a step back\nInput "exit" to stop the program' + "\nInput: ")
            val = input()
            if(not (val.isdigit() and (0 <= int(val) < int(len(cur_data))))):
                pass
            else:
                prev_steps.append(int(val))
                navigate(original_data, cur_data[int(val)], prev_steps)

        else:
            print('You have navigated to the empty item. Please input ".." to navigate a step back')
            navigate(original_data, cur_data, prev_steps)
    elif(isinstance(cur_data, dict)):
        print("\n\n\nYou are in the chosen dictionary.\nInput the next level to navigate to from here from the list below:")
        for k in cur_data.keys():
            print(k)
        print('Or Input ".." to navigate a step back\nInput "exit" to stop the program\nInput:')
        val = input()
        if not val in cur_data.keys():
            print("Entered value is not in list\n")
        else:
            prev_steps.append(val)
            navigate(original_data, cur_data[val], prev_steps)
    else:
        print("\n\nData:\n" + str(cur_data))
        print('Input ".." to navigate a step back\ninput "exit" to stop the program\n')
        val = input()
        if(val):
            pass
    if(val == ".."):
        cur_data = original_data
        for step in prev_steps[:-1]:
            cur_data = cur_data[step]

        navigate(original_data, cur_data, prev_steps[:-1])
    elif(val == "exit"):
        sys.exit()
    else:
        print("Invalid input\n\n")
        navigate(original_data, cur_data, prev_steps)


if __name__ == "__main__":

    API_KEY = ''  # enter your own
    API_SECRET = ''  # enter your own
    ACCESS_TOKEN = ''  # enter your own
    ACCESS_TOKEN_SECRET = ''  # enter your own

    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    requests.get(url, auth=auth)

    r = requests.get(
        'https://api.twitter.com/1.1/friends/list.json?screen_name=imaginedragons', auth=auth)

    navigate(r.json(), r.json(), [])
