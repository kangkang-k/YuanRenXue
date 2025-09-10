function getClearanceCookie() {
    // 这里正常情况 cookie 值应该是计算出来的
    // 我用 "xxxxxx" 作为占位，你可以改成你真实算出来的值
    const cookie = "__jsl_clearance=xxxxxx; Expires=Mon, 06 May 2025 20:10:00 GMT; Path=/;";
    return cookie;
}

// 调用示例
console.log(getClearanceCookie());
