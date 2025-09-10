const CryptoJS = require('crypto-js')

function I(X, l) {
    C = X
    q = CryptoJS['enc']['Utf8']['parse'](C)
    v = CryptoJS['DES']['decrypt'](l, q, {
        'mode': CryptoJS['mode']['ECB'],
        'padding': CryptoJS['pad']['Pkcs7']
    });
    return CryptoJS.enc.Utf8.stringify(v);
}


function get_data(k) {
    return  JSON['parse'](I(k['result']['slice'](0x0, 0x8), k['result']['slice'](0x8)))['data']
}

