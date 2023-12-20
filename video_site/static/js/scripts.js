//e7f3afa7f6bc747e9a10789a5ca62773
function showMovieDetails(movieId) {
    // movieIdが提供されていない場合のエラーハンドリングを追加
    if (!movieId) {
      console.error('No movie ID provided');
      return;
    }
  
    const apiKey = 'e7f3afa7f6bc747e9a10789a5ca62773';
    const url = `https://api.themoviedb.org/3/movie/${movieId}?api_key=${apiKey}&language=ja`;
  
    fetch(url)
      .then(response => response.json())
      .then(data => {
        console.log(data); // この行を追加してデバッグ情報を表示
        const modal = document.getElementById('movie-modal');
        document.getElementById('modal-movie-image').src = `https://image.tmdb.org/t/p/w500${data.poster_path}`;
        document.getElementById('modal-movie-title').textContent = data.title;
        document.getElementById('modal-movie-overview').textContent = data.overview;
  
        modal.style.display = 'block';
      })
      .catch(error => {
        console.error('Error fetching movie details:', error);
      });
  }
  
  
  function closeModal() {
    const modal = document.getElementById('movie-modal');
    modal.style.display = 'none';
  }
  