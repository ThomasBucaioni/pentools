# Python reminder

## Data

### Images

```
from wand.image import Image
fin = input("Enter file name: ")
fout = fin.replace(".jpg",".png")
with open(fin,"rb") as f:
  image_blob = f.read()
  with Image(blob=image_blob) as img:
     img.format = 'png'
     img.save(filename=fout)
f.close()
```

### Linked list

```
linky = [["FirstPointer",0,0,"",""]]
```

### Graph

```
nodes = []
nodes.append(["node1",[("node2",66), ("node3",48),("node10",29)]])
```

### DB

```
from dataclasses import dataclass
@dataclass
class myclass:
    mystring: str
    myint: int
    mylist: list
myinstance = myclass("somestring", 0, ['mylist', 1, {mydict: true}])
type(myinstance) # <class '__main__.myclass'>

import sqlite3
from os.path import exists
if not exists("mydb.db"):
  print("Creating database")
conn = sqlite3.connect("mydb.db")

sq = 'create table if not exists myclass(mystring text not null, myint int)
status = conn.execute(sq)
sq = 'create table if not exists mylist(somestring text not null, someint int, somedict takesalinktoanothertablenoinsertionpossible)'
status = conn.execute(sq)
curse = conn.cursor()
sq = "insert into myclass(somestring, someint) values ('sometext', 0);"
curse.execute(sq)
conn.commit()
curse.close()
conn.close()
# get a db admin job
```

### Json and Xml

#### Xml

https://developer.mozilla.org/en-US/docs/Web/XML/XML_introduction
```
import xml.etree.ElementTree as et
tree = et.parse('file.xml')
root = tree.getroot()
print(len(root))

print(root.tag)
print(root[0].tag)
print(root[0][0].text)

for i in range(len(root)):
    print(root[i][0].text)
```

#### Json

- https://www.json.org/json-en.html
- https://docs.python.org/3/library/json.html

```
import json
f = open("somefile.json","r")
json.load(f)
type(somefile)
```

