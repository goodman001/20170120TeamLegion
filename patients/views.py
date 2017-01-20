# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . import models
from entry.models import Entry

from doctor.functions import findall,finddata,savedata,updatedata,deldata,findallif,findallexcept
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from patients.models import Patient
from . import models
from entry.models import Entry
from django.http import HttpResponseRedirect

def index(request):
    if request.session.get("pat_id",None) != None and request.session.get("pat_id",None)>=0:
        #print request.session.get("doc_id",None)
        #print "hahaha"
        pat_id = request.session.get("pat_id",None)
        return HttpResponseRedirect('/patients/mainpage/'+str(pat_id))
    '''
    all_patients = models.Patient.objects.all()
    #template = loader.get_template('patients/index.html')
    context = {
        'all_patients': all_patients,
    }
    return render(request, 'patients/index.html', context)
    '''
    return render(request, 'patients/index.html')
def regpage(request):
    return render(request, 'patients/register.html')
def reg_store(request):
    if request.method == 'POST':
      username = request.POST['username']
      firstname = request.POST['firstname']
      lastname = request.POST['lastname']
      birthday = request.POST['birthday']
      pwd = request.POST['passwd']
      data0 = {"p_user_name":username}
      res = finddata(Patient,data0)
      if res == None:
         data = {"p_user_name":username,"p_first_name":firstname,"p_last_name":lastname,"p_birth_date":birthday,"p_password":pwd,"doc_id":"-1"}
         res2 = savedata(Patient,data)
         if res2 == 1:
            return render(request, 'patients/index.html')
         else:
            return HttpResponse('<html><script type="text/javascript">alert("Store into db fail!register fail!"); window.location="/patients/"</script></html>')
      else:
         return HttpResponse('<html><script type="text/javascript">alert("The patient has existed!register fail!"); window.location="/patients/"</script></html>')
      print data
    return HttpResponse("reg_store")
def logincheck(request):
    if request.method == 'POST':
       username = request.POST['username']
       pwd = request.POST['passwd']
       data0 = {"p_user_name":username,"p_password":pwd}
       res = finddata(Patient,data0)
       if res == None:
            return HttpResponse('<html><script type="text/javascript">alert("The username or password is wrong !"); window.location="/patients/"</script></html>')
       else:
            request.session["pat_id"] = res.id;
            return HttpResponseRedirect('/patients/mainpage/'+str(res.id))
            print "login success"
def mainpage(request,pat_id):
    if request.session.get("pat_id",None) == None or request.session.get("pat_id",None)<0:
        #print request.session.get("doc_id",None)
        #print "hahaha"
        return HttpResponseRedirect('/patients/')
    data_pat = {"id":int(request.session.get("pat_id",None))}
    res = finddata(Patient,data_pat)
    return render(request, 'patients/mainpage.html',{'patients':res})
def logoff(request):
    try:
        del request.session['pat_id']
    except:
        pass
    return HttpResponseRedirect('/patients/')
def detail(request, patient_id):


    # 

    queryset_list = Entry.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 5) 
    page_request_var = "page"

    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
        "object_list" : queryset,
        "title" : "List",
        "page_request_var":page_request_var
    }

    return render(request, "entry_list.html", context)

    # 


    # try:
    #     patient = models.Patient.objects.get(pk=patient_id)
    # except models.Patient.DoesNotExist:
    #     raise Http404("Patient does not exist")

    # return render(request, 'patients/detail.html', {'patient': patient})

def create(request):
    return HttpResponse("<h3> Create Patient Entries Page </h3>")

def update(request):
    return HttpResponse("<h3> Update Patient Entries Page </h3>")

def delete(request):
    return HttpResponse("<h4> Delete Patient Entries Page </h4>")
