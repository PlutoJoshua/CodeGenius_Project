const keywords = ["JavaScript", "Python", "HTML", "CSS", "React", "Node.js", "Django"];
/*[
    {% for data in save_datas %}
        "{{ data.keyword }}"{% if not forloop.last %},{% endif %}
    {% endfor %}
];*/
const keywordBox = document.querySelector('.keyword-box');
const iconBasePath = "/static/img/";

/*const iconFiles = [
"icon1.jpg",
"icon2.jpg",
"icon3.jpg",
"icon4.jpg",
"icon5.jpg",
"icon6.jpg",
"icon7.jpg"
]; 아이콘 랜덤하게 불러올 경우 */

keywords.forEach((keyword, index) => {
    const keywordItem = document.createElement('div');
    keywordItem.className = 'keyword-item';

    const rank = document.createElement('div');
    rank.className = 'rank';
    rank.innerText = index + 1;

    const icon = document.createElement('img');
    icon.src = `${iconBasePath}icon${index + 1}.jpg`; // 아이콘 순서대로 불러올 경우

    /* const randomIcon = iconFiles[Math.floor(Math.random() * iconFiles.length)];
    icon.src = `${iconBasePath}${randomIcon}`;  아이콘 랜덤하게 불러올 경우*/

    const keywordText = document.createElement('div');
    keywordText.className = 'keyword';
    keywordText.innerText = keyword;

    keywordItem.appendChild(rank);
    keywordItem.appendChild(icon);
    keywordItem.appendChild(keywordText);

    keywordBox.appendChild(keywordItem);
});