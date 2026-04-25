examples = {
    "Example 1: Simple Assignment": "x = 5 end",

    "Example 2: Math Operations": """x = 10 + 5 end
y = 20 - 3 end
z = 4 * 7 end
w = 100 / 25 end""",

    "Example 3: Complex Expression": """result = 5 + 3 * 2 end
value = 10 - 4 / 2 end
total = result + value end""",

    "Example 4: If Statement": """if ( x = 0 ) end
    print ( zero ) end
end""",

    "Example 5: If Multiple Conditions": """if ( x = 0 , y >= 10 , z ++ ) end
    print ( yes ) end
end""",

    "Example 6: If Else": """if ( x = 0 ) end
    print ( zero ) end
else end
    print ( not_zero ) end
end""",

    "Example 7: If Elif": """if ( x = 0 ) end
    print ( zero ) end
elif ( x = 1 ) end
    print ( one ) end
else end
    print ( other ) end
end""",

    "Example 8: For Loop": """for ( i = 0 , i < 10 , i ++ ) end
    print ( i ) end
end""",

    "Example 9: For Body": """x = 0 end
for ( i = 1 , i <= 5 , i ++ ) end
    x = x + i end
end
print ( x ) end""",

    "Example 10: Input Output": """input ( x ) end
y = x + 5 end
print ( y ) end""",

    "Example 11: Nested If": """for ( i = 0 , i < 5 , i ++ ) end
    if ( i = 2 ) end
        print ( two ) end
    end
end""",

    "Example 12: All Features": """a = 10 end
b = 20 end
sum = a + b end
if ( sum >= 30 ) end
    for ( i = 0 , i < 3 , i ++ ) end
        print ( sum ) end
    end
else end
    print ( small ) end
end""",

    "ERROR: Missing end": "x = 5",

    "ERROR: Unknown char": "x = 5 > 3 end",

    "ERROR: Invalid condition": "if ( x > 5 ) end",

    "ERROR: Missing paren": "if ( x = 5 end",

    "ERROR: Double operators": "x = 5 ++ 3 end",

    "ERROR: Empty print": "print ( ) end",

    "ERROR: Missing comma": "if ( x = 5 y = 10 ) end",

    "ERROR: Invalid increment": "x ++ = 5 end",

    "ERROR: For no update": """for ( i = 0 , i < 5 ) end
    print ( i ) end
end""",
}


def get_example_names():
    return list(examples.keys())
