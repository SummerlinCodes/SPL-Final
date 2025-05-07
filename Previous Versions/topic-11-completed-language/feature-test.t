// Trivial Language: Feature Test Suite

print("Feature Test Suite for Trivial Language");

// ------------------------------------------------------------
// Literals and Identifiers
// ------------------------------------------------------------
print("Testing literals and identifiers...");
x = 42;
y = -3.14;
z = "hello";
a = true;
b = false;
n = null;
assert x == 42;
assert y == -3.14;
assert z == "hello";
assert a == true;
assert b == false;
assert n == null;

// ------------------------------------------------------------
// Arithmetic Operations
// ------------------------------------------------------------
print("Testing arithmetic operations...");
assert 1 + 2 == 3;
assert 5 - 3 == 2;
assert 3 * 4 == 12;
assert 8 / 2 == 4;
assert (1 + 2) * 3 == 9;

// ------------------------------------------------------------
// Boolean and Logical Operations
// ------------------------------------------------------------
print("Testing logical operations...");
assert true and true;
assert not(false);
assert false or true;
assert !false;

// ------------------------------------------------------------
// Lists
// ------------------------------------------------------------
print("Testing lists...");
l = [1, 2, 3];
assert head(l) == 1;
assert tail(l) == [2, 3];
assert length(l) == 3;
assert l[0] == 1;

// ------------------------------------------------------------
// Objects
// ------------------------------------------------------------
print("Testing objects...");
o = {"a": 1, "b": 2};
assert o["a"] == 1;
assert o.b == 2;
assert length(keys(o)) == 2;

// ------------------------------------------------------------
// Function Definitions and Calls
// ------------------------------------------------------------
print("Testing functions...");
function add(x, y) { return x + y }
assert add(1, 2) == 3;

mult = function(x, y) { return x * y }
assert mult(3, 4) == 12;

// ------------------------------------------------------------
// Nested Blocks and Scope
// ------------------------------------------------------------
print("Testing nested blocks...");
x = 5;
if (true) {
    x = x + 1;
    if (x > 5) {
        x = x * 2
    }
}
assert x == 12;

// ------------------------------------------------------------
// While Loops
// ------------------------------------------------------------
print("Testing while loops...");
count = 0;
n = 1;
while (n < 10) {
    n = n * 2;
    count = count + 1
}
assert count == 4;

// ------------------------------------------------------------
// If Statements
// ------------------------------------------------------------
print("Testing if statements...");
if (true) {
    x = 1
} else {
    x = 2
}
assert x == 1;

if (false) {
    x = 10
} else {
    x = 20
}
assert x == 20;

// ------------------------------------------------------------
// Return Statements
// ------------------------------------------------------------
print("Testing return...");
function constant() { return 99 }
assert constant() == 99;

function conditional(x) {
    if (x > 0) {
        return 1
    };
    return 0
}
assert conditional(1) == 1;
assert conditional(-1) == 0;

// ------------------------------------------------------------
// Built-in Functions
// ------------------------------------------------------------
print("Testing built-in functions...");
assert head([10,20,30]) == 10;
assert tail([10,20,30]) == [20,30];
assert length([1,2]) == 2;
assert keys({"x": 1}) == ["x"];

// ------------------------------------------------------------
// Assignment Expressions
// ------------------------------------------------------------
print("Testing assignment expressions...");
a = b = c = 7;
assert a == 7;
assert b == 7;
assert c == 7;

// ------------------------------------------------------------
// Complex Access
// ------------------------------------------------------------
print("Testing complex access...");
obj = {"list": [0,1,2], "value": {"inner": 5}};
assert obj["list"][1] == 1;
assert obj.value.inner == 5;

print("Feature test complete.");
