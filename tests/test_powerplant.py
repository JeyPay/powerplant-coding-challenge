if __name__ == '__main__':
    """A simple POST call done to the server. The server should run first"""
    import requests
    import json
    with open('example_payloads/payload3.json') as f:
        data = ''.join(f.readlines())

    r = requests.post('http://127.0.0.1:8888/productionplant', data=data)
    print(r.json())