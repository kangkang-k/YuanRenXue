const CryptoJS = require("crypto-js");

const C = "aiding1234567891"

function X(k, n = C) {
    const O = CryptoJS['\x41\x45\x53']['\x65\x6e\x63\x72' + '\x79\x70\x74'](k, CryptoJS['\x65\x6e\x63']['\x55\x74\x66\x38']['\x70\x61\x72\x73' + '\x65'](n), {
        '\x6d\x6f\x64\x65': CryptoJS['\x6d\x6f\x64\x65']['\x45\x43\x42'],
        '\x70\x61\x64\x64\x69\x6e\x67': CryptoJS['\x70\x61\x64']['\x50\x6b\x63\x73' + '\x37']
    });
    return O['\x74\x6f\x53\x74' + '\x72\x69\x6e\x67']();
}


console.log(X(7['toString']() + ('"|python-spider.com|yuanrenxue.com|大威天龙，大罗法咒"')))


function get_msg(page) {
    return X(page['toString']() + ('"|python-spider.com|yuanrenxue.com|大威天龙，大罗法咒"'))
}

console.log(get_msg(7));