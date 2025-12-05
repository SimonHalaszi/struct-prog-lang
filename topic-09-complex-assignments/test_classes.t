class MyClass {
    members a, b, c;
    
    constructor(x, y, z) {
        a = x;
        b = y;
        c = z;
    }
 
    function getA() {
        return a
    }
    
    function getB() {
        return b
    }

    function getC() {
        return c
    }

    function accumulate() {
        localVar = 0;
        localVar = localVar + a;
        localVar = localVar + b;
        localVar = localVar + c;
        return localVar;
    }
}

instance = MyClass(1, 2, 3);

print instance.accumulate();

// Wont work:
// print a;
// accumulate();