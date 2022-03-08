import re

def reg_generate(green_reg, yellow_reg, gray_reg, used_char):
    # 初期化
    green_string_for_reg = ""

    # Green処理
    green_string = input("Green: ")
    for char in green_string:
        if char == "?":
            green_string_for_reg += "."
        else:
            green_string_for_reg += char
            used_char += char
    green_reg += "(?=" + green_string_for_reg + ")"
    # Yellow処理
    yellow_string = input("Yellow: ")

    for index, char in enumerate(yellow_string, start=1):
        if char != "?":
            used_char += char
            #含まれている文字パターン
            yellow_reg += "(?=.*" + char + ")"
            #除外位置パターン
            exclude_loc = ""
            for i in range(1, 6):
                if i == index:
                    exclude_loc += char
                else:
                    exclude_loc += "."
            yellow_reg += "(?!" + exclude_loc + ")"
    # Gray処理
    gray_string = input("Gray: ")
    exclude_chars = gray_string.split(",")
    for char in exclude_chars:
        if char not in used_char:
            gray_reg += "(?!.*" + char + ")"
    # regular expression return
    return green_reg, yellow_reg, gray_reg, used_char


def main():
    # 初期化
    used_char = ""
    green_reg = ""
    yellow_reg = ""
    gray_reg = ""

    # Word辞書ファイルを読み込んでsetに格納
    init_set = set()
    with open('5wordsList', 'r', encoding='utf-8') as f:
        for row in f:
            init_set.add(row.strip()) 

    green_reg, yellow_reg, gray_reg, used_char = reg_generate(green_reg, yellow_reg, gray_reg, used_char)

    # フィルタリング処理
    reg = "^" + green_reg + yellow_reg + gray_reg + "[a-z]{5}$"
    print("Regular Expression Pattern:", reg)
    word_set = set()
    for word in init_set:
        if re.match(reg, word):
            word_set.add(word)

    # ステータス出力
    print("Words Number: ", len(word_set))
    # 単語のリストを出力
    count = 0
    for word in word_set:
        print(word)
        count += 1
        if count == 10:
            break
if __name__ == '__main__':
    main()