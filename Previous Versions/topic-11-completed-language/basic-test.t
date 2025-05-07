// This is a test suite for the Trivial language. 

print("Trivial Language Test Suite");

print "Testing basic values...";
x = 1;
assert x == 1;
assert not(x == 3);

x = -123.456;
assert x == -123.456;

x = "alpha";
assert x == "alpha";
print x;

x = true;
assert x == true;
assert x == not(false);
x = false;
assert x == false;
assert x == not(true);

print "Testing complex values";
x = [1,2,3];
print(x);
assert x == [1,2,3];
assert not (x == [1,2,4]);

x = { "a":1, "b":2 };
assert x == { "a":1, "b":2 };
assert not (x == { "a":1, "b":3 });
print(x);

print "Testing operations...";

// addition
assert 1+2 == 3;
assert "dog" + "cat" == "dogcat";
assert [1,2] + [3,4] == [1,2,3,4];
assert {"dog":1} + {"cat":2} == {"dog":1, "cat":2};
assert {"dog":1, "cat":2} + {"cat":3} == {"dog":1, "cat":3};
x = {"dog":1};
x["dog"] = x["dog"] * 2;
assert x == {"dog":2};
x.cat = 3;
x.cat = x.cat * 2;
assert x == {"dog":2, "cat":6};

// subtraction
assert 4-1 == 3;

// multiplication
assert 4 * 5 == 20;
assert 0.4 * 5 == 2.0;
assert "dog" * 2 == "dogdog";
assert 2 * "dog" == "dogdog";

// division
assert 6/2 == 3;
assert 5.5 / 0.5 == 11.0;

// comparison
assert 1==1;
assert not(1==2);
assert "dog" == "dog";
assert not("dog" == "cat");
assert [1,2,3] == [1,2,3];
assert not([1,2,3] == [1,2,4]);
assert {"a":1} == {"a":1};
assert not({"a":1} == {"a":2});

assert 1!=2;
assert not(1!=1);
assert "dog" != "cat";
assert not("dog" != "dog");
assert [1,2,3] != [1,2,4];
assert not([1,2,3] != [1,2,3]);
assert {"a":1} != {"a":2};
assert not({"a":1} != {"a":1});

assert 1 < 2;
assert not(2 < 1);
assert 1 <= 2;
assert 2 <= 2;
assert not(2 <= 1);

assert 3 > 2;
assert not(2 > 3);
assert 3 >= 2;
assert 2 >= 2;
assert not(2 >= 3);


print "Testing block statement lists...";

if (true) {
    if (1) {x=1}
    if (1) {x=1; x=2}
    if (1) {x=1; x=2};
    if (1) {x=1;;; x=2;}
    x=4
}
assert x == 4;

print "Testing control structures...";

x = 2;
if (x < 3) {
    x = x + 4
} else {
    x = x + 5
}
assert x == 6;

x = 0; y = 1;
while (y < 64) {
    y = y * 2;
    x = x + 1
}
assert x == 6;

print "Testing functions...";

function add(x, y) { return x + y }
assert add(2,3) == 5;

sub = function(x,y) { return x - y}
assert sub(5,3) == 2;

print "Done."
