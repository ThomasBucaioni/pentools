# MitmProxy

Sources:
- https://www.packtpub.com/product/learning-python-web-penetration-testing-video/9781785280351
- https://www.mitmproxy.com

## Http requests

Add a header to all responses:
```
def response(context, flow):
    flow.response.headers["my-fake-header"] = "fake"
```

Log all the requests:
```
def request(context, flow)
    f = open('httplogs.txt', 'a+')
    f.write(flow.request.url + '\n')
    f.close()
```

Remove duplicates:
```
global history
history = []
...
    global history
    url = flow.request.url
    if url not in history:
        ...
    else
        pass
```

## SQLi

```
import urlparse
...
    a = urlparse.urlparse(url)
    query = a.query.split('&')
    qlen = len(query)
    while qlen:
        queries = deepcopy(query)
        queries[qlen-1] = queries[qlen-1].split('=')[0] + '=injection_placeholder'
        newquery = '&'.join(queries)
        url_to_test = a.scheme + '://' + a.netloc + '?' + newquery
        qlen -= 1
        for injection in injection_vector:
            req = requests.get(url_to_test.replace('injection_placeholder', injection))
            print(req.content)
            for err in errors:
                if req.content.find(err) != -1:
                    res = req.url + ";" + err
                    f.write(res)
    f.close()
...
```
