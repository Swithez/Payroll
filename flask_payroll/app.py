import os
from flask import Flask, render_template, request, send_from_directory, session, make_response
from werkzeug.utils import secure_filename
from controllers.payroll import Payroll
from views.report_generator import ReportGeneratorFactory, ReportFormat
from werkzeug.exceptions import NotFound

app = Flask(__name__, template_folder='views')
UPLOAD_FOLDER = 'data/import'
EXPORT_FOLDER = 'data/export'
DEFAULT_EMPLOYEES_FILE = os.path.join(UPLOAD_FOLDER, 'employees.json')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)
ALLOWED_EXTENSIONS = {'json'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    payroll = None
    error = None
    file_path = session.get('file_path')
    statistics = None

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                session['file_path'] = file_path
            else:
                error = "Incorrect file or format"
        else:
            session.pop('file_path', None)

    try:
        payroll = Payroll()
        if file_path:
            payroll.import_employees_from_json(file_path)
        else:
            payroll.import_employees_from_json(DEFAULT_EMPLOYEES_FILE)
            file_path = DEFAULT_EMPLOYEES_FILE
        statistics = payroll.get_statistics()
    except Exception as e:
        error = str(e)

    if request.method == 'POST' and request.form.get('format'):
        try:
            format_type = ReportFormat[request.form['format']]
            report_generator = ReportGeneratorFactory.get_report_generator(format_type)
            report_generator.generate_report(payroll)
            report_filename = f"payroll_report.{format_type.value}"
            report_path = os.path.join(EXPORT_FOLDER, report_filename)
            report_generator.save_report(payroll, report_path)

            print(f"Report saved to: {report_path}")

            try:
                response = make_response(send_from_directory(directory=EXPORT_FOLDER, path=report_filename, as_attachment=True))
                response.headers['Content-Disposition'] = f'attachment; filename={report_filename}'
                return response
            except NotFound:
                error = f"File not found: {report_filename}"

        except KeyError:
            error = "Необходимо выбрать формат отчёта" # Сообщение об ошибке
        except Exception as e:
            error = str(e)

    return render_template('index.html', payroll=payroll, error=error, file_path=file_path, statistics=statistics)

if __name__ == '__main__':
    app.run(debug=True)