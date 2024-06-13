document.getElementById('toggleButton').addEventListener('click', function() {
    var historyBar = document.getElementById('historyBar');
    var container = document.getElementById('container');
    var chatContainer = document.getElementById('chatContainer');
    if (historyBar.style.display === 'none') {
        historyBar.style.display = 'block';
        container.style.marginLeft = '350px';
        container.style.width = 'calc(100% - 350px)';
        chatContainer.style.width = 'calc(100% - 350px)'; /* 채팅창 너비 조정 */
        chatContainer.style.maxWidth = 'calc(100% - 50px)';
        container.style.justifyContent = 'center'; /* 컨테이너 중앙 정렬 */
        this.textContent = '▲';
    } else {
        historyBar.style.display = 'none';
        container.style.marginLeft = '0';
        container.style.width = '100%';
        chatContainer.style.width = '100%';
        chatContainer.style.maxWidth = 'calc(100% - 50px)';
        container.style.justifyContent = 'center'; /* 컨테이너 중앙 정렬 */
        this.textContent = '▼';
    }
});