from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション用のキー

# 手札の合計を計算（Aを1または11として扱う）
def calculate_hand_value(hand):
    total = sum(card[1] for card in hand)
    num_aces = sum(1 for card in hand if card[0][1:] == '1')
    while num_aces > 0 and total + 10 <= 21:
        total += 10
        num_aces -= 1
    return total

# テンプレートで calculate_hand_value を使えるように登録
@app.context_processor
def utility_processor():
    return dict(calculate_hand_value=calculate_hand_value)

# 新しいゲームを初期化する
def init_game():
    single_deck = [ (f"{suit}{num}", 10 if num > 10 else num)
                    for suit in ['s','h','d','c']
                    for num in range(1,14) ]
    deck = single_deck * 6
    random.shuffle(deck)

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    session['deck'] = deck
    session['player_hands'] = [player_hand]
    session['current_hand'] = 0
    session['dealer'] = dealer_hand
    session['phase'] = 'player'
    session['message'] = ''

@app.route('/start')
def start():
    if 'history' not in session:
        session['history'] = []
    session['phase'] = 'bet'
    return redirect(url_for('index'))

@app.route('/bet', methods=['POST'])
def bet():
    print(request.form)
    if 'amount' in request.form:
        amount = int(request.form['amount'])  # ボタンでのBET
    elif 'half-amount' in request.form:
        amount = int(request.form['half-amount'])    # half-in
    elif 'custom_amount' in request.form:
        try:
            amount = int(request.form['custom_amount'])  # カスタム入力
        except ValueError:
            session['message'] = '正しい金額を入力してください'
            session['phase'] = 'bet'
            return redirect(url_for('index'))
    # elif 'half-amount' in request.form:
    #     amount = int(request.form['half-amount'])    # half-in
    else:
        session['message'] = '金額を選んでください'
        session['phase'] = 'bet'
        return redirect(url_for('index'))

    balance = session.get('balance', 1000)
    if amount <= 0 or amount > balance:
        session['message'] = 'ベットできる残高を超えています'
        session['phase'] = 'bet'
        return redirect(url_for('index'))

    session['bet'] = amount
    session['balance'] = balance - amount
    init_game()
    return redirect(url_for('index'))


# ナチュラルブラックジャック判定用関数
def is_blackjack(hand):
    return len(hand) == 2 and calculate_hand_value(hand) == 21

@app.route('/')
def index():
    print("index()に入った")
    pien_flag = False
    
    # セッション初期値
    if 'balance' not in session:
        session['balance'] = 10000
    if 'history' not in session:
        session['history'] = []

    # #  デバッグ用: http://127.0.0.1:5000?force_natural=1 でナチュラルBJを強制
    # if request.args.get('force_natural') == '1':
    #     init_game()
    #     player = [('h10', 10), ('h1', 11)]
    #     dealer = [('d1', 2), ('c10', 10)]
    #     session['player_hands'] = [player]
    #     session['dealer'] = dealer
    #     session['current_hand'] = 0
    # # 
    # # スプリット後のデバッグ http://127.0.0.1:5000?debug_split=1
    # elif request.args.get('debug_split') == '1':
    #     init_game()
    #     # 10と10でスプリット可能な手札を強制セット
    #     player = [('s10', 10), ('s10', 10)]
    #     dealer = [('d9', 9), ('c5', 5)]

    #     # スプリット後の手札に2枚目を追加（カードは適当）
    #     deck = session['deck']
    #     hand1 = [player[0], ('c1', 1)]
    #     hand2 = [player[1], ('d8', 8)]

    #     session['player_hands'] = [hand1, hand2]
    #     session['dealer'] = dealer
    #     session['current_hand'] = 0
    #     session['bet'] = 100
    #     session['balance'] = int(session.get('balance', 1000)) - 100
    #     session['phase'] = 'player'
    # # 


    # ナチュラルBJ判定を player フェーズ時のみ実行 
    if session.get('phase') == 'player':
        hands = session.get('player_hands', [])
        current = session.get('current_hand', 0)
        player = hands[current] if hands and current < len(hands) else []
        dealer = session.get('dealer', [])
        if len(hands) == 1 and (is_blackjack(player) or is_blackjack(dealer)):
            session['message'] = 'ナチュラルブラックジャック！'
            return redirect(url_for('resolve'))

    phase = session.get('phase')
    dealer = session.get('dealer', [])
    dealer_up = dealer[0] if dealer else None
    dealer_total = calculate_hand_value(dealer) if phase != 'player' else None
    message = session.pop('message', '')

   # ベットフェーズ
    if phase == 'bet':
        history = session.get('history', [])

        # 先にフラグ用変数を定義しておく
        pien_flag = False

        # セッション内にフラグがあるか、残高が0かチェック
        if session.get('balance', 0) <= 0:
            session['pien'] = True
            pien_flag = True
            print("index(): 残高0なのでpienフラグON")
        else:
            # セッションにフラグがあれば pop する
            pien_flag = session.pop('pien', False)

        print('pien_flag:', pien_flag)

        reset_count = session.get('reset_count', 0)

        return render_template('bet.html',
                            balance=session['balance'],
                            message=message,
                            history=history,
                            pien_flag=pien_flag,
                            reset_count=reset_count)

    # 終了フェーズ
    if phase == 'end':
        hands = session.get('player_hands', [])
        history = session.get('history', [])
        pien_flag = session.pop('pien', False) 
        natural_bj = session.pop('natural_bj', False) 
        print('pien_flag:', pien_flag)
        return render_template('index.html',
                               player_hands=hands,
                               dealer=dealer,
                               dealer_up=dealer_up,
                               dealer_total=dealer_total,
                               message=message,
                               phase='end',
                               balance=session['balance'],
                               bet=session.get('bet',0),
                               history=history,
                               pien_flag=pien_flag,
                               natural_bj=natural_bj)

    # 通常プレイフェーズ
    hands = session.get('player_hands', [])
    i = session.get('current_hand', 0)
    if not hands or i >= len(hands):
        return redirect(url_for('start'))

    player = hands[i]
    can_split = (len(player) == 2 and player[0][0][1:] == player[1][0][1:] and len(hands) == 1)
    # if calculate_hand_value(player) == 21:
    #     return next_hand_or_finish()

    history = session.get('history', [])
    natural_bj = session.pop('natural_bj', False) 
    return render_template('index.html',
                           player_hands=hands,
                           player=player,
                           dealer=dealer,
                           dealer_up=dealer_up,
                           player_total=calculate_hand_value(player),
                           dealer_total=dealer_total,
                           message=message,
                           phase=phase,
                           can_split=can_split,
                           hand_index=i+1,
                           hand_count=len(hands),
                           balance=session['balance'],
                           bet=session.get('bet',0),
                           history=history,
                           natural_bj=natural_bj
                           )

@app.route('/hit', methods=['POST'])
def hit():
    deck = session.get('deck', [])
    i = session['current_hand']
    hands = session['player_hands']
    if deck:
        hands[i].append(deck.pop())
    session['player_hands'] = hands
    total = calculate_hand_value(hands[i])
    if total > 21:
        session['message'] = f"Hand {i+1}: Bust!"
        return next_hand_or_finish()
    return redirect(url_for('index'))

@app.route('/stand', methods=['POST'])
def stand():
    return next_hand_or_finish()

def next_hand_or_finish():
    session['current_hand'] += 1
    if session['current_hand'] >= len(session['player_hands']):
        return redirect(url_for('resolve'))
    return redirect(url_for('index'))

@app.route('/split', methods=['POST'])
def split():
    balance = session.get('balance', 0)
    bet = session.get('bet', 0)
    if balance < bet:
        session['message'] = '残高不足でスプリットできません'
        return redirect(url_for('index'))
    session['balance'] = balance - bet

    deck = session.get('deck', [])
    hands = session.get('player_hands', [])
    if deck and len(hands[0]) == 2 and hands[0][0][0][1:] == hands[0][1][0][1:]:
        split1 = [hands[0][0], deck.pop()]
        split2 = [hands[0][1], deck.pop()]
        session['player_hands'] = [split1, split2]
        session['current_hand'] = 0
    return redirect(url_for('index'))


@app.route('/resolve')
def resolve():
    print("resolve() に入った")

    # BJ判定
    natural_bj_indices = [i for i, h in enumerate(session.get('player_hands', [])) if is_blackjack(h)]
    dealer_is_natural_bj = is_blackjack(session.get('dealer', []))

    deck = session.get('deck', [])
    dealer = session.get('dealer', [])
    if not any(is_blackjack(h) for h in session.get('player_hands', [])):
        if any(calculate_hand_value(h) <= 21 for h in session.get('player_hands', [])):
            while calculate_hand_value(dealer) < 17 and deck:
                dealer.append(deck.pop())
    session['dealer'] = dealer


    dealer_total = calculate_hand_value(dealer)
    results = []
    dealer_hand = session.get('dealer', [])
    dealer_is_natural = is_blackjack(dealer_hand)

    for hand in session.get('player_hands', []):
        player_total = calculate_hand_value(hand)
        player_is_natural = is_blackjack(hand)

        # 両者ナチュラルBJなら引き分け
        if player_is_natural and dealer_is_natural:
            results.append('Push')
        # プレイヤーがナチュラルBJなら勝ち
        elif player_is_natural:
            results.append('Win')
        # ディーラーがナチュラルBJなら負け
        elif dealer_is_natural:
            results.append('Lose')
        # 通常の比較
        elif player_total > 21:
            results.append('Bust')
        elif dealer_total > 21 or player_total > dealer_total:
            results.append('Win')
        elif player_total == dealer_total:
            results.append('Push')
        else:
            results.append('Lose')

    # ナチュラルBJで勝ってて、ディーラーはBJじゃない場合のみ
    if any(results[i] == 'Win' for i in natural_bj_indices) and not dealer_is_natural_bj:
        session['natural_bj'] = True
    else:
        session['natural_bj'] = False  # 明示的にFalseもセット

    
    print(f"natural_bj_indices: {natural_bj_indices}")
    print(f"results: {results}")
    print(f"dealer_is_natural_bj: {dealer_is_natural_bj}")
    print(f"natural_bj set to: {session['natural_bj']}")

    # 残り処理
    payout = 0
    for r in results:
        if r == 'Win':
            payout += session.get('bet',0) * 2
        elif r == 'Push':
            payout += session.get('bet',0)
    session['balance'] = session.get('balance',0) + payout

    if session['balance'] <= 0:
        session['pien'] = True

    history = session.get('history', [])
    history.append({
        'round': len(history)+1,
        'bet': session.get('bet',0),
        'result': ' / '.join(results),
        'balance': session['balance']
    })
    session['history'] = history
    session['phase'] = 'end'
    session['current_hand'] = 0
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    # リセット時に、リセット回数を記録
    reset_count = session.get('reset_count', 0) + 1
    session.clear()
    session['balance'] = 10000
    session['pien'] = True
    session['reset_count'] = reset_count    # jsに渡す

    session.pop('pien', None)
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)

# http//127.0.0.1:5000