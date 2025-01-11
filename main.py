import streamlit as st
from mpmath import mp
from fpdf import FPDF
import tempfile
import os

# Функция для расчета M! где M = N - 1
def calculate_factorial(N):
    try:
        N = int(N)
    except ValueError:
        return None, "Неверный ввод. Пожалуйста, введите положительное целое число.", None

    if N < 1:
        return None, "Неверный ввод. Пожалуйста, введите целое число больше или равное 1.", None

    M = N - 1

    try:
        # Вычисляем M! как целое число
        factorial_result = mp.fac(M)
        # Преобразуем результат в строку без экспоненты и десятичной точки
        result_string = str(int(factorial_result))

        digit_count = len(result_string)

        return result_string, digit_count, M
    except Exception as e:
        return None, f"Ошибка вычисления: {str(e)}", None

# Функция для экспорта результата в PDF
def export_to_pdf(M, factorial_result, digit_count):
    pdf = FPDF()
    pdf.add_page()

    # Определяем путь к файлу шрифта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, 'DejaVuSans.ttf')

    # Проверяем, существует ли файл шрифта
    if not os.path.exists(font_path):
        st.error(f"Файл шрифта не найден по пути: {font_path}")
        return None

    # Добавляем шрифт DejaVu для поддержки кириллицы
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', '', 12)

    # Формула
    formula = f"Формула разницы: {M}!"
    pdf.multi_cell(0, 10, formula)

    # Количество цифр
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Результат содержит {digit_count} цифр.")

    # Сам факториал
    pdf.ln(10)

    # Для отображения большого числа можно разбить его на строки
    # Например, каждые 100 символов
    chunk_size = 100
    chunks = [factorial_result[i:i + chunk_size] for i in range(0, len(factorial_result), chunk_size)]
    factorial_text = f"{M}! =\n" + "\n".join(chunks)
    pdf.multi_cell(0, 10, factorial_text)

    # Сохраняем PDF во временный файл
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# Интерфейс Streamlit
st.title("Формула разницы")

N_input = st.text_input("Введите число (N)", "5")

if st.button("Вычислить"):
    result, digit_count_or_error, M = calculate_factorial(N_input)
    if result:
        st.success(f"Результат содержит {digit_count_or_error} цифр.")
        st.text(f"{M}! = {result}")

        # Создаем PDF и сохраняем путь к файлу
        pdf_path = export_to_pdf(M, result, digit_count_or_error)

        if pdf_path:
            # Предоставляем кнопку для скачивания PDF
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Скачать PDF",
                    data=pdf_file,
                    file_name="difference_formula.pdf",
                    mime="application/pdf"
                )
    else:
        st.error(digit_count_or_error)
