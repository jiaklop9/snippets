var AAA = Function.prototype.constructor
Function.prototype.constructor = function (x) {
    if (x != "debugger") {
        return AAA(x)
    }
    return function () {
    };
}
