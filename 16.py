import re

# AAencode 解码器 (Python 版)
def aa_decode(data: str) -> str:
    """
    解码 AAencode 混淆的 JavaScript
    :param data: 混淆后的字符串 (完整)
    :return: 解码出的原始 JavaScript
    """
    # 提取出 eval(...) 内部的部分
    match = re.search(r"\(ﾟДﾟ\)\[\'_\']\(\'_\'\)\((.*)\)", data, re.S)
    if not match:
        raise ValueError("未找到 AAencode 主体，请确认代码完整")

    # 构造一段 JS 在 node.js 里运行来解码
    js_code = f"""
    function aa_decode(text) {{
        try {{
            return eval(text);
        }} catch(e) {{
            return e.toString();
        }}
    }}
    console.log(aa_decode({match.group(1)}));
    """

    return js_code


if __name__ == "__main__":
    with open("js/16.js", "r", encoding="utf-8") as f:
        encoded_js = f.read()

    decoded_stub = aa_decode(encoded_js)
    with open("decode_runner.js", "w", encoding="utf-8") as f:
        f.write(decoded_stub)

    print("已生成 decode_runner.js，用 node 执行：")
    print("    node decode_runner.js > decoded.js")
    print("结果会保存到 decoded.js")
