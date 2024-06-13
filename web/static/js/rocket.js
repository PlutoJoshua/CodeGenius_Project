document.getElementById('emailForm').addEventListener('submit', function(event) {
    event.preventDefault(); // 기본 폼 제출을 막음
    const image = document.querySelector('.rocket img');
    image.classList.add('move-up');
    setTimeout(() => {
        this.submit(); // 폼을 1초 후에 제출
    }, 1000);
});