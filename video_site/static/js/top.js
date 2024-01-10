document.addEventListener("DOMContentLoaded", function () {
    var menuBtn = document.getElementById("menu-btn-check");
    var menuContent = document.querySelector(".menu-content");

    menuBtn.addEventListener("mouseover", function () {
        menuContent.style.display = "block"; // メニューを表示
    });

    menuBtn.addEventListener("mouseout", function () {
        menuContent.style.display = "none"; // メニューを非表示
    });
});


//スクロールすると上部に固定させるための設定を関数でまとめる
function FixedAnime() {
    var headerH = $('#header').outerHeight(true);
    var scroll = $(window).scrollTop();
    if (scroll >= headerH){//headerの高さ以上になったら
        $('#header').addClass('fixed');//fixedというクラス名を付与
      }else{//それ以外は
        $('#header').removeClass('fixed');//fixedというクラス名を除去
      }
  }

//ナビゲーションをクリックした際のスムーススクロール
$('#g-navi a').click(function () {
    var elmHash = $(this).attr('href'); //hrefの内容を取得
    var pos = Math.round($(elmHash).offset().top-120);  //headerの高さを引く
    $('body,html').animate({scrollTop: pos}, 500);//取得した位置にスクロール※数値が大きいほどゆっくりスクロール
    return false;//リンクの無効化
  });
  
  
  // 画面をスクロールをしたら動かしたい場合の記述
  $(window).scroll(function () {
    FixedAnime();/* スクロール途中からヘッダーを出現させる関数を呼ぶ*/
  });
  
  // ページが読み込まれたらすぐに動かしたい場合の記述
  $(window).on('load', function () {
    FixedAnime();/* スクロール途中からヘッダーを出現させる関数を呼ぶ*/
  });


// フェード
const fade = document.querySelector('.fade');

const fadeKeyframes = {
  opacity: [0, 1],
}

const fadeOptions = {
  duration: 3000,
  easing: 'ease',
  fill: 'forwards',
}

fade.animate(fadeKeyframes, fadeOptions);
