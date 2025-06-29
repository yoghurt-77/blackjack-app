// ぴえん要素を生成＋落下させる
function createPien() {
  const el = document.createElement('div');
  const scale = 1 + parseInt(document.body.dataset.resetCount || '0') * 0.5;
  el.style.transform = `scale(${scale})`;
  el.className = 'pien';
  el.textContent = '😢';
  el.style.left = Math.random() * 100 + 'vw';
  const duration = 3 + Math.random() * 3;
  el.style.animationDuration = duration + 's';
  document.body.appendChild(el);
  setTimeout(() => el.remove(), duration * 1000);
}

// 一定間隔で「ぴえん」を降らせ続ける
function startPienRain() {
  createPien();
  return setInterval(createPien, 200);
}

// GAMEOVER＆リセットボタンの表示
function gameOver() {
  const wrapper = document.getElementById('game-over-wrapper');

  const msg = document.createElement('div');
  msg.className = 'game-over';

  msg.innerHTML = `
    <div>GAME OVER</div>
    <button class="reset-button">ぴえん</button>
  `;

  wrapper.appendChild(msg);

  msg.querySelector('.reset-button').onclick = () => {
    fetch('/reset', { method: 'POST' })
      .then(() => location.href = '/');
  };
}


// 花火の演出
function launchFireworksInModal(repeat = 10) {
  const container = document.getElementById('modal-fireworks');
  if (!container) return;

  container.innerHTML = ''; // 初期化

  const colors = ['red', 'yellow', 'blue', 'white', 'lime'];
  const particleCount = 15;
  let count = 0;

  const launch = () => {
    const centerX = Math.random() * container.clientWidth;
    const centerY = Math.random() * container.clientHeight;

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'firework';

      const angle = (Math.PI * 2 * i) / particleCount;
      const radius = 60 + Math.random() * 30;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;

      particle.style.left = `${centerX}px`;
      particle.style.top = `${centerY}px`;
      particle.style.setProperty('--x', `${x}px`);
      particle.style.setProperty('--y', `${y}px`);
      particle.style.backgroundColor = colors[i % colors.length];

      container.appendChild(particle);
    }

    count++;
    if (count < repeat) {
      const nextDelay = 300 + Math.random() * 400; // 300〜700msでランダム発射
      setTimeout(launch, nextDelay);
    }
  };

  launch(); // 最初の一発
}

// 花火の繰り返し
function repeatFireworks() {
  for (let i = 0; i < 10; i++) {
          launchFireworksInModal(50);
          launchFireworksInModal(50);
  }
}


// ハートシャワー
let heartInterval = null;
function startHeartShower(duration = 5000) {
  heartInterval = setInterval(() => {
    for (let i = 0; i < 10; i++) {
      const heart = document.createElement('div');
      heart.className = 'heart';
      heart.textContent = '💗';
      heart.style.left = Math.random() * 100 + 'vw';
      heart.style.animationDuration = (2 + Math.random() * 2) + 's';
      heart.style.fontSize = (1 + Math.random() * 2) + 'rem';
      heart.style.transform = `rotate(${Math.random() * 360}deg)`;
      document.body.appendChild(heart);
      setTimeout(() => heart.remove(), 6000);
    }
  }, 150); // ← ここを heartInterval に代入しておく
}

// 赤７
function launchLuckySeven(callback) {
  const container = document.createElement('div');
  container.className = 'seven-container';

  const left = document.createElement('div');
  left.className = 'seven seven-left';
  left.textContent = '7';

  const center = document.createElement('div');
  center.className = 'seven seven-center';
  center.textContent = '7';

  const right = document.createElement('div');
  right.className = 'seven seven-right';
  right.textContent = '7';

  container.appendChild(left);
  container.appendChild(center);
  container.appendChild(right);

  document.body.appendChild(container);

  // アニメーションが終わったらcallback
  let ended = 0;
  const onEnd = () => {
    ended++;
    if (ended === 3 && typeof callback === 'function') {
      callback();
      console.log('callback()はTrue');
    }
  };
  [left, center, right].forEach(el => {
    el.addEventListener('animationend', () => {
      console.log('animation end', el.className);
      onEnd();
      console.log(`onEnd()到達。end=${ended}`);
    });
  });
}
// 赤7の隠し音
function hideSoundLuckySeven() {
  const luckySound = document.getElementById('lucky-seven-sound');
  let soundPlayed = false;

  const playLucky = () => {
    if (!soundPlayed) {
      luckySound.volume = 0.5;
      luckySound.play().catch(e => console.warn('再生失敗', e));
    }
  };

  window.addEventListener('click', playLucky, { once: true });

  // 花火
  repeatFireworks();
}

// 666
function trigger666() {
  // すでに存在してたら一旦削除
  document.getElementById('rip-wrapper')?.remove();

  const rip = document.createElement('div');
  rip.id = 'rip-wrapper';
  rip.innerHTML = `
    <div class="rip left"></div>
    <div class="rip right"></div>
  `;
  document.body.appendChild(rip);

  const demon = document.createElement('div');
  demon.id = 'demon-summon';
  demon.textContent = '👿';
  document.body.appendChild(demon);
  }



// モーダル表示用の関数
const showModal = (message) => {
  const overlay = document.getElementById('modal-overlay');
  const msgBox = document.getElementById('modal-message');
  const closeBtn = document.getElementById('modal-close');

  msgBox.textContent = message;
  overlay.style.display = 'flex';

  console.log('OKボタンを押した');

  closeBtn.onclick = () => {
    overlay.style.display = 'none';

    // 演出後削除
    // shakeの削除
    console.log('shakeの削除');
    document.body.classList.remove('shake');

    console.log('heartの削除');
    if (heartInterval) {
      clearInterval(heartInterval);
      heartInterval = null;
    }
    // ハート生成の削除
    console.log('document.query...の前')
    document.querySelectorAll('.heart').forEach(el => el.remove());
    console.log('ハートの削除完了');

    // 赤７の削除
    console.log('赤７の削除');
    const sevenContainer = document.querySelector('.seven-container');
    if (sevenContainer) {
      sevenContainer.remove();
    }
  };
};



// DOMロード後の処理は1つにまとめる！
document.addEventListener('DOMContentLoaded', () => {
  const resultEl = document.querySelector('.result');
  const text = resultEl ? resultEl.textContent : '';
  const balance = parseInt(document.body.dataset.balance, 10);
  const isPien = document.body.dataset.pien === "true";
  const isNaturalBJ = document.body.dataset.bj === "true";
  const bgm = document.getElementById('bgm');
  const toggle = document.getElementById('bgm-toggle');
  const bgmOverLay = document.getElementById('pien-bgm-overlay');
  const startBtn = document.getElementById('start-pien-bgm-btn');
  const skipBtn = document.getElementById('skip-pien-bgm-btn');
  const pienBgm = document.getElementById('pien-bgm');
  const pienCountEl = document.querySelector('.pien-count');
  const count = parseInt(document.body.dataset.resetCount || 0);


    // ナチュラルBJ演出
  if (isNaturalBJ) {
    const bj = document.getElementById('natural-bj');
    if (bj) bj.style.display = 'block';

    // ユーザーの操作後に再生（例えば画面クリック）
    window.addEventListener('click', () => {
      const sound = document.getElementById('bj-sound');
      sound.volume = 0.3;
      if (sound) {
        sound.play().catch(e => console.log("音再生エラー:", e));
      }
    }, { once: true }); // 一度だけ再生
  }

  // 勝利演出
  if (resultEl && text.includes('You Win')) {
    document.body.classList.add('win-animation');
    setTimeout(() => {
      document.body.classList.remove('win-animation');
    }, 4000);
  }

  // ぴえん発動条件：フラグが立ってたら
  if (isPien) {
    startPienRain();    // ぴえんを降らせ続ける
    setTimeout(gameOver, 7000);    // ぴえん秒数（ミリ秒）
  }

  // ぴえんBGM
  if (isPien && bgmOverLay && startBtn && pienBgm) {
    bgmOverLay.style.display = 'flex';

    // 音ありで泣く
    startBtn.addEventListener('click', () => {
      pienBgm.volume = 0.3;
      pienBgm.play().catch(e => console.warn("pienBGM再生エラー:", e));
      bgmOverLay.style.display = 'none';
    })

    // 音無しで我慢
    skipBtn.addEventListener('click', ()=> {
      // BGM再生せず、オーバーレイだけ消す
      console.log("音無しボタンが押されました");
      bgmOverLay.style.display = 'none';
    })
  }



  // ぴえんカウント押したら何か起きるやつ
  if (pienCountEl) {
    pienCountEl.style.cursor = 'pointer';
    pienCountEl.addEventListener('click', () => {
      if (count === 1) {
        showModal('初ぴえん…これからだね');
      } else if (count === 3) {
        showModal('3ぴえん…ぴえん道の入り口');
      } else if (count === 5) {
        showModal('5ぴえん！だいぶ泣いてきたね');
      } else if (count === 10) {
        showModal('🎉 10ぴえん達成！ぴえん中毒ですね 😵‍💫');
        repeatFireworks();

      } else if (count === 20) {
        showModal('🔥 20ぴえん記念！ぴえん女神の誕生 🍰');
        repeatFireworks();
        startHeartShower();

      } else if (count === 50) {
        showModal('🔥 50ぴえん！ぴえん業火に包まれる 🔥');
        repeatFireworks();
        document.body.classList.add('shake');
      } else if (count === 77) {
        showModal('💥 77ぴえん！ラッキーセブン揃い踏み 💥');
        console.log('7を表示する');
        launchLuckySeven(() => {
          repeatFireworks();
          hideSoundLuckySeven();
          console.log('repeatFireworks()の後');
        });
      } 
      else if (count === 100) {
        showModal('🎯 100ぴえん達成！ぴえんワールドが回る 🌪️');
        document.body.classList.add('spin-whole');
        repeatFireworks();
        startHeartShower();
        document.body.classList.add('shake');
        // 2秒後に戻す
        setTimeout(() => {
          document.body.classList.remove('spin-whole');
        }, 2000);
      }
      else if (count === 666) {
        trigger666();
        document.body.classList.add('invert-effect');

        document.getElementById('modal-close').onclick = () => {

          document.getElementById('rip-wrapper')?.remove();
          document.getElementById('demo-summon')?.remove();
        };
      }
    });
  }
});