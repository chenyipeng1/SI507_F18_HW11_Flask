from flask import Flask, render_template
import requests
import secrets_example
import json
import time

API_KEY = secrets_example.api_key

# I have implement the extra 1 and 2, and you can check.

app = Flask(__name__)

@app.route('/')
def welcome():
	return '<h1>Welcome!</h1>'

@app.route('/user/<nm>')
def hello_name(nm):
    return render_template('user.html', name = nm, section_name = None, list = find_top_data(), time = get_time())

@app.route('/user/<nm>/<section>')
def hello_name_1(nm, section):
    return render_template('user.html', name = nm, section_name = section, list = find_top_data(section), time = get_time())

CACHE_NAME = "data.json"
UNI_LIST = []

def get_top_data(section, base_url):
    try:
        with open(CACHE_NAME, 'r') as cache_file:
            cache_contents = cache_file.read()
            CACHE_DICTION = json.loads(cache_contents)
    except:
        CACHE_DICTION = {}
    
    data = CACHE_DICTION


    if base_url not in UNI_LIST:
    	# need to request data and write into json
        UNI_LIST.append(base_url)
        raw_data = requests.get(base_url + "?api-key={}".format(API_KEY)).text
        data[base_url] = json.loads(raw_data)
        dumped_json = json.dumps(data, indent = 4)
        fw = open(CACHE_NAME,"w")
        fw.write(dumped_json)
        fw.close()
    return data

def find_top_data(section = None):
    top_list = []
    # get title and url
    if not section:
        base_url = "https://api.nytimes.com/svc/topstories/v2/{}.json".format('technology')
    else:
        base_url = "https://api.nytimes.com/svc/topstories/v2/{}.json".format(section)

    re = get_top_data(section, base_url)
    for i in range(5):
        sub_list = []
        sub_list.append(re[base_url]["results"][i]["title"])
        sub_list.append(re[base_url]["results"][i]["url"])
        top_list.append(sub_list)
    return top_list

def get_time():
	localtime = time.localtime(time.time())
	return localtime[3], localtime[4]

if __name__ == '__main__':
    app.run(debug=True)


