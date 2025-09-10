const CryptoJS = require("crypto-js");

function get_uc(num) {
    const k = 'wdf2ff*TG@*(F4)*YH)g430HWR(*)' + 'wse';
    const t = Math.floor(Date.now() / 1000);
    const m = CryptoJS.enc.Utf8.parse(k);

    function encrypt(word) {
        const srcs = CryptoJS.enc.Utf8.parse(word);
        const encrypted = CryptoJS.AES.encrypt(srcs, m, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        return encrypted.toString();
    }

    const s = encrypt(t + '|' + num);
    return s;
}
