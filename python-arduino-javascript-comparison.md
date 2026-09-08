# Python, Arduino C++, and JavaScript

This guide compares programming concepts in Python, Arduino C++, and JavaScript.
- **Python**, running as a script or application on a computer
- **Arduino C++**, compiled and uploaded to a microcontroller
- **JavaScript**, used here inside a Node-RED Function node

## Table of contents

- [1. The most important differences](#1-the-most-important-differences)
- [2. Essential syntax](#2-essential-syntax)
- [3. Variables and types](#3-variables-and-types)
- [4. Operators](#4-operators)
- [5. Conditions](#5-conditions)
- [6. Lists and arrays](#6-lists-and-arrays)
- [7. Dictionaries, structures, and objects](#7-dictionaries-structures-and-objects)
- [8. Loops](#8-loops)
- [9. Functions](#9-functions)
- [10. Scope and state](#10-scope-and-state)
- [11. Built-ins and libraries](#11-built-ins-and-libraries)
- [12. The Node-RED `msg` object](#12-the-node-red-msg-object)
- [13. Errors and debugging](#14-errors-and-debugging)

## 1. The most important differences

| Aspect | Python | Arduino C++ | Node-RED Function node |
|---|---|---|---|
| Where it runs | Computer, server, or single-board computer | Microcontroller | Inside the Node-RED runtime[^node-red-hosting] |
| How it starts | The interpreter executes a script | The compiled sketch starts when the board powers on or resets | A message arrives at the Function node |
| Repetition | Written explicitly with a loop or scheduler | Arduino repeatedly calls `loop()` | Node-RED invokes the function once for each incoming message |
| Translation | Interpreted at run time | Compiled before upload | Interpreted or just-in-time compiled by the JavaScript engine |

[^node-red-hosting]: For example, Node-RED can run locally, on an edge device, or as a container image on a cloud platform.

### Program structure

### Python

A Python script normally executes from top to bottom and repetions needs to expliciity written:

```python
value = 10
result = value * 2

while True:
    # Some code
```

### Arduino C++

An Arduino sketch has two required functions:

```cpp
void setup() {
  // Runs once when the board starts or resets.
}

void loop() {
  // Runs repeatedly.
}
```

### JavaScript in a Node-RED Function node

The code runs once for each incoming message:

```javascript
const value = Number(msg.payload);
const result = value * 2;

msg.payload = result;
return msg;
```

Node-RED provides `msg`. The code reads properties from this object, performs ordinary JavaScript operations, and can return the message to the flow.



## 2. Essential syntax

| Concept | Python | Arduino C++ | JavaScript |
|---|---|---|---|
| Comment | `# comment` | `// comment` | `// comment` |
| Variable | `value = 10` | `int value = 10;` | `let value = 10;`[^var-let] |
| Constant | `LIMIT = 100` by convention | `const int LIMIT = 100;` | `const LIMIT = 100;` |
| True and false | `True`, `False` | `true`, `false` | `true`, `false` |
| Equality | `a == b` | `a == b` | `a === b` preferred |
| Logical AND | `and` | `&&` | `&&` |
| Logical OR | `or` | `\|\|` | `\|\|` |
| Logical NOT | `not` | `!` | `!` |
| Code blocks | Indentation | Braces `{ }` | Braces `{ }` |
| Statement ending | Newline | Semicolon `;` | Semicolon `;` is recommended |

[^var-let]: `var` and `let`: Both declare variables in JavaScript. `var` is function-scoped, while `let` is block-scoped. In simple Node-RED Function-node code, they often behave the same. `var` is common in older examples, while `let` provides more precise scope control.

C++ and JavaScript require parentheses around conditions and use braces for blocks:

```python
if value > 10:
    result = value * 2
```

```cpp
if (value > 10) {
  result = value * 2;
}
```

```javascript
if (value > 10) {
    result = value * 2;
}
```

## 3. Variables and types

Python and JavaScript determine types from values. C++ requires explicit types.

```python
count = 5
temperature = 21.5
name = "sensor_1"
is_active = True
```

```cpp
int count = 5;
float temperature = 21.5;
const char* name = "sensor_1";
bool isActive = true;
```

```javascript
let count = 5;
const temperature = 21.5;
const name = "sensor_1";
let isActive = true;
```

In JavaScript, use `const` when a variable will not be reassigned and `let` when it will change.

Common Arduino C++ types include:

| Type | Use |
|---|---|
| `bool` | `true` or `false` |
| `int` | Whole numbers |
| `unsigned long` | Non-negative counters and time values such as `millis()` |
| `float` | Values with a fractional part |
| `char`, `char[]`, `const char*` | Characters and character-based text |
| `String` | Arduino string object |


## 4. Operators

Most arithmetic operators are the same:

| Operation | Python | Arduino C++ | JavaScript |
|---|---|---|---|
| Addition | `a + b` | `a + b` | `a + b` |
| Subtraction | `a - b` | `a - b` | `a - b` |
| Multiplication | `a * b` | `a * b` | `a * b` |
| Division | `a / b` | `a / b` | `a / b` |
| Remainder | `a % b` | `a % b` | `a % b` |
| Exponentiation | `a ** b` | `pow(a, b)` | `a ** b` |
| Add one | `a += 1` | `a++` or `a += 1` | `a++` or `a += 1` |

### C++ integer division

In C++, the operand types affect division:

```cpp
int whole = 7 / 2;         // 3
float result = 7.0 / 2.0; // 3.5
```

Python and JavaScript produce `3.5` for `7 / 2`.

### JavaScript equality

Prefer strict equality in JavaScript:

```javascript
value === 5
value !== 5
```

Unlike `==` and `!=`, these operators do not convert the operands to matching types before comparison.

## 5. Conditions

```python
if value > 80:
    status = "high"
elif value > 60:
    status = "warning"
else:
    status = "normal"
```

```cpp
const char* status;

if (value > 80) {
  status = "high";
} else if (value > 60) {
  status = "warning";
} else {
  status = "normal";
}
```

```javascript
let status;

if (value > 80) {
    status = "high";
} else if (value > 60) {
    status = "warning";
} else {
    status = "normal";
}
```

Python uses `elif`; C++ and JavaScript use `else if`.

## 6. Lists and arrays

Python lists and JavaScript arrays can grow dynamically:

```python
values = [18.2, 19.1, 20.0]
values.append(21.3)
first = values[0]
number_of_values = len(values)
```

```javascript
const values = [18.2, 19.1, 20.0];
values.push(21.3);
const first = values[0];
const numberOfValues = values.length;
```

A basic C++ array has a fixed size and one element type:

```cpp
float values[] = {18.2, 19.1, 20.0};
float first = values[0];
const int numberOfValues = sizeof(values) / sizeof(values[0]);
```

All three use index `0` for the first element.

## 7. Dictionaries, structures, and objects

A Python dictionary and a JavaScript object both store named values:

```python
measurement = {
    "value": 21.5,
    "unit": "°C",
    "valid": True,
}

value = measurement["value"]
```

```javascript
const measurement = {
    value: 21.5,
    unit: "°C",
    valid: true
};

const value = measurement.value;
```

A C++ `struct` defines the name and type of each field:

```cpp
struct Measurement {
  float value;
  const char* unit;
  bool valid;
};

Measurement measurement = {21.5, "°C", true};
float value = measurement.value;
```

Some Arduino libraries provide other data structures. For example, an ArduinoJson document supports key-based access, but it is a library type rather than a built-in C++ dictionary.

```cpp
#include <ArduinoJson.h>

JsonDocument measurement;

measurement["value"] = 21.5;
measurement["unit"] = "°C";
measurement["valid"] = true;
```

## 8. Loops
### Python
Using index:
```python
values = [18.2, 19.1, 20.0]
total = 0

for i in range(len(values)):
    total += values[i]
```

Iterating directly over the values:
```python
values = [18.2, 19.1, 20.0]
total = 0

for value in values:
    total += value
```

### Arduino C++
Using index:
```cpp
float values[] = {18.2, 19.1, 20.0};
const int numberOfValues = sizeof(values) / sizeof(values[0]);
float total = 0;

for (int i = 0; i < numberOfValues; i++) {
  total += values[i];
}
```
alternative using `size_t`:
```cpp
float values[] = {18.2, 19.1, 20.0};

const size_t numberOfValues =
    sizeof(values) / sizeof(values[0]);

float total = 0;

for (size_t i = 0; i < numberOfValues; i++) {
  total += values[i];
}
```

Iterating directly over the values:
```cpp
float values[] = {18.2, 19.1, 20.0};
float total = 0;

for (float val : values) {
  total += val;
}
```
### JavaScript
Using index:
```javascript
const values = [18.2, 19.1, 20.0];
let total = 0;

for  (let i = 0; i < values.length; i++) {
    total += values[i];
}
```
Iterating directly over the values:
```javascript
const values = [18.2, 19.1, 20.0];
let total = 0;

for (const value of values) {
    total += value;
}
```


## 9. Functions

```python
def celsius_to_kelvin(celsius):
    return celsius + 273.15
```

```cpp
float celsiusToKelvin(float celsius) {
  return celsius + 273.15;
}
```

```javascript
function celsiusToKelvin(celsius) {
    return celsius + 273.15;
}
```

C++ declares the return type and parameter types. Python and JavaScript do not require them.

A function does not have to return a useful value:

- Python implicitly returns `None` if no `return` statement is used.
- A C++ function that returns nothing is declared with `void`.
- A JavaScript function without `return` produces `undefined`.

A Python script and an Arduino sketch are not required to return anything.

## 10. Scope and state

A variable declared inside a function is local to that function.

#### Python

```python
def celsius_to_kelvin(celsius):
    kelvin = celsius + 273.15
    return kelvin
```

#### Arduino C++

```cpp
float celsiusToKelvin(float celsius) {
  float kelvin = celsius + 273.15;
  return kelvin;
}
```

#### JavaScript

```javascript
function celsiusToKelvin(celsius) {
    const kelvin = celsius + 273.15;
    return kelvin;
}
```

In all three examples, both the parameter (`celsius`) and `kelvin` are local to the function. JavaScript `let` would also work here, but `const` communicates that `kelvin` will not be reassigned.

Variables declared outside a function have a wider scope. Use wider scope only when the value must be shared or retained.

#### Python

```python
ZERO_DEGREES_IN_KELVIN = 273.15

def celsius_to_kelvin(celsius):
    kelvin = celsius + ZERO_DEGREES_IN_KELVIN
    return kelvin
```

#### Arduino C++
```cpp
const float ZERO_DEGREES_IN_KELVIN = 273.15;

float celsiusToKelvin(float celsius) {
  float kelvin = celsius + ZERO_DEGREES_IN_KELVIN;
  return kelvin;
}
```

#### JavaScript
```javascript
const ZERO_DEGREES_IN_KELVIN = 273.15;

function celsiusToKelvin(celsius) {
    const kelvin = celsius + ZERO_DEGREES_IN_KELVIN;
    return kelvin;
}
```

### Arduino sketch
In an Arduino sketch, a variable declared outside `setup()` and `loop()` can retain its value between calls to `loop()`:

```cpp
unsigned long sampleCount = 0;

void loop() {
  sampleCount++;
}
```
### Node-RED
Variables declared with `const`,`let` or `var` in the body of a Node-RED Function node are created again for each incoming message. Node-RED provides context when a value must persist between messages; context is a Node-RED feature rather than a JavaScript language feature.

## 11. Built-ins and libraries

The three environments provide similar operations through different names and mechanisms.

Python imports a module:

```python
import math

root = math.sqrt(16)
```

Arduino C++ includes a library header before compilation:

```cpp
#include <math.h>

float root = sqrt(16.0);
```

JavaScript provides built-in objects such as `Math`, `Number`, `Array`, and `JSON`:

```javascript
const root = Math.sqrt(16);
```

Additional libraries available to Arduino C++ depend on what is installed and included in the sketch. Additional modules available to JavaScript in a Function node depend on the Node-RED configuration.

## 12. The Node-RED `msg` object

`msg` is an ordinary JavaScript object supplied by Node-RED.

```javascript
const value = msg.payload;
```

Nested properties use ordinary JavaScript object syntax:

```javascript
const value = msg.payload.measurement.value;
```

The equivalent access in a Python dictionary would be:

```python
value = msg["payload"]["measurement"]["value"]
```

A common Function-node pattern is:

```javascript
const value = Number(msg.payload.measurement.value);
const result = Math.sqrt(value);

msg.payload = result;
return msg;
```

The calculation is ordinary JavaScript. Assigning the result to `msg.payload` and returning `msg` passes the modified message to the next node.

## 13. Errors and debugging

The environments report problems at different stages.

| Environment | Common problem | Example or symptom |
|---|---|---|
| Python | Undefined name or incorrect indentation | `NameError` or `IndentationError` |
| Arduino C++ | Missing type, semicolon, declaration, or incompatible value | Compilation fails before the sketch is uploaded |
| Arduino hardware | Incorrect pin, connection, timing, or initialization | The sketch runs but the observed behavior is wrong |
| JavaScript | Unexpected conversion or missing property | A result becomes `NaN` or `undefined` |
| Node-RED Function node | Incorrect message structure or missing returned message | A property cannot be read or no message continues in the flow |

### Inspect types and values

Python:

```python
print(type(value), value)
```

Arduino C++:

```cpp
Serial.print("value = ");
Serial.println(value);
```

JavaScript can inspect a value with `typeof` and test converted numbers with `Number.isFinite(...)`:

```javascript
const value = Number(msg.payload);
const valueType = typeof value;
const isValidNumber = Number.isFinite(value);
```

### Validate values at boundaries

Python commonly handles a failed conversion with an exception:

```python
try:
    value = float(text)
except ValueError:
    print("Expected a numeric value")
```

Arduino programs commonly test conditions or status values explicitly:

```cpp
if (value < minimum || value > maximum) {
  isValid = false;
}
```

JavaScript can test the result after conversion:

```javascript
const value = Number(text);

if (!Number.isFinite(value)) {
    throw new Error("Expected a numeric value");
}
```