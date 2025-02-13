document.addEventListener('DOMContentLoaded', function() {
    var buttonImport = document.createElement('button');
    buttonImport.type = 'button';
    buttonImport.id = 'import_csv_btn';
    buttonImport.textContent = 'Импотрировать CSV';
    applyCustomStyles(buttonImport);

    var buttonExport = document.createElement('button');
    buttonExport.type = 'button';
    buttonExport.id = 'export_csv_btn';
    buttonExport.textContent = 'Экспортировать CSV';
    applyCustomStyles(buttonExport);

    var objectTools = document.querySelector('.object-tools');

    if (objectTools) {
        objectTools.appendChild(buttonImport);
        objectTools.appendChild(buttonExport);

        // Обработчик импорта CSV
        buttonImport.addEventListener('click', function() {
            var input = document.createElement('input');
            input.type = 'file';
            input.accept = '.csv';
            input.id = 'csvInput';

            var dialog = document.createElement('div');
            dialog.style.position = 'fixed';
            dialog.style.top = '50%';
            dialog.style.left = '50%';
            dialog.style.transform = 'translate(-50%, -50%)';
            dialog.style.padding = '20px';
            dialog.style.backgroundColor = '#000';
            dialog.style.boxShadow = '0 0 10px rgba(0,0,0,0.5)';
            dialog.style.zIndex = '1000';

            var p = document.createElement('p');
            p.textContent = 'Выберите CSV-файл:';
            dialog.appendChild(p);
            dialog.appendChild(input);

            var uploadButton = document.createElement('button');
            uploadButton.textContent = 'Загрузить';
            applyCustomStyles(uploadButton);

            uploadButton.addEventListener('click', function() {
                var file = input.files[0];
                if (!file) {
                    alert('Выберите CSV-файл');
                    return;
                }

                var formData = new FormData();
                formData.append('file', file);

                const csrfToken = getCookie('csrftoken');

                var xhr = new XMLHttpRequest();
                xhr.open('POST', window.location.origin + '/admin/models/news/import-csv/', true);
                xhr.setRequestHeader('X-CSRFToken', csrfToken);

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        alert('CSV успешно импортирован');
                        location.reload();
                    } else {
                        alert('Ошибка при импорте CSV');
                    }
                };

                xhr.send(formData);
            });

            dialog.appendChild(uploadButton);
            document.body.appendChild(dialog);
        });

        // Обработчик экспорта CSV
        buttonExport.addEventListener('click', function() {
            const csrfToken = getCookie('csrftoken');
            var xhrExport = new XMLHttpRequest();
            xhrExport.open('GET', window.location.origin + '/admin/models/news/export-csv/', true);
            xhrExport.responseType = 'blob';

            xhrExport.onload = function() {
                if (xhrExport.status === 200) {
                    var blob = xhrExport.response;
                    var link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = 'export_news_data.csv';
                    link.click();

                    alert('Экспорт CSV успешно завершен');
                } else {
                    alert('Ошибка экспорта CSV');
                }
            };

            xhrExport.setRequestHeader('X-CSRFToken', csrfToken);
            xhrExport.send();
        });
    }

    // ✅ Применяем стили к элементам
    function applyCustomStyles(button) {
        button.style.display = 'block';
        button.style.float = 'left';
        button.style.padding = '8px 12px';
        button.style.background = 'var(--object-tools-bg)';
        button.style.color = 'var(--object-tools-fg)';
        button.style.fontWeight = '400';
        button.style.fontSize = '0.6875rem';
        button.style.textTransform = 'uppercase';
        button.style.letterSpacing = '0.5px';
        button.style.border = 'none';
        button.style.borderRadius = '15px';
        button.style.cursor = 'pointer';
        button.style.marginRight = '10px';
        button.style.transition = 'background 0.3s ease';
    }

    // ✅ Получаем CSRF-токен из cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
