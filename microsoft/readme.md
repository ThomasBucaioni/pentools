# Microsoft Windows attacks

## Cmd

```
forfiles /P C:\Windows /S /M *.txt /c "cmd /c echo @PATH"
```

## WebDAV

```
pip install wsgidav
mkdir mywebdav
.local/wsgidav --host=0.0.0.0 --auth=anonymous --port 80 --root ./mywebdav
```


