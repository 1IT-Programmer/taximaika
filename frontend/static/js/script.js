window.onload = function() {
    console.log("Frontend JavaScript loaded.");
};

// Обработчик события кликов по ссылке "logout"
const logoutLink = document.getElementById('logout-link');
if (logoutLink) {
    logoutLink.addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем переход по ссылке
        fetch('/logout', {
            method: 'GET',
            credentials: 'include'
        }).then(response => {
            window.location.href = '/'; // Переходим на главную страницу после выхода
        });
    });
}

// Обработка ошибок при входе или регистрации
const errorMessage = document.getElementById('error-message');
if (errorMessage) {
    errorMessage.style.display = 'none'; // Изначально скрыто
}

// Пример: обработка результатов AJAX-запроса
fetch('/some-api-endpoint', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({key: 'value'})
}).then(response => {
    if (!response.ok) throw Error(response.statusText); // Обрабатываем ошибку
    return response.json();
}).then(data => {
    console.log('Success:', data);
}).catch(error => {
    console.error('Error:', error);
    errorMessage.innerText = 'Ошибка при выполнении запроса.';
    errorMessage.style.display = 'block';
});
