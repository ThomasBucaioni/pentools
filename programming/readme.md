# Programming

## LUA

https://www.packtpub.com/product/lua-quick-start-guide/9781789343229

### Hello World

Repl:
```
$ sudo apt-get install lua
$ lua
> print("Hello World")
```
Script:
```
$ lua hello.lua
```

### Variables

```
foo = "bar"
print(foo)
foo = 2
print(foo)
```

### Comments

```
-- This is commented
```

### Types

Nil, booleans, numbers, strings, functions, table(hash), complex structures, thread(parallel executions)
```
foo = nil
print(foo)
if true then
    print(math.floor(1.41)
else
    print(math.ceil(3.14)
end
print(type(somevar))
stringlength1 = #"some string"
stringlength2 = string.len("some string") -- same as `#`
concatstring = "Hello" .. " " .. "world"
convertedinteger = "This is number three: " .. 3
convertedstring = "001" + 1 -- equals 2
escapechar = "This is an escape quote: \""
otherchars = "\n\t\\" -- Even more escape chars: https://www.lua.org/pil/2.4.html
some_user_input = io.read()
```

### Scopes

Tutorials: http://lua-users.org/wiki/ScopeTutorial
```
var1 = "This is global var1"
var2 = "This is global var2"
do
    local var2 = "This is a local var2"
    print(var2) -- local shadowed print
end
```

### Functions

```
function PrintsSomething()
    a = "Hello"
    b = "world"
    print(a .. " " .. b)
end
PrintsSomething()

function add_func(a,b)
    print(a + b)
end
add_func(1,2)
add_func(1,2,3,4) -- ignored

function returning_func(a)
    return a + 2
end 
result = returning_func(1)
print(result)

function multiple_returns(a)
    return a, a+1, a+2
end
a, b, c = multiple_returns(1)
a = multiple_returns(1) -- discarded
```

### Operators

```
a = 2^3
b = 8
a ~= b -- false
c = true and false
c == false -- true
d = 1 and 2 -- value is 2...
e = 1 or 2 -- value is 1...
```

### Control

```
if a ~= b then
    print("a is not b")
elseif c == d
    print("c is d")
else
    print('else case')
end

if true then
    if false then
        print("Bug")
    end
end
```

### Loops

```
i = 10
while i > 0 do
    print("i = " .. i)
    i=i-1
    if i == 5 then
        break
    end
end

i = 10
repeat
    print("Eat, sleep, rave, repeat")
    i = i-1
until i < 0

for i=0,10,2 do
    print(i)
end

for i=10,0,-3 do
    print(i)
end
```

### Tables and objects

#### Tables

```
tbl = {}

tbl["key1"] = 1
x = "key1"
tbl[x] == tbl["key1] -- true

key2 = 2
tbl[key2] = "The key is a number and the value is a string"
print(tbl[2])

tbl.key1 -- dot syntax

colors = {
    red = "#ff0000",
    green = "#00ff00",
    blue = "#0000ff"
}
print(colors.red, colors.green, colors.blue)

a = {}
b = a
a.x = 1
b.x = 2 -- changes table `a`
```

#### Arrays

```
arr = {}
arr[1] = "x"
arr[2] = "y"
arr[3] = "z"
for i = 1, 3 do
    print(arr[i])
end

arr = { "Monday", "Tuesday", "Wednesday" }

vector = { [0] = "zero index", "index 1", "index 2", "index 3" } -- vector has index 0

sparsearr = {}
sparsearr[1] = 1
sparsearr[10] = 10
for i = 1, 10 do
    print(arr[i])
end

for i = 1,#arr do
    print(arr[i]) -- stops at 1...
end

matrix = {}
matrix[1] = {}
matrix[1][1] = 1
matrix[2] = {}
matrix[2][2] = 1
```

#### Iterating

```
arr = { "x", "y", "z" }
for i, v in pairs(arr) do
    print("The key is " .. i .. " and the value is " .. arr[i])
end
```

#### Closures

```
function NextNumber()
    local currentNumber = 0
    return function () -- anonymous function
        currentNumber = currentNumber + 1
        return currentNumber
    end
end
next = NextNumber()
print(next()) -- prints 1
print(next()) -- prints 2
print(next()) -- prints 3
```


## Ruby

https://www.packtpub.com/product/learn-to-code-with-ruby-video/9781788834063

### Hello World

In `hello.rb` (interpreted):
```
puts "Hello World"
```
Run: 
```
$ ruby hello.rb
```
Repl: 
```
$ irb
```

### Basics

#### Puts
```
puts "Newline included in the `puts` method"
puts 0
puts 1.4142
puts 1+1
# puts "1" + 1 # No conversion
puts "1" + "1" # Concatenation
puts # simple line break
```

#### Print
Does not add a line break:
```
print "Hello" # No line break
print " "
print "World"
```

#### Method `p`
Adds more information:
```
p "Some string 
with a line break"
```

#### Arithmetic

```
p 1+2
p 2-1
p 10/2
p 11/2 # Integer division, no remainder
p 11.0/2 # Floating point division
p 11/2.0
p 2**10 # equals 1024
p 5%2 # remainder
p 0.1 # `p .1` not working
p -1
```

#### Comment

```
# This is commented out
=begin
And this will be commented too
=end
```

#### Variables
Typing is dynamic:
```
a=1
b=2
p a+b
c="Some string"
p c # with quotes
puts c # no quotes
```

#### Parallel assignment

```
a, b, c, d = 10, 20, 30
p a, b, c, d # d => nil
a, b = b, a
```

#### Constants

```
PI = 3.14159
```

#### Methods

```
a = "someString"
a.upcase
a.downcase
a.length
MSQRT2 = -1.4142
MSQRT2.abs
MSQRT2.truncate
b = 1
b.next
p -1.next # equals 0
puts "SomeString".inspect
p "SomeString" # same as `puts "SomeString".inspect`
```

#### Return and Nil

Nil ~ emptyness
```
irb> 4 # returns 4
irb> 4+3 # returns 7
irb> puts 4+3 # prints 7 and returns `nil`
irb> puts nil # prints nothing and returns `nil`
irb> p nil # prints `nil` and returns `nil`
```

#### String interpolation

```
p 5.to_s # prints a string
p '5'.to_i # prints an integer
a = 'World'
p "Hello #{a}" # replaces `a`
a = 1
p "Result is #{a+1}" # converts `a+1` to a string
```

#### Gets and Chomp

```
irb> gets # waits for a keyboard input
irb> a = gets # `a` stores the keyboard input with a line break
irb> a = gets.chomp # without the line break
irb> a = gets.chomp.to_i # converts the input to an integer
```

### Numbers and booleans

#### `.class` Method

```
p 1234.class # returns `Integer`
p "Hello".class # returns `String`
p true.class # returns `TrueClass`
p 123.4.class # returns `Float`
```

#### Conversions

```
a = '1'
a.to_i
a.to_i.class # Integer
a = 1
a.to_s
a.to_s.class # String
a = 1.23
a.to_i # rounded down (truncated)
1.23.to_f # no changes
```

#### Booleans

```
1 > 2
1 < 2
b = 1<2
p b # prints `true`
a = false
a & b # is `false`
a | b # is `true`
```

#### Boolean methods

```
1.even? # returns `false`
1.odd? # returns `true`
```

#### Comparisons

```
a = 1
b = 2 
a == b
a != b
a > b
a >= b
a < b
a <= b
a == 1.0 # is `true`
"Hello".downcase == "hello" # is `true`
"123" == 123.to_s # is `true`
```

#### Arithmetic methods and arguments

Operators (methods): `+`, `-`, `*`, `/`, `%`
```
1 + 2 == 1.+(2) # replaced by the Ruby interpreter
10 - 5 == 10.-(5) # same
10.- 5 # allowed but not recommended
10.div(5) == 10./(5) # and same as `10 / 5`
10.%(3) == 10.modulo(3) # and same as `10 % 3`
```

#### Between methods

```
2.between?(1,3) # is `true`
'b'.between?('a','c') # is `true`
1.1.between?(1,1.11) # is `true`
```

#### Float methods

```
10.5.floor
10.5.ceil
10.4.round # is 10
10.5.round # is 11
10.1234.round(2) # is 10.12
10.1298.round(2) # is 10.13
```

#### Assignments

Alternatives: `+=`, `-=`, `*=`, `/=`, `**=`

#### Blocks

```
5.times { p "Hello" } # prints 5 times "Hello"
5.times do p "Hello" end # same
5.times do |counter|
p "Hello #{counter}"
p "again"
end # `counter` is a local variable only
5.times { |anothercounter| puts "The counter value is: #{anothercounter}" }
```

#### Upto and Downto Methods

```
5.downto(0) { |i| puts "Counter: #{i}" }
5.upto(10) { |i| puts "Counter: #{i}" }
5.downto(0) do |i|
puts "Counter: #{i}"
end # same
```

#### Step Method

```
1.step(100, 2) { |i| puts "#{i}" } # prints odd numbers from 1 to 100
0.step(100, 7) { |i| puts i }
```

### Strings

#### Creation

```
emptystring = ""
a = String.new("Some string") # same as `a = "Some string"`
```

#### Multiline

```
a = "Some\nString"
puts a # two lines
words = <<EOL
line 1
line 2
EOL # same as Bash. Takes TABs too
```

#### Escape character

```
puts "Hello \"World\""
puts "Hello \tWorld\n"
puts 'Hello \'World\''
```

#### Single quotes

```
puts 'Hello\nWorld' # not escaped
a = "string"
puts '#{a}' # does Not work
```

#### Comparison

```
"Hello" == "hello" # false
"a" < "b" # true
'a' < 'B' # false
```

#### Concatenation

```
a = "Hello"
b = " "
c = "World"
puts a + b + c
a.prepend(b).prepend(c)
```

#### Methods `.length` and `.size`

```
a = "Hello World"
a.length
a.size
```

#### Extraction and slicing

```
a = 'Some string'
a[-2]
a.slice(3) # char at position 3, same as `a[3]`
a[0, 5] # first 5 chars
a[-5,5] # last 5 chars
a[3..7]
a.slice(3..7) # same as `a[3..7]`
a.slice(3...7) # excluded
a[5..-2]
```

#### Overwrite

```
a = 'Another string'
a[0] = 'B'
a[0..8] = 'Just another '
```

#### Case methods

```
"Hello".capitalize
"Hello".upcase
"Hello".downcase
"HeLlO".swapcase
```

#### Reverse method

```
"Hello".reverse
```

#### Bang method

With a `!`: 
```
a = 'string'
a.capitalize # `a` is not modified
p a # not capitalized
a.capitalize! # `a` is modified
p a # capitalized
```

#### Method `include?`

```
"Hello".include?('ll') # true
```

#### Empty and nil

```
"".empty? # true
nil.nil? # true
```

### Methods and conditionals

#### Collection of code, reusable

DRY: Don't Repeat Yourself
```
def some_function(func_param)
    a = 'Hello ' + func_param.to_s # local variable, invisible outside
    puts "Returning: #{a}"
    return a # terminates the execution
end
a = some_function('world')
```

#### Implicit return

```
def some_func(num1, num2)
    num1 + num2 # returned implicitly
end
def returns_nil()
end
def returns_nil_to()
    puts "Some string"
end
```

#### Falsiness

Only `false` and `nil` are false:
```
if [] || nil || false # empty array `[]` is `true`
    p "This is printed"
elseif {} && "" # empty hash is `true`, empty string is `true`
    p "This in never printed"
else
    p "This neither"
end
```

#### Method `.respond_to?`

```
a = 1
a.respond_to?("odd?") # true
a.respond_to?(:odd?) # true
b = "String"
b.respond_to?("length") # true
b.respond_to?(:length) # true
```

#### Ternary

```
p 1<2?"This is true":"This is false"
```

#### Default/optional parameters

```
def some_func(param1 = 1, param2 = 2)
    param1 + param2
end
```


