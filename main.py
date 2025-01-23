import streamlit as st
from fpdf import FPDF
import tempfile
import os


def compute_factorial_differences(N):
    M = N - 1
    initial_values = [i ** M for i in range(1, N + 1)]
    initial_expressions = [f"{i}^{M}" for i in range(1, N + 1)]
    levels = [{'values': initial_values, 'expressions': initial_expressions}]

    current_values = initial_values.copy()
    current_expressions = initial_expressions.copy()

    while len(current_values) > 1:
        next_values = []
        next_expressions = []
        for i in range(len(current_values) - 1):
            diff = current_values[i + 1] - current_values[i]
            next_values.append(diff)
            expr = f"({current_expressions[i + 1]} - {current_expressions[i]})"
            next_expressions.append(expr)

        levels.append({
            'values': next_values[::-1],
            'expressions': next_expressions[::-1]
        })
        current_values = next_values
        current_expressions = next_expressions

    factorial_result = current_values[0] if current_values else None
    return factorial_result, levels


def calculate_factorial(N):
    try:
        N = int(N)
    except ValueError:
        return None, "Неверный ввод. Пожалуйста, введите положительное целое число.", None, None

    if N < 1:
        return None, "Неверный ввод. Пожалуйста, введите целое число больше или равное 1.", None, None

    M = N - 1

    try:
        factorial_result, levels = compute_factorial_differences(N)
        if factorial_result is None:
            return None, "Ошибка при вычислении разностей.", None, None

        digit_count = len(str(factorial_result))
        return factorial_result, digit_count, M, levels
    except Exception as e:
        return None, f"Ошибка вычисления: {str(e)}", None, None


def export_to_pdf(M, factorial_result, digit_count, levels):
    pdf = FPDF()
    pdf.add_page()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, 'DejaVuSans.ttf')
    if not os.path.exists(font_path):
        st.error("Файл шрифта не найден.")
        return None

    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', '', 10)

    pdf.cell(0, 10, f"Вычисление {M}! методом разностных уровней", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, f"Результат: {factorial_result} ({M}!)", ln=True)
    pdf.cell(0, 10, f"Количество цифр: {digit_count}", ln=True)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name


st.title("Вычисление факториала методом разностных уровней")

N_input = st.text_input("Введите число N", "5")

if st.button("Вычислить"):
    result, digit_count, M, levels = calculate_factorial(N_input)

    if result is not None:
        st.success(f"Результат: {result} ({M}!)")
        st.success(f"Количество цифр: {digit_count}")

        # Генерация PDF только с результатом
        pdf_path = export_to_pdf(M, result, digit_count, levels)
        if pdf_path:
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    "Скачать PDF",
                    pdf_file,
                    "factorial_calculation.pdf",
                    "application/pdf"
                )
        os.unlink(pdf_path)
    else:
        st.error(digit_count)