function adjustTextAreaHeight(textarea) {
  textarea.style.height = 'auto'; // 高さを一旦リセット
  textarea.style.height = textarea.scrollHeight + 'px'; // コンテンツの高さに設定
}

document.addEventListener('DOMContentLoaded', function () {
  const textArea = document.getElementById('user_input');
  textArea.addEventListener('input', function() {
      adjustTextAreaHeight(this);
  });
});
