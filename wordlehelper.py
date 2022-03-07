import re
def main():
    # Word辞書ファイルを読み込んでsetに格納
    init_set = set()
    with open('5wordsList', 'r', encoding='utf-8') as f:
        for row in f:
            init_set.add(row.strip()) 
    # ユーザインタフェース起動。
    # Green処理
    green_string = input("Green: ")
    green_reg = "(?=" + green_string.replace("?", ".") + ")"

    # フィルタリング処理
    reg = "^" + green_reg + "[a-z]{5}$"
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