import random

# ブラックジャックを作る

# Aが存在する場合の手札の合計を計算する
def calculate_hand_value(hand):
    total = sum(card[1] for card in hand)
    num_aces = sum(1 for card in hand if card[0][1:] == '1')  # "s1", "h1"など

    # Aを11としてもバーストしないなら10を加算（1->11）
    while num_aces > 0 and total + 10 <= 21:
        total += 10
        num_aces -= 1
    return total

# 最初の2枚でブラックジャックかどうか判定
def is_blackjack(hand):
    return len(hand) == 2 and calculate_hand_value(hand) == 21

# デッキを1枚ずつのタプルで生成
single_deck = [
    (f"{suit}{num}", 10 if num > 10 else num)
    for suit in ['s', 'h', 'd', 'c']
    for num in range(1, 14)
]
# 6デッキ分展開
trump_deck = single_deck * 6  # 52枚 x 6 = 312枚
random.shuffle(trump_deck)

# カード配布
dealer = [trump_deck.pop(), trump_deck.pop()]
player = [trump_deck.pop(), trump_deck.pop()]

# 表示
print(f"ディーラーの手札: [{dealer[0][0]}][?]")
print(f"あなたの手札: [{player[0][0]}][{player[1][0]}] 合計: {calculate_hand_value(player)}")

# ブラックジャック判定
if is_blackjack(player):
    if is_blackjack(dealer):
        print("お互いブラックジャック！引き分け（プッシュ）！")
    else:
        print("あなたののブラックジャック！勝利！")
    exit()

if is_blackjack(dealer):
    print("ディーラーのブラックジャック！あなたのの負け！")
    exit()

# プレイヤーのターン
player_total = calculate_hand_value(player)
action = ["hit", "stand"]
while True:
    n = int(input("hit: 1  stand: 2 > "))
    while n < 1 or n > 2:
        n = int(input("hit: 1  stand: 2 > "))

    if n == 1:
        player.append(trump_deck.pop())
        print("あなたの: ", end="")
        for card in player:
            print(f"[{card[0]}]", end=" ")
        print()
        
        player_total = calculate_hand_value(player)
        if player_total > 21:
            print(f"あなたの合計: {player_total} → バースト！")
            exit()
        elif player_total == 21:
            break
        else:
            print(f"あなたの合計: {player_total}")
    else:
        print("スタンドしました")
        print(f"あなたの合計: {player_total}")
        break

# ディーラーのターン
dealer_total = calculate_hand_value(dealer)
while True:
    if dealer_total < 17:
        dealer.append(trump_deck.pop())
        print("ディーラー: ", end="")
        for card in dealer:
            print(f"[{card[0]}]", end=" ")
        print()

        dealer_total = calculate_hand_value(dealer)
        if dealer_total > 21:
            print(f"ディーラー合計: {dealer_total} → バースト！")
            print("あなたの勝利！")
            exit()
        elif dealer_total == 21:
            break
        else:
            pass
            # print(f"合計: {dealer_total}")
    else:
        print(f"ディーラー合計: {dealer_total}")
        break

# 勝敗判定
if player_total == dealer_total:
    print("引き分け！")
elif player_total > dealer_total:
    print("あなたの勝ち！")
else:
    print("あなたの負け！")
