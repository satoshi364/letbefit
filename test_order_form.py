import pytest
from playwright.sync_api import sync_playwright

# Параметризация теста для разных браузеров
@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_order_form(browser_name):
    with sync_playwright() as p:
        # Открываем браузер в зависимости от параметра
        browser = getattr(p, browser_name).launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.set_default_timeout(300000)

        # Задание 2: Проверка корректности всех полей ввода (первая форма с телефоном)
        # Переходим на сайт с формой заказа
        page.goto("https://letbefit.ru")

        # Проверяем корректность работы поля для телефона
        page.fill('input[name="phone"]', '+79631059876')  # Корректное значение
        assert page.input_value('input[name="phone"]') == '+79631059876'  # Проверяем ввод

        # Задание 3: Убедитесь, что все обязательные поля формы отмечены
        # Проверяем обязательное поле: очищаем и пытаемся отправить
        page.fill('input[name="phone"]', '')  # Очищаем поле телефона
        page.click('button:has-text("Оформить")')  # Нажимаем на "Оформить"
        error_message = page.text_content('css-селектор или xpath к элементу ошибки для телефона')
        print("Сообщение об ошибке (телефон):", error_message)
        assert error_message is not None  # Убедитесь, что сообщение об ошибке появилось

        # Задание 4: Проведите проверку на ввод некорректных данных
        # Проверяем ввод некорректного значения телефона
        page.fill('input[name="phone"]', '123')  # Некорректное значение
        page.click('button:has-text("Оформить")')
        error_message = page.text_content('css-селектор или xpath к элементу ошибки для телефона')
        print("Сообщение об ошибке (некорректный телефон):", error_message)
        assert error_message is not None  # Сообщение об ошибке должно появиться

        # Задание 5: Проверьте, корректно ли работает кнопка отправки формы
        # Проверяем, что кнопка активируется после заполнения всех обязательных полей
        page.fill('input[name="phone"]', '+79631059876')  # Корректное значение
        assert page.is_enabled('button:has-text("Оформить")')  # Кнопка должна быть активна

        # Переходим ко второй форме после нажатия "Оформить"
        page.click('button:has-text("Оформить")')

        # Задание 2 и 3: Проверка полей на второй форме (имя и email обязательные поля)
        # Переходим к форме с полями для имени и email
        page.fill('input[name="name"]', 'Тест Тестович')  # Корректное значение для имени
        page.fill('input[name="email"]', 'test@example.com')  # Корректное значение для email
        assert page.input_value('input[name="name"]') == 'Тест Тестович'  # Проверяем ввод имени
        assert page.input_value('input[name="email"]') == 'test@example.com'  # Проверяем ввод email

        # Задание 4: Проверьте на некорректные данные (некорректный email)
        page.fill('input[name="email"]', 'invalid_email')  # Некорректный email
        page.click('button:has-text("Оформить")')
        error_message = page.text_content('css-селектор или xpath к элементу ошибки для email')
        print("Сообщение об ошибке (некорректный email):", error_message)
        assert error_message is not None  # Сообщение об ошибке должно появиться

        # Задание 5: Проверьте, что кнопка активируется после заполнения обязательных полей
        page.fill('input[name="name"]', 'Тест Тестович')  # Корректное имя
        page.fill('input[name="email"]', 'test@example.com')  # Корректный email
        assert page.is_enabled('button:has-text("Оформить")')  # Кнопка активна после заполнения полей

        # Задание 6: Убедитесь, что отображается сообщение об успешной отправке формы
        page.click('button:has-text("Оформить")')
        success_message = page.text_content('css-селектор или xpath к элементу подтверждения заказа')
        print("Сообщение об успешной отправке:", success_message)
        assert success_message is not None  # Проверяем наличие сообщения о подтверждении заказа

        # Задание 7: Кросс-браузерное тестирование
        # Запускаем тесты сразу в нескольких браузерах: Chromium, Firefox и WebKit, используя параметризацию pytest.

        # Закрываем браузер после завершения теста
        browser.close()