import io
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMessage

from docxtpl import DocxTemplate


DOC_PATH = os.path.join(settings.BASE_DIR, 'doc_templates')


def docx_generation(doc_path, context):
    doc = DocxTemplate(doc_path)
    doc.render(context)
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer


def index(request):
    return render(request, 'documents_generator/index.html')


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

    context = {
        'agreement_place': agreement_place,
        'salesman_lastname': salesman_lastname,
        'salesman_firstname': salesman_firstname,
        'salesman_patronymic': salesman_patronymic,
        'salesman_id_number': salesman_id_number,
        'salesman_passport_number': salesman_passport_number,
        'salesman_passport_issue_date': salesman_passport_issue_date,
        'salesman_passport_issue_place': salesman_passport_issue_place,
        'salesman_residence_place': salesman_residence_place,
        'buyer_lastname': buyer_lastname,
        'buyer_firstname': buyer_firstname,
        'buyer_patronymic': buyer_patronymic,
        'buyer_id_number': buyer_id_number,
        'buyer_passport_number': buyer_passport_number,
        'buyer_passport_issue_date': buyer_passport_issue_date,
        'buyer_passport_issue_place': buyer_passport_issue_place,
        'buyer_residence_place': buyer_residence_place,
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

