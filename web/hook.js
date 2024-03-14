// 定义 hook 脚本，这样，代码读写cookie的时候，就会断点停下来，方便分析了
Object.defineProperty(document, 'cookie', {
        get: function() {
            debugger;
            return "";
        },
        set: function(value) {
            debugger;
            return value;
        },
});