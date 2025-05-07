from tokenizer import tokenize
from parser import parse
from pprint import pprint
import copy

def type_of(*args):
    def single_type(x):
        if isinstance(x, bool):
            return "boolean"
        if isinstance(x, int) or isinstance(x, float):
            return "number"
        if isinstance(x, str):
            return "string"
        if isinstance(x, list):
            return "array"
        if isinstance(x, dict):
            return "object"
        if x is None:
            return "null"
        assert False, f"Unknown type for value: {x}"
    return "-".join(single_type(arg) for arg in args)

def is_truthy(x):
    if x in [None, False, 0, 0.0, ""]:
        return False
    if isinstance(x, (list, dict)) and len(x) == 0:
        return False
    return True

def ast_to_string(ast):
    s = ""
    if ast["tag"] == "number":
        return str(ast["value"])
    if ast["tag"] == "string":
        return str('"' + ast["value"] + '"')
    if ast["tag"] == "null":
        return "null"
    if ast["tag"] == "list":
        items = []
        for item in ast["items"]:
            result = ast_to_string(item)
            items.append(result)
        return "[" + ",".join(items) + "]"
    if ast["tag"] == "object":
        items = []
        for item in ast["items"]:
            key = ast_to_string(item["key"])
            value = ast_to_string(item["value"])
            items.append(f"{key}:{value}")
        return "{" + ",".join(items) + "}"
    if ast["tag"] == "identifier":
        return str(ast["value"])
    if ast["tag"] in ["+","-","/","*","&&","||","and","or","<",">","<=",">=","==","!="]:
        return  "(" + ast_to_string(ast["left"]) + ast["tag"] + ast_to_string(ast["right"]) + ")"
    if ast["tag"] in ["negate"]:
        return  "(-" + ast_to_string(ast["value"]) + ")"
    if ast["tag"] in ["not","!"]:
        return  "(" + ast["tag"] + " " + ast_to_string(ast["value"]) + ")"
    if ast["tag"] == "print":
        if ast["value"]:
            return "print (" + ast_to_string(ast["value"]) + ")"
        else:
            return "print ()" 

    if ast["tag"] == "assert":
        s = "assert (" + ast_to_string(ast["condition"]) + ")"
        if ast["explanation"]:
            s = s + "," + ast_to_string(ast["explanation"]) + ")"

    if ast["tag"] == "if":
        s = "if (" + ast_to_string(ast["condition"]) + ") {" + ast_to_string(ast["then"]) + "}"
        if ast["else"]:
            s = s + " else {" + ast_to_string(ast["else"]) + "}"

    if ast["tag"] == "while":
        s = "while (" + ast_to_string(ast["condition"]) + ") {" + ast_to_string(ast["do"]) + "}"

    if ast["tag"] == "statement_list":
        items = []
        for item in ast["statements"]:
            result = ast_to_string(item)
            items.append(result)
        return "{" + ";".join(items) + "}"

    if ast["tag"] == "program":
        items = []
        for item in ast["statements"]:
            result = ast_to_string(item)
            items.append(result)
        return "{" + ";".join(items) + "}"

    if ast["tag"] == "function":
        return str(ast)

    if ast["tag"] == "call":
        items = []
        for item in ast["arguments"]:
            result = ast_to_string(item)
            items.append(result)
        return "(" + ",".join(items) + ")"

    if ast["tag"] == "complex":
        s = f"{ast_to_string(ast["base"])}[{ast_to_string(ast["index"])}]"
        return s

    if ast["tag"] == "assign":
        s = f"{ast_to_string(ast["target"])} = {ast_to_string(ast["value"])}]"
        return s

    if ast["tag"] == "return":
        if ast["value"]:
            return "return " + ast_to_string(ast["value"])
        else:
            return "return" 

    assert False, f"Unknown tag [{ast['tag']}] in AST"

__builtin_functions = [
    "head","tail","length","keys"
]

def evaluate_builtin_function(function_name, args):
    if function_name == "head":
        assert len(args) == 1 and isinstance(args[0], list), "head() requires a single list argument"
        return (args[0][0] if args[0] else None), None

    if function_name == "tail":
        assert len(args) == 1 and isinstance(args[0], list), "tail() requires a single list argument"
        return args[0][1:], None

    if function_name == "length":
        assert len(args) == 1 and isinstance(args[0], (list, dict, str)), "length() requires list, object, or string"
        return len(args[0]), None

    if function_name == "keys":
        assert len(args) == 1 and isinstance(args[0], dict), "keys() requires an object argument"
        return list(args[0].keys()), None

    assert False, f"Unknown builtin function '{function_name}'"

def evaluate(ast, environment):
    if ast["tag"] == "number":
        assert type(ast["value"]) in [
            float,
            int,
        ], f"unexpected type {type(ast["value"])}"
        return ast["value"], None
    if ast["tag"] == "boolean":
        assert ast["value"] in [
            True,
            False,
        ], f"unexpected type {type(ast["value"])}"
        return ast["value"], None
    if ast["tag"] == "string":
        assert type(ast["value"]) == str, f"unexpected type {type(ast["value"])}"
        return ast["value"], None
    if ast["tag"] == "null":
        return None, None
    if ast["tag"] == "list":
        items = []
        for item in ast["items"]:
            result, _ = evaluate(item, environment)
            items.append(result)
        return items, None        
    if ast["tag"] == "object":
        object = {}
        for item in ast["items"]:
            key, _ = evaluate(item["key"], environment)
            assert type(key) is str, "Object key must be a string"
            value, _ = evaluate(item["value"], environment)
            object[key] = value
        return object, None        

    if ast["tag"] == "identifier":
        identifier = ast["value"]
        if identifier in environment:
            return environment[identifier], None
        if "$parent" in environment:
            return evaluate(ast, environment["$parent"])
        if identifier in __builtin_functions:
            return {"tag": "builtin", "name": identifier}, None
        raise Exception(f"Unknown identifier: '{identifier}'")
    if ast["tag"] == "+":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        types = type_of(left_value, right_value)
        if types == "number-number":
            return left_value + right_value, None
        if types == "string-string":
            return left_value + right_value, None
        if types == "object-object":
            return {**left_value, **right_value}, None
        if types == "array-array":
            return left_value + right_value, None
        raise Exception(f"Illegal types for {ast['tag']}: {types}")
    if ast["tag"] == "-":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        types = type_of(left_value, right_value)
        if types == "number-number":
            return left_value - right_value, None
        raise Exception(f"Illegal types for {ast["tag"]}:{types}")

    if ast["tag"] == "*":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        types = type_of(left_value, right_value)
        if types == "number-number":
            return left_value * right_value, None
        if types == "string-number":
            return left_value * int(right_value), None
        if types == "number-string":
            return right_value * int(left_value), None
        raise Exception(f"Illegal types for {ast['tag']}:{types}")

    if ast["tag"] == "/":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        types = type_of(left_value, right_value)
        if types == "number-number":
            assert right_value != 0, "Division by zero"
            return left_value / right_value, None
        raise Exception(f"Illegal types for {ast['tag']}:{types}")
    
    if ast["tag"] == "negate":
        value, _ = evaluate(ast["value"], environment)
        types = type_of(value)
        if types == "number":
            return -value, None
        raise Exception(f"Illegal type for {ast['tag']}:{types}")

    if ast["tag"] in ["&&", "and"]:
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return is_truthy(left_value) and is_truthy(right_value), None

    if ast["tag"] in ["||", "or"]:
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return is_truthy(left_value) or is_truthy(right_value), None

    if ast["tag"] in ["!", "not"]:
        value, _ = evaluate(ast["value"], environment)
        return not is_truthy(value), None

    if ast["tag"] in ["<", ">", "<=", ">="]:
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        types = type_of(left_value, right_value)
        if types not in ["number-number", "string-string"]:
            raise Exception(f"Illegal types for {ast['tag']}: {types}")
        if ast["tag"] == "<":
            return left_value < right_value, None
        if ast["tag"] == ">":
            return left_value > right_value, None
        if ast["tag"] == "<=":
            return left_value <= right_value, None
        if ast["tag"] == ">=":
            return left_value >= right_value, None

    if ast["tag"] == "==":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value == right_value, None
    
    if ast["tag"] == "!=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value != right_value, None

    if ast["tag"] == "print":
        if ast["value"]:
            value, _ = evaluate(ast["value"], environment)
            if type(value) is bool:
                if value == True:
                    value = "true"
                if value == False:
                    value = "false"
            print(str(value))
            return str(value) + "\n", None
        else:
            print()
        return "\n", None

    if ast["tag"] == "assert":
        if ast["condition"]:
            value, _ = evaluate(ast["condition"], environment)
            if not(value):
                raise(Exception("Assertion failed:",ast_to_string(ast["condition"])))
        return "\n", None

    if ast["tag"] == "if":
        condition, _ = evaluate(ast["condition"], environment)
        if condition:
            value, exit_status = evaluate(ast["then"], environment)
            if exit_status:
                return value, exit_status
        else:
            if "else" in ast:
                value, exit_status = evaluate(ast["else"], environment)
                if exit_status:
                    return value, exit_status
        return None, False

    if ast["tag"] == "while":
        condition_value, exit_status = evaluate(ast["condition"], environment)
        if exit_status:
            return condition_value, exit_status
        while condition_value:
            value, exit_status = evaluate(ast["do"], environment)
            if exit_status:
                return value, exit_status
            condition_value, exit_status = evaluate(ast["condition"], environment)
            if exit_status:
                return condition_value, exit_status
        return None, False

    if ast["tag"] == "statement_list":
        for statement in ast["statements"]:
            value, exit_status = evaluate(statement, environment)
            if exit_status:
                return value, exit_status
        return value, exit_status

    if ast["tag"] == "program":
        for statement in ast["statements"]:
            value, exit_status = evaluate(statement, environment)
            if exit_status:
                return value, exit_status
        return value, exit_status

    if ast["tag"] == "function":
        return ast, False

    if ast["tag"] == "call":
        function, _ = evaluate(ast["function"], environment)
        argument_values = [evaluate(arg, environment)[0] for arg in ast["arguments"]]

        if function.get("tag") == "builtin":
            return evaluate_builtin_function(function["name"], argument_values)
        
        # regular function call:
        local_environment = {
            name["value"]: val
            for name, val in zip(function["parameters"], argument_values)
        }
        local_environment["$parent"] = environment
        value, exit_status = evaluate(function["body"], local_environment)
        if exit_status:
            return value, False
        else:
            return None, False


    if ast["tag"] == "complex":
        base, _ = evaluate(ast["base"], environment)
        index, _ = evaluate(ast["index"], environment)
        if index == None:
            return base, False
        if type(index) in [int, float]:
            assert int(index) == index
            assert type(base) == list
            assert len(base) > index
            return base[index], False
        if type(index) == str:
            assert type(base) == dict
            return base[index], False
        assert False, f"Unknown index type [{index}]"

    if ast["tag"] == "assign":
        assert "target" in ast
        target = ast["target"]
        if target["tag"] == "identifier":
            target_base = environment
            target_index = target["value"] 
        elif target["tag"] == "complex":
            base, _ = evaluate(target["base"], environment)
            index_ast = target["index"]
            
            if index_ast["tag"] == "string":
                # direct property (like x.bar)
                index = index_ast["value"]
            else:
                # evaluated property (like x["bar"])
                index, _ = evaluate(index_ast, environment)
            
            assert type(index) in [int, float, str], f"Unknown index type [{index}]"
        
            if isinstance(base, list):
                assert isinstance(index, int), "List index must be integer"
                assert 0 <= index < len(base), "List index out of range"
                target_base = base
                target_index = index
            elif isinstance(base, dict):
                target_base = base
                target_index = index
            else:
                assert False, f"Cannot assign to base of type {type(base)}"
        value, _ = evaluate(ast["value"], environment)
        target_base[target_index] = value
        return value, None

    if ast["tag"] == "return":
        if "value" in ast:
            value, exit_status = evaluate(ast["value"], environment)
            return value, "return"
        return None, "return"

    assert False, f"Unknown tag [{ast['tag']}] in AST"


def equals(code, environment, expected_result, expected_environment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)

    assert (
        result == expected_result
    ), f"""ERROR: When executing
    {[code]} 
    -- expected result -- 
    {[expected_result]}
    -- got --
    {[result]}."""

    if expected_environment != None:
        assert (
            environment == expected_environment
        ), f"""ERROR: When executing
        {[code]} 
        -- expected environment -- 
        {[expected_environment]}
        -- got --
        {[environment]}."""


def test_evaluate_single_value():
    print("test evaluate single value")
    equals("4", {}, 4, {})
    equals("3", {}, 3, {})
    equals("4.2", {}, 4.2, {})
    equals("X", {"X": 1}, 1)
    equals("Y", {"X": 1, "Y": 2}, 2)
    equals('"x"', {"x": "cat", "y": 2}, "x")
    equals('x', {"x": "cat", "y": 2}, "cat")
    equals("null", {}, None)


def test_evaluate_addition():
    print("test evaluate addition")
    equals("1+1", {}, 2, {})
    equals("1+2+3", {}, 6, {})
    equals("1.2+2.3+3.4", {}, 6.9, {})
    equals("X+Y", {"X": 1, "Y": 2}, 3)
    equals("\"X\"+\"Y\"", {}, "XY")


def test_evaluate_subtraction():
    print("test evaluate subtraction")
    equals("1-1", {}, 0, {})
    equals("3-2-1", {}, 0, {})


def test_evaluate_multiplication():
    print("test evaluate multiplication")
    equals("1*1", {}, 1, {})
    equals("3*2*2", {}, 12, {})
    equals("3+2*2", {}, 7, {})
    equals("(3+2)*2", {}, 10, {})


def test_evaluate_division():
    print("test evaluate division")
    equals("4/2", {}, 2, {})
    equals("8/4/2", {}, 1, {})


def test_evaluate_negation():
    print("test evaluate negation")
    equals("-2", {}, -2, {})
    equals("--3", {}, 3, {})


def test_evaluate_print_statement():
    print("test evaluate_print_statement")
    equals("print", {}, "\n", {})
    equals("print 1", {}, "1\n", {})
    equals("print 1+1", {}, "2\n", {})
    equals("print 1+1+1", {}, "3\n", {})
    equals("print true", {}, "true\n", {})
    equals("print false", {}, "false\n", {})


def test_evaluate_if_statement():
    print("testing evaluate_if_statement")
    equals("if(1) {3}", {}, None, {})
    equals("if(0) {3}", {}, None, {})
    equals("if(1) {x=1}", {"x": 0}, None, {"x": 1})
    equals("if(0) {x=1}", {"x": 0}, None, {"x": 0})
    equals("if(1) {x=1} else {x=2}", {"x": 0}, None, {"x": 1})
    equals("if(0) {x=1} else {x=2}", {"x": 0}, None, {"x": 2})


def test_evaluate_while_statement():
    print("testing evaluate_while_statement")
    equals("while(0) {x=1}", {}, None, {})
    equals("x=1; while(x<5) {x=x+1}; y=3", {}, 3, {"x": 5, "y": 3})


def test_evaluate_assignment_statement():
    print("test evaluate_assignment_statement")
    equals("X=1", {}, 1, {"X": 1})
    equals("x=x+1", {"x": 1}, 2, {"x": 2})
    equals("y=x+1", {"y": 1, "$parent": {"x": 3}}, 4, {"y": 4, "$parent": {"x": 3}})
    equals(
        "x=x+1",
        {"y": 1, "$parent": {"x": 3}},
        4,
        {"y": 1, "x": 4, "$parent": {"x": 3}},
    )

def test_evaluate_list_literal():
    print("test evaluate_list_literal")
    environment = {}
    code = '[1,2,3]'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == [1,2,3]
    code = '[]'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == []

def test_evaluate_object_literal():
    print("test evaluate_object_literal")
    environment = {}
    code = '{"a":1,"b":2}'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == {"a":1,"b":2}
    code = '{}'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == {}

def test_evaluate_function_literal():
    print("test evaluate_function_literal")
    code = "f=function(x) {1}"
    ast = parse(tokenize(code))
    equals(code, {}, {'tag': 'function', 'parameters': [{'tag': 'identifier', 'value': 'x', 'position': 11}], 'body': {'tag': 'statement_list', 'statements': [{'tag': 'number', 'value': 1}]}}, {'f': {'tag': 'function', 'parameters': [{'tag': 'identifier', 'value': 'x', 'position': 11}], 'body': {'tag': 'statement_list', 'statements': [{'tag': 'number', 'value': 1}]}}}
    )
    code = "function f(x) {1}"
    ast = parse(tokenize(code))
    equals(code, {}, {'tag': 'function', 'parameters': [{'tag': 'identifier', 'value': 'x', 'position': 11}], 'body': {'tag': 'statement_list', 'statements': [{'tag': 'number', 'value': 1}]}}, {'f': {'tag': 'function', 'parameters': [{'tag': 'identifier', 'value': 'x', 'position': 11}], 'body': {'tag': 'statement_list', 'statements': [{'tag': 'number', 'value': 1}]}}}
    )

def test_evaluate_function_call():
    print("test evaluate_function_call")
    environment = {}
    code = "function f() {return(1234)}"
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert environment == {'f': {'tag': 'function', 'parameters': [], 'body': {'tag': 'statement_list', 'statements': [{'tag': 'return', 'value': {'tag': 'number', 'value': 1234}}]}}}
    ast = parse(tokenize("f()"))
    assert ast == {
        "statements": [
            {
                "arguments": [],
                "function": {"tag": "identifier", "value": "f"},
                "tag": "call",
            }
        ],
        "tag": "program",
    }
    result, _ = evaluate(ast, environment)
    assert result == 1234
    environment = {}
    code = """
        x = 3; 
        function g(q)
            {return 2};
        g(4)
        """
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == 2
    code = """
        x = 3; 
        function g(q)
            {return [1,2,3,q]};
        g(4)
        """
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == [1,2,3,4]

def test_evaluate_return_statement():
    print("test evaluate_return_statement")
    environment = {}
    code = """
        function f() { return };
        f()
    """
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert result == None
    code = """
        function f() { return 2+2 };
        f()
    """
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert result == 4
    code = """
        function f(x) { 
            if (x > 1) {
                return 123
            };
            return 2+2 
        };
        f(7) + f(0)
    """
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert result == 127


def test_evaluate_complex_expression():
    print("test evaluate_complex_expression")
    environment = {"x":[2,4,6,8]}
    code = "x[3]"
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == 8

    environment = {"x": {"a": 3, "b": 4}}
    code = 'x["b"]'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == 4

    environment = {"x": {"a": [1,2,3], "b": 4}}
    code = 'x["a"]'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == [1,2,3]

    code = 'x["a"][2]'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == 3

    code = 'x.a[2]'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == 3
    code = "x.b = 7;"
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    code = "x.b;"
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == 7


    environment = {"x": [[1,2],[3,4]]}
    code = 'x[0][1]'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == 2

    environment = {"x": {"a":{"x":4,"y":6},"b":{"x":5,"y":7}}}
    code = 'x["b"]["y"]'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert result == 7

def test_evaluate_complex_assignment():
    print("test evaluate_complex_assignment")
    environment = {"x":[1,2,3]}
    code = 'x[1]=4'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert environment["x"][1] == 4

    environment = {"x":{"a":1,"b":2}}
    code = 'x["b"]=4'
    ast = parse(tokenize(code))
    result, _ = evaluate(ast, environment)
    assert environment["x"]["b"] == 4

def test_evaluate_builtins():
    print("test evaluate builtins")
    
    # head of list
    equals("head([1,2,3])", {}, 1)
    equals("head([])", {}, None)

    # tail of list
    equals("tail([1,2,3])", {}, [2, 3])
    equals("tail([])", {}, [])

    # length of list, string, object
    equals("length([1,2,3])", {}, 3)
    equals('length("hello")', {}, 5)
    equals("length({})", {}, 0)
    equals('length({"a":1,"b":2})', {}, 2)

    # keys of object
    equals('keys({"a":1,"b":2})', {}, ["a", "b"])
    equals('keys({})', {}, [])

def test_evaluator_with_new_tags():
    print("test evaluator with new tags...")

    # test not / !
    equals("!0", {}, True)
    equals("not 0", {}, True)
    equals("!1", {}, False)
    equals("not 1", {}, False)

    # test and / &&
    equals("1 and 1", {}, True)
    equals("1 && 1", {}, True)
    equals("0 and 1", {}, False)
    equals("0 && 1", {}, False)

    # test or / ||
    equals("1 or 0", {}, True)
    equals("1 || 0", {}, True)
    equals("0 or 0", {}, False)
    equals("0 || 0", {}, False)

    # test assignment expressions
    env = {}
    equals("x=5", env, 5, {"x":5})
    equals("y=x+2", env, 7, {"x":5, "y":7})

    # test nested assignment expressions
    env = {}
    equals("a=b=4", env, 4, {"a":4, "b":4})

    # test block with or without extra semicolons or bracket statements
    equals("if(1){x=1; y=2}", {}, None, {"x":1,"y":2})
    equals("if(1){x=1; y=2;}", {}, None, {"x":1,"y":2})
    equals("if(1){x=1; if(false) {z=4} y=2;}", {}, None, {"x":1,"y":2})

if __name__ == "__main__":
    # statements and programs are tested implicitly
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_negation()
    test_evaluate_print_statement()
    test_evaluate_if_statement()
    test_evaluate_while_statement()
    test_evaluate_assignment_statement()
    test_evaluate_function_literal()
    test_evaluate_function_call()
    test_evaluate_complex_expression()
    test_evaluate_complex_assignment()
    test_evaluate_return_statement()
    test_evaluate_list_literal()
    test_evaluate_object_literal()
    test_evaluate_builtins()
    test_evaluator_with_new_tags()
    print("done.")