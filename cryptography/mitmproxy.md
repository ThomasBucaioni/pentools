# MitmProxy

https://www.mitmproxy.com

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

```
