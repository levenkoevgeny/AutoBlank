import io
import os
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils.html import escape

from docxtpl import DocxTemplate


DOC_PATH = os.path.join(settings.BASE_DIR, 'doc_templates')


def make_short_name(lastname, firstname, patronymic):
    parts = [lastname]
    if firstname:
        parts.append(f'{firstname[0]}.')
    if patronymic:
        parts.append(f'{patronymic[0]}.')
    return ' '.join(parts)


def fmt_date(value):
    if not value:
        return ''
    try:
        parts = value.split('-')
        return f'{parts[2]}.{parts[1]}.{parts[0]}'
    except (IndexError, AttributeError):
        return value


def number_to_words(num):
    ones = [
        '', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь',
        'восемь', 'девять', 'десять', 'одиннадцать', 'двенадцать',
        'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать',
        'семнадцать', 'восемнадцать', 'девятнадцать',
    ]
    tens = [
        '', '', 'двадцать', 'тридцать', 'сорок', 'пятьдесят',
        'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто',
    ]
    hundreds = [
        '', 'сто', 'двести', 'триста', 'четыреста', 'пятьсот',
        'шестьсот', 'семьсот', 'восемьсот', 'девятьсот',
    ]

    def conv(n, forms, gv=None):
        if n == 0 and not forms:
            return ''
        s = ''
        if n >= 100:
            s += hundreds[n // 100] + ' '
            n %= 100
        if n >= 20:
            s += tens[n // 10] + ' '
            n %= 10
        if 1 <= n < 20:
            s += ones[n] + ' '
        elif n > 0:
            s += ones[n] + ' '
        if forms:
            v = gv if gv is not None else n
            lt = v % 100
            lo = v % 10
            if 11 <= lt <= 19:
                s += forms[2] + ' '
            elif lo == 1:
                s += forms[0] + ' '
            elif 2 <= lo <= 4:
                s += forms[1] + ' '
            else:
                s += forms[2] + ' '
        return s

    if num == 0:
        return 'ноль'

    rub = int(num)

    formatted = f'{rub:,}'.replace(',', ' ')

    result = ''
    if rub >= 1000000:
        result += conv(rub // 1000000, ['миллион', 'миллиона', 'миллионов'])
    if rub >= 1000:
        result += conv((rub % 1000000) // 1000, ['тысяча', 'тысячи', 'тысяч'])
    result += conv(rub % 1000, ['', '', ''])
    result = result.strip()

    return f'{result}'


def docx_generation(doc_path, context):
    doc = DocxTemplate(doc_path)
    doc.render(context)
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer


def yandex_servise(request):
    return render(request, 'yandex_519162dd5d6ded9a.html')

def index(request):
    return render(request, 'documents_generator/index.html')

def favicon_view(request):
    favicon_path = os.path.join(settings.BASE_DIR, 'assets', 'img', 'favicon.ico')
    return FileResponse(open(favicon_path, 'rb'), content_type='image/x-icon')


def download_template(request):
    doc_path = os.path.join(DOC_PATH, 'Шаблон договора.docx')
    response = FileResponse(open(doc_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="Шаблон договора.docx"'
    return response



def generate_document(request):
    agreement_place = request.POST.get('agreement_place')
    salesman_lastname = request.POST.get('salesman_lastname')
    salesman_firstname = request.POST.get('salesman_firstname')
    salesman_patronymic = request.POST.get('salesman_patronymic')
    salesman_id_number = request.POST.get('salesman_id_number')
    salesman_passport_number = request.POST.get('salesman_passport_number')
    salesman_passport_issue_date = request.POST.get('salesman_passport_issue_date')
    salesman_passport_issue_place = request.POST.get('salesman_passport_issue_place')
    salesman_residence_place = request.POST.get('salesman_residence_place')

    buyer_lastname = request.POST.get('buyer_lastname')
    buyer_firstname = request.POST.get('buyer_firstname')
    buyer_patronymic = request.POST.get('buyer_patronymic')
    buyer_id_number = request.POST.get('buyer_id_number')
    buyer_passport_number = request.POST.get('buyer_passport_number')
    buyer_passport_issue_date = request.POST.get('buyer_passport_issue_date')
    buyer_passport_issue_place = request.POST.get('buyer_passport_issue_place')
    buyer_residence_place = request.POST.get('buyer_residence_place')

    type_car = request.POST.get('type_car')
    model_car = request.POST.get('model_car')
    year_car = request.POST.get('year_car')
    vin_car = request.POST.get('vin_car')
    reg_cert_number = request.POST.get('reg_cert_number')
    reg_cert_issue_date = request.POST.get('reg_cert_issue_date')
    reg_cert_issue_place = request.POST.get('reg_cert_issue_place')
    transfer_deadline = request.POST.get('transfer_deadline')
    acceptance_deadline = request.POST.get('acceptance_deadline')
    price = request.POST.get('price')
    payment_method = request.POST.get('payment_method')
    payment_date = request.POST.get('payment_date')

    salesman_full_name_short = make_short_name(salesman_lastname, salesman_firstname, salesman_patronymic)
    buyer_full_name_short = make_short_name(buyer_lastname, buyer_firstname, buyer_patronymic)

    context = {
        'agreement_place': agreement_place,
        'salesman_lastname': salesman_lastname,
        'salesman_firstname': salesman_firstname,
        'salesman_patronymic': salesman_patronymic,
        'salesman_id_number': salesman_id_number,
        'salesman_passport_number': salesman_passport_number,
        'salesman_passport_issue_date': fmt_date(salesman_passport_issue_date),
        'salesman_passport_issue_place': salesman_passport_issue_place,
        'salesman_residence_place': salesman_residence_place,
        'buyer_lastname': buyer_lastname,
        'buyer_lastnamer': buyer_lastname,
        'buyer_firstname': buyer_firstname,
        'buyer_patronymic': buyer_patronymic,
        'buyer_id_number': buyer_id_number,
        'buyer_passport_number': buyer_passport_number,
        'buyer_passport_issue_date': fmt_date(buyer_passport_issue_date),
        'buyer_passport_issue_place': buyer_passport_issue_place,
        'buyer_residence_place': buyer_residence_place,
        'type_car': type_car,
        'model_car': model_car,
        'year_car': year_car,
        'vin_car': vin_car,
        'reg_cert_number': reg_cert_number,
        'reg_cert_issue_date': fmt_date(reg_cert_issue_date),
        'reg_cert_issue_place': reg_cert_issue_place,
        'transfer_deadline': fmt_date(transfer_deadline),
        'acceptance_deadline': fmt_date(acceptance_deadline),
        'price': price,
        'price_words': number_to_words(float(price)) if price else '',
        'payment_method': payment_method,
        'payment_date': fmt_date(payment_date),
        'salesman_full_name_short': salesman_full_name_short,
        'buyer_full_name_short': buyer_full_name_short,
    }

    buffer = docx_generation(os.path.join(DOC_PATH, 'dogovor-kupli-prodazhy.docx'), context)
    buffer.seek(0)
    file_name = "Dogovor_kupli_prod.docx"

    email = EmailMessage(
        subject="Doc",
        body="Hi!",
        to=["it@amia.by"],
    )

    email.attach(
        f'{file_name}',
        buffer.read(),
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

    # email.send()

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    return response


def sitemap_xml(request):
    today = datetime.now().strftime('%Y-%m-%d')
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        '<url>'
        '<loc>https://autoblank.by/</loc>'
        '<lastmod>' + today + '</lastmod>'
        '<changefreq>monthly</changefreq>'
        '<priority>1.0</priority>'
        '</url>'
        '<url>'
        '<loc>https://autoblank.by/feedback</loc>'
        '<lastmod>' + today + '</lastmod>'
        '<changefreq>monthly</changefreq>'
        '<priority>0.7</priority>'
        '</url>'
        '</urlset>'
    )
    return HttpResponse(xml, content_type='application/xml')


def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.error(request, 'Заполните обязательные поля.')
            return render(request, 'documents_generator/feedback.html', {
                'form_data': {'name': name, 'email': email, 'subject': subject, 'message': message}
            })

        body = (
            f'Имя: {name}\n'
            f'Email: {email}\n'
            f'Тема: {subject}\n\n'
            f'Сообщение:\n{message}'
        )

        try:
            email_msg = EmailMessage(
                subject=f'[AutoBlank] Предложение: {subject}' if subject else '[AutoBlank] Предложение',
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[os.getenv('FEEDBACK_EMAIL', 'dolganovvvlad486@gmail.com')],
                reply_to=[email],
            )
            email_msg.send()
            messages.success(request, 'Ваше сообщение отправлено! Спасибо за обратную связь.')
            return redirect('gai:feedback')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            return render(request, 'documents_generator/feedback.html', {
                'form_data': {'name': name, 'email': email, 'subject': subject, 'message': message}
            })

    return render(request, 'documents_generator/feedback.html')

