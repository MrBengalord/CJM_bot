from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
from CJM_Bot import main

# Указание директории шаблонов при создании экземпляра Flask
app = Flask(__name__, template_folder='templates')
app.secret_key = "supersecretkey"  # For flash messages

@app.route('/')
def index():
    return render_template('CJM.html')  # Using the template name

@app.route('/result', methods=['POST'])
def result():
    try:
        input1 = request.form.get('input1')
        input2 = request.form.get('input2')
        stages = request.form.getlist('stages')
        options = request.form.getlist('options')
        file = request.files.get('file')
        print(stages)
        print(options)
        print(file)

        # Поля валидации
        if not input1 or not input2:
            flash("Категория и Клиент являются обязательными полями", "error")
            return redirect(url_for('index'))
        
        if not stages:
            flash("Необходимо выбрать хотя бы один этап", "error")
            return redirect(url_for('index'))

        if not options:
            flash("Необходимо выбрать хотя бы одну опцию", "error")
            return redirect(url_for('index'))


        # main function call with parameters
        generated_file_path = main(input1, input2, stages, options, file)
        
        if not generated_file_path:
            flash("Произошла ошибка при генерации файла. Пожалуйста, попробуйте снова", "error")
            return redirect(url_for('index'))

        results = {
            'input1': input1,
            'input2': input2,
            'stages': stages,
            'options': options,
            'file_filename': file.filename if file else 'No file uploaded',
            'generated_file_path': generated_file_path
        }

        return render_template('result.html', results=results)
    
    except Exception as e:
        flash(f"Произошла ошибка: {e}", "error")
        return redirect(url_for('index'))

@app.route('/download', methods=['POST'])
def download_file():
    filename = request.form.get('filename','{}')
    print(filename)
    
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
