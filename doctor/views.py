from django.shortcuts import render
from doctor.functions import findall,finddata,savedata,updatedata,deldata,findallif,findallexcept
from doctor.models import Doctor
from patients.models import Patient
from entry.models import Entry
import datetime
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    if request.session.get("doc_id",None) != None and request.session.get("doc_id",None)>=0:
        #print request.session.get("doc_id",None)
        #print "hahaha"
	doc_id = request.session.get("doc_id",None)
	return HttpResponseRedirect('/doctors/mainpage/'+str(doc_id))
    return render(request, 'doctor/index.html')
    #return HttpResponse("<h1> This is the Doctor app homepage</h1>")
def regpage(request):
    return render(request, 'doctor/register.html')
def reg_store(request):
    if request.method == 'POST':
       username = request.POST['username']
       firstname = request.POST['firstname']
       lastname = request.POST['lastname']
       birthday = request.POST['birthday']
       pwd = request.POST['passwd']
       data0 = {"d_user_name":username}
       res = finddata(Doctor,data0)
       if res == None:
           data = {"d_user_name":username,"d_first_name":firstname,"d_last_name":lastname,"d_birth_date":birthday,"d_password":pwd} 
           res2 = savedata(Doctor,data)
           if res2 == 1:
              return render(request, 'doctor/index.html')
           else:
              return HttpResponse('<html><script type="text/javascript">alert("Store into db fail!register fail!"); window.location="/doctors/"</script></html>')
       else:
           return HttpResponse('<html><script type="text/javascript">alert("The username has existed!register fail!"); window.location="/doctors/"</script></html>')
       print data
    return HttpResponse("reg_store")
def logincheck(request):
    if request.method == 'POST':
       username = request.POST['username']
       pwd = request.POST['passwd']
       data0 = {"d_user_name":username,"d_password":pwd}
       res = finddata(Doctor,data0)
       if res == None:
            return HttpResponse('<html><script type="text/javascript">alert("The username or password is wrong !"); window.location="/doctors/"</script></html>')
       else:
	    request.session["doc_id"] = res.id; 
            return HttpResponseRedirect('/doctors/mainpage/'+str(res.id))
            print "login success"
def mainpage(request,doc_id):
    if request.session.get("doc_id",None) == None or request.session.get("doc_id",None)<0:
	#print request.session.get("doc_id",None)
	#print "hahaha"
	return HttpResponseRedirect('/doctors/')
    data_if = {"doc_id": int(request.session.get("doc_id",None)) }
    res = findallif(Patient,data_if)
    data_doc = {"id":int(request.session.get("doc_id",None))}
    res_doc = finddata(Doctor,data_doc)
    #print res[0].p_first_name;
    return render(request, 'doctor/mainpage.html',{'patients':res,'docinfo':res_doc})
def updatepage(request):
    if request.session.get("doc_id",None) == None or request.session.get("doc_id",None)<0:
        #print request.session.get("doc_id",None)
        #print "hahaha"
        return HttpResponseRedirect('/doctors/')
    data_doc = {"id":int(request.session.get("doc_id",None))}
    res_doc = finddata(Doctor,data_doc)
    return render(request, 'doctor/updatedocinfo.html',{'docinfo':res_doc})
def addpage(request):
    if request.session.get("doc_id",None) == None or request.session.get("doc_id",None)<0:
        return HttpResponseRedirect('/doctors/')
    data = {"doc_id":request.session.get("doc_id",None)}
    res = findallexcept(Patient,data)
    return render(request, 'doctor/addpatientpage.html',{'patients':res})

def detail(request, doctor_id):
    return HttpResponse("<h2> Details for Doctor: " +str(doctor_id) + "</h2>")

def add(request,patient_id):
    if request.session.get("doc_id",None) == None or request.session.get("doc_id",None)<0:
        return HttpResponseRedirect('/doctors/')
    data={"id":int(patient_id)}
    datas={"doc_id": int(request.session.get("doc_id",None))}
    updatedata(Patient,data,datas)
    return HttpResponseRedirect('/doctors/mainpage/'+str(request.session.get("doc_id",None)))
    #return render(request, 'doctor/addpatient.html')

def update(request):
    if request.session.get("doc_id",None) == None or request.session.get("doc_id",None)<0:
        #print request.session.get("doc_id",None)
        #print "hahaha"
        return HttpResponseRedirect('/doctors/')
    doc_id = int(request.session.get("doc_id",None))
    if request.method == 'POST':
       username = request.POST['username']
       firstname = request.POST['firstname']
       lastname = request.POST['lastname']
       birthday = request.POST['birthday']
       pwd = request.POST['passwd']
       data0 = {"d_user_name":username}
       res = finddata(Doctor,data0)
       if res != None:
	   data = {"id":doc_id}
           datas = {"d_user_name":username,"d_first_name":firstname,"d_last_name":lastname,"d_birth_date":birthday,"d_password":pwd}
           updatedata(Doctor,data,datas)
	   return HttpResponseRedirect('/doctors/mainpage/'+str(doc_id))
       else:
           try:
	   	del request.session['doc_id']
           except:
		pass
           return HttpResponse('<html><script type="text/javascript">alert("The username has no existed!update fail!"); window.location="/doctors/"</script></html>')
 
    #return HttpResponse("<h3> Update Doctor Entries Page </h3>")

def delete(request,patient_id):
    if request.session.get("doc_id",None) == None or request.session.get("doc_id",None)<0:
        #print request.session.get("doc_id",None)
        #print "hahaha"
        return HttpResponseRedirect('/doctors/')
    data={"id":int(patient_id)}
    datas={"doc_id": None}
    updatedata(Patient,data,datas)
    return HttpResponseRedirect('/doctors/mainpage/'+str(request.session.get("doc_id",None))) 
    #return HttpResponse("<h4> Delete Doctor Entries Page </h4>")
def logoff(request):
    try:
        del request.session['doc_id']
    except:
        pass
    return HttpResponseRedirect('/doctors')
'''
timedelta = 0 : all time
timedelta = 1: one weeks ago
timedelta = 2: two weeks ago
timedelta = 3: three weeks ago
timedelta = 4: a month ago
timedelta = 5: two month ago
'''
def view_pic(request,patient_id):
    if request.session.get("doc_id",None) == None or request.session.get("doc_id",None)<0:
        #print request.session.get("doc_id",None)
        #print "hahaha"
        return HttpResponseRedirect('/doctors/')
    queryset_list = []
    data_pat = {"id": int(patient_id)}
    infos = finddata(Patient, data_pat)
    print infos.p_user_name
    try:
        timedelta = request.POST['condition']
        step = int(timedelta)
        d = datetime.datetime.now()
        if step in [1,2,3]:
            dayscount = datetime.timedelta(days=step*7)
            dayto = d - dayscount
            date_w= datetime.datetime(dayto.year, dayto.month, dayto.day)
            print str(date_w)
            queryset_list = Entry.objects.filter(timestamp__range=[date_w,d],user_id=int(patient_id))
        elif step in [4,5]:
            dayscount = datetime.timedelta(days=(step%3)*30)
            dayto = d - dayscount
            date_m= datetime.datetime(dayto.year, dayto.month, dayto.day)
            print str(date_m)
            queryset_list = Entry.objects.filter(timestamp__range=[date_m,d],user_id=int(patient_id))
        else:
            queryset_list = Entry.objects.filter(user_id=int(patient_id))
    except:
        queryset_list = Entry.objects.filter(user_id=int(patient_id))
    for item in queryset_list:
		print(item.timestamp)
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
        "page_request_var":page_request_var,
        "patient_id":patient_id,
        "patient_username":infos.p_first_name + '.' + infos.p_last_name
    }
    #queryset_list = Entry.objects.filter(user_id=res.id)
    # else:
    # 	queryset_list = Entry.objects.filter(user_id=0)
    #return HttpResponse("<h4> Delete Doctor Entries Page </h4>")
    return render(request, "doctor/viewpic_list.html", context)