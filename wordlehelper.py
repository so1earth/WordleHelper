import re
import os
DISPLAY_WORD_CNT = 200


def reg_generate(green_reg, yellow_reg, gray_reg, used_char):
    # 初期化
    green_string_for_reg = ""

    # Green処理
    green_string = input("Green: ")
    if len(green_string) == 5:
        for char in green_string:
            if char == "?":
                green_string_for_reg += "."
            else:
                green_string_for_reg += char
                used_char += char
        green_reg += "(?=" + green_string_for_reg + ")"

    # Yellow処理
    yellow_string = input("Yellow: ")
    if len(yellow_string) == 5:
        for index, char in enumerate(yellow_string, start=1):
            if char != "?":
                used_char += char
                # 含まれている文字パターン
                yellow_reg += "(?=.*" + char + ")"
                # 除外位置パターン
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


def filter_via_regex(init_set, green_reg, yellow_reg, gray_reg):
    reg = "(?i)" + "^" + green_reg + \
                yellow_reg + gray_reg + "[a-zA-Z]{5}$"
    print("Regular Expression Pattern:", reg)
    word_set = set()
    for word in init_set:
        if re.match(reg, word):
            word_set.add(word)
    print()
    return word_set

def slot_status(green_reg, yellow_reg, gray_reg):
    # Green Status表示
    green_reg_list = green_reg.split(')')
    green_alpha_dic = {}
    for pattern in green_reg_list:
        if pattern == '':
            continue
        else:
            for i, letter in enumerate(pattern):
                if letter.isalpha():
                    green_alpha_dic[letter] = i - 2
    print("   ", end="")
    for num in range(1, 6):
        enter_flag = False
        for letter, loc in green_alpha_dic.items():
            if num == loc:
                print('\033[32m\033[07m\033[1m' + letter + '\033[0m', end=" ")
                enter_flag = True
        if enter_flag == False:
            print("?", end=" ")
    print()
    # Yello Status表示
    yellow_reg_list = yellow_reg.split('!')
    yello_alpha_dic = {}
    for pattern in yellow_reg_list:
        if pattern == '':
            continue
        elif pattern.startswith('.') or pattern[0].isalpha:
            for i, letter in enumerate(pattern[0:6]):
                if letter.isalpha():
                    yello_alpha_dic[letter] = i + 1
    for letter, loc in yello_alpha_dic.items():
        print('\033[33m\033[07m\033[1m' + letter + '\033[0m' + ": ", end="")
        for num in range(1, 6):
            if (num == loc) or (num in green_alpha_dic.values()):
                print("✕ ", end="")
            else:
                print("△ ", end="")
        print()
    # Gray Status 表示
    print()
    gray_reg_list = gray_reg.split('(')
    gray_alpha_list = []
    for pattern in gray_reg_list:
        if pattern == '':
            continue
        else:
            for letter in pattern:
                if letter.isalpha():
                    gray_alpha_list.append(letter)
    for i, letter in enumerate(gray_alpha_list):
        print("✕" + '\033[37m\033[07m\033[1m' + letter + '\033[0m', end="")
        if i == len(gray_alpha_list) - 1:
            print()
        else:
            print(", ", end="")
    print()


def candidates_show(word_set):
    # ステータス表示
    print("Match Number: ", len(word_set), end="")
    print(f" (Showing {DISPLAY_WORD_CNT})") if len(
        word_set) > DISPLAY_WORD_CNT else print("")

    # 大文字と小文字を分ける。
    upper_words = []
    lower_words = []
    for word in word_set:
        if word.islower():
            lower_words.append(word)
        else:
            upper_words.append(word)

    # 小文字のリストをRating順にソート
    lower_words_dic = dict.fromkeys(lower_words, 0)
    vow_sounds = "aiueo"
    for word in lower_words_dic:
        for letter in word:
            if letter in vow_sounds:
                lower_words_dic[word] += 1
    for word in lower_words_dic:
        for letter in word:
            if word.count(letter) > 1:
                lower_words_dic[word] -= 1
    lower_words_tup = sorted(lower_words_dic.items(),
                             key=lambda x: x[1], reverse=True)
    lower_words = [l for l, r in lower_words_tup]

    word_list = lower_words + upper_words

    # 単語のリストを出力　
    count = 0
    for word in word_list:
        print(word, end="  ")
        count += 1
        if count % 10 == 0:
            print()
            if count >= DISPLAY_WORD_CNT:
                break

def main():
    # 初期化
    used_char = ""
    green_reg = ""
    yellow_reg = ""
    gray_reg = ""

    # Word辞書ファイルを読み込んでsetに格納
    init_set = set()
    five_word_file = os.path.join(os.path.dirname(__file__), '5wordsList')
    with open(five_word_file, 'r', encoding='utf-8') as f:
        for row in f:
            init_set.add(row.strip())

    flag = True
    while flag == True:
        # 正規表現パターン作成
        green_reg, yellow_reg, gray_reg, used_char = reg_generate(
            green_reg, yellow_reg, gray_reg, used_char)

        # フィルタリング処理
        word_set = filter_via_regex(init_set, green_reg, yellow_reg, gray_reg)

        # ステータス出力
        slot_status(green_reg, yellow_reg, gray_reg)

        # 候補の表示
        candidates_show(word_set)

        # プロンプト
        print("\n")
        while flag == True:
            ctrl_string = input("Another try to narrow down? (y or n) : ")
            if ctrl_string == "n":
                flag = False
                break
            elif ctrl_string == 'y':
                break
            else:
                pass



if __name__ == '__main__':
    main()
