# Javascript

## Variables

### Objects

```
const obj = {
  foo: 1,
  propertyEnumerable() {
    return false;
  },
};

obj.propertyEnumerable(); // false; expected result
obj.foo; // 1
```

### Other

#### Declaration

```
var text = "Some text"
var globalscope = 'blue'
function foo(){
    globalscope = 'green'
}
foo();
console.log(globalscope) // 'green'

let num = 10
num = 20

const name = '3.14'

"use strict";
var let = 2 // error
```

#### Operators
```
num1 = 1
num2 = 2
num3 = num1 + num2 // 3

st1 = '1'
st2 = '2'
st3 = st1 + st2 // '12'

const seq = [1, 2, 3]
const stseq = ['1', '2', '3']
console.log(seq[0])

var a = true; // bool
if(a){console.log("True")}
```
Arrays: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array

## Functions

### Built-in

```
const myFalse = new Boolean(false); // initial value of false
const g = Boolean(myFalse); // initial value of true
const myString = new String("Hello"); // string object
const s = Boolean(myString); // initial value of true

var st = "example "
st = st.trim()
st.length
st.concat(' ', 'concat')
```
Tutorials: https://developer.mozilla.org/en-US/docs/Web/JavaScript

### Example
```
function padZeros(num, totalLen) {
  let numStr = num.toString(); // Initialize return value as string
  const numZeros = totalLen - numStr.length; // Calculate no. of zeros
  for (let i = 1; i <= numZeros; i++) {
    numStr = `0${numStr}`;
  }
  return numStr;
}
```

## Conditionals

```
var randomNum = parseInt(Math.random()*10)
switch(randomNum) {
 case 0:
   console.log("Number is 0")
   break // !!
 case 1:
   console.log("Number is 1")
   break
 case 2:
   console.log("Number is 2")
   break
 case 3:
   console.log("Number is 3")
   break
 case 4:
   console.log("Number is 4")
   break
 default:
   console.log("Number is 5 or higher")
}
```

## Loops

```
for (count = 1; count < 10; count++) {
  console.log(count)
}

var count = 1
while (count < 10) {
  console.log(count);
  count=count+1;
}
console.log(count);



```

APIs: https://developer.mozilla.org/en-US/
