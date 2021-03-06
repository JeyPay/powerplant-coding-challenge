if __name__ == '__main__':
    import requests
    import json
    with open('example_payloads/payload1.json') as f:
        data = ''.join(f.readlines())

    r = requests.post('http://127.0.0.1:8888/productionplant', data=data)
    print(r.json())