# Create your views here.
import os
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib import messages 
from .forms import CustomUserForm,ContactForm,PDFForm
from .models import Certificate, Pdf
from django.views.generic import View
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from django.core.files import File
from django.conf import settings
from xhtml2pdf import pisa
import hashlib
from iota import Iota, ProposedTransaction, Tag, TryteString
import json
from pprint import pprint
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xhtml2pdf.default import DEFAULT_FONT


# Create your views here.
def index(request):
    print(request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

    form = ContactForm()
    context = {'form': form}
    return render(request, 'index.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('kblock:index')
        else:
            messages.info(request, 'Try again! Username or Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def register_page(request):
    if request.method != 'POST':
        form = CustomUserForm()
    else:
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)
            return redirect('kblock:login')

    context = {'form': form}

    return render(request, 'accounts/register.html', context)

@login_required(login_url='kblock:login')
def account(request):
    name = request.user
    data = Certificate.objects.filter(name__icontains = name)
    file = Pdf.objects.filter(name__icontains = name)
    userdata = zip(data, file)
    certif ={
        "data" : data,
        "certifs": userdata
    }
    return render(request, 'account.html', certif)

def commonarea(request):
    search = ""
    if request.GET.get('text'):
        search = request.GET.get('text')
  
    data = Certificate.objects.filter(name__icontains = search)
    certif= {
        "certifs": data,        
        "search" : search
    }
    return render(request,'commonarea.html',certif)

def checkhash(request):
    if request.method == 'POST':
        hash = request.POST.get('hash')
        file = request.FILES['file'].read()

        m = hashlib.sha256()
        m.update(file)
        file = m.hexdigest()

        if file == hash: 
            result = 'It is the same file!'
        else:
            result = 'The hash values are different, Not the same file!'
        print(file)
        print(hash)
        context = {'file': file , 'hash': hash , 'result': result}

        return render(request, 'checkhash.html', context)

    return render(request, 'checkhash.html')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class MessageView(LoginRequiredMixin,View):
    def get(self, request):
        #excludes = ['lorem 2', 'lorem 3']
        teacher = User.objects.exclude(id=1)
        form = PDFForm(data=request.GET)
        return render(request, 'generate_pdf.html', {'form': form , 'teachers': teacher })

    def post(self, request):
        form = PDFForm(data=request.POST)
        if form.is_valid():
            form.save()
            response = generate_pdf_response(context=form.cleaned_data)

            return response      

        return HttpResponse("ERROR 404")

def generate_pdf_response(context):
    obj = Certificate()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename={context['name']}.pdf"
    html = render_to_string("pdf.html", context=context)
    font_patch()
    status = pisa.CreatePDF(html,dest=response)
    filename = f"{context['name']+context['role']}.pdf"


    obj.name = f"{context['name']+context['role']}"
    # obj.datecreate = timezone.localtime(timezone.now())
    obj.pdf.save(filename, File(BytesIO(response.content)))
    
    m = hashlib.sha256()
    string = response.content
    m.update(string)
    string = m.hexdigest()
    print(string)

    Certificate.objects.filter(name=obj.name).update(hash = string)
    # print(hash(string))
    # print(hash(response.content))
    chain_data = {
        "hash": string,
        "name" : context['name'],
        "role": context['role'],
    }
    print(chain_data)
        
    hash = send_iota(chain_data)
    #bundle = fetch_iota(hash)

    Certificate.objects.filter(name=obj.name).update(web = 'https://explorer.iota.org/legacy-devnet/transaction/%s' % hash)

    if status.err:
        return HttpResponse("PDF文件生成失败")
    return response

#font problem
def font_patch():
    pdfmetrics.registerFont(TTFont('yh', '{}/theme/font/msyh.ttf'.format(
        settings.STATICFILES_DIRS[0])))
    DEFAULT_FONT['helvetica'] = 'yh'


def send_iota(json_data):
    api = Iota(
            adapter = 'https://nodes.devnet.iota.org:443',
            seed = "RVBKLUNYCLFIBNUKUEVKSCSAAUOTRXXHSXFQYOYST9LPZYPGBCJPVLGDLSKFIHXPCNBLZNHUQWXWPEYMM",
            testnet = True,
        )
    data = json_data
    json_data = json.dumps(data).encode()
    print('Constructing transaction locally...')
    string_data = TryteString.from_bytes(json_data)
    addr = api.get_new_addresses(index=42)['addresses'][0]
    tag = Tag(b'TESTTAG')
    tx = ProposedTransaction(
        address = addr,
        value = 0,
        tag = tag,
        message = string_data,
    )
    print('Sending transfer. . ')
    response = api.send_transfer([tx])
    print('Check your transaction on the Tangle!')
    print('https://explorer.iota.org/legacy-devnet/transaction/%s' % response['bundle'][0].hash)
    print('Tail transaction hash of the bundle is: %s' % response['bundle'].tail_transaction.hash)
    return  str(response['bundle'][0].hash)    

# def fetch_iota(hash):
#     api = Iota('https://nodes.devnet.iota.org:443', testnet=True)
#     print('Looking for bundle on the Tangle...')
#     bundle = api.get_transaction_objects(hashes=[hash])['transactions'][0]
#     bundle = bundle.as_json_compatible()
#     print('Extracting data from bundle...')
#     print('Succesfully:')
#     pprint(bundle)
#     return bundle
