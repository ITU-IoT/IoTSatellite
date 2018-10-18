import urequests

def post(ip, port, path, data):
    print("Posting data to "+ip+":"+str(port)+":")
    print(data)
    try:
        r = urequests.post("http://"+ip+":"+str(port)+path, json = data)
        print("Response:")
        print(r.text)
        return r
    except Exception as e:
        print("Post failed! Error message:")
        print(repr(e))
        return None

def get(ip, port, path):
    print("Getting data from "+ip+":"+str(port))
    try:
        r = urequests.get("http://"+ip+":"+str(port)+path)
        # print("Response:")
        # print(r.text)
        return r
    except Exception as e:
        print("Get failed! Error message:")
        print(repr(e))
        return None