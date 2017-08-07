from django.shortcuts import render,get_object_or_404,redirect,render_to_response,get_list_or_404
from django.utils import timezone
from .models import Post,FDataFrame,Person,ADataFrame
from .forms import PostForm
from .tables import PersonTable
from django_tables2 import RequestConfig
from itertools import chain
import random
import datetime
import time
import csv 
import statsmodels.tsa.arima_process as tsp
import numpy as np
import statsmodels.api as sm

import logging

logging.basicConfig(level=logging.DEBUG)

UNRULY_PASSENGERS = [146,184,235,200,226,251,299,273,
281,304,203, 134, 147]


def unruly_passengers_csv(request):
    #Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition']='attachment;filename=unruly.csv'
    
    writer =csv.writer(response)
    writer.writernow(['Year','Unruly Airline Passengers'])
    for(year,num) in zip(range(1995,2006),UNRULY_PASSENGERS):
        writer.writenow([year,num])
        
        
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def trend_plot(request,rules):
    #Adataframe =  ADataFrame.objects.filter(date2str=str(date))
    
    xdata1 =[]
    ydata5 =[]
    csvdata = ADataFrame.objects.filter(associationrules=str(rules),support_threshold='0.01')
    #csvdata1= csvdata.values('date2str')
    for l in csvdata:
        xdata1.append(l.date2str)
        ydata5.append(l.confidence)


    ydata5 = map(float,ydata5)
    xdata1 = map(int,xdata1)
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}

    chartdata = {
        'x': xdata1,
        'name1': 'confidence of Rule: {% rules %}', 'y1': ydata5, 'extra1': extra_serie,
    }

    charttype = "multiBarChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    ar = np.r_[1., -0.5, -0.2]; ma = np.r_[1., 0.2, -0.2]
    np.random.seed(123)
    x = tsp.arma_generate_sample(ar, ma, 20000, burnin=1000)
    sm.tsa.pacf(x, 5)
    ap = tsp.ArmaProcess(ar, ma)
    ap.pacf(5)     
    return render_to_response('blog/multibarchart.html', data)

    
def trend_plot_items(request,items):
    xdata1 =[]
    ydata5 =[]
    csvdata = FDataFrame.objects.filter(items=str(items),support_threshold='0.01')
    for l in csvdata:
        xdata1.append(l.date2str)
        ydata5.append(l.confidence)


    ydata5 = map(float,ydata5)
    xdata1 = map(int,xdata1)
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}

    chartdata = {
        'x': xdata1,
        'name1': 'confidence of Rule: {% rules %}', 'y1': ydata5, 'extra1': extra_serie,
    }

    charttype = "multiBarChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    ar = np.r_[1., -0.5, -0.2]; ma = np.r_[1., 0.2, -0.2]
    np.random.seed(123)
    x = tsp.arma_generate_sample(ar, ma, 20000, burnin=1000)
    sm.tsa.pacf(x, 5)
    ap = tsp.ArmaProcess(ar, ma)
    ap.pacf(5)     
    return render_to_response('blog/multibarchart.html', data)    


def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'blog/post_detail.html',{'post':post})
	
	
def post_new(request): 
    if request.method == "POST":
        form  = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail',pk = post.pk)
    else:
        form = PostForm()
    return render(request,'blog/post_edit.html',{'form':form})


def post_edit(request,pk):
    post = get_object_or_404(Post,pk =pk)
    if request.method == "POST":
        form  = PostForm(request.POST,instance = post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author=request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail',pk = post.pk)
    else:
        form = PostForm(instance = post)
    return render(request,'blog/post_edit.html',{'form':form})


def piechart(request):
    #xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    #ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    xdata1 =[]
    ydata1 =[]
    #xdata = FDataFrame.objects.get(frequentitems = 'C2, B2')
    #ydata = xdata.
    #csvdata = get_list_or_404(FDataFrame,frequentitems="C2, B2 ")
    #FDataFrame.objects.filter(frequentitems="C2, B2 ")
    #csvdata = ADataFrame.objects.filter(associationrules="Rule:('M474',)==>('B5', 'C4', 'FTDES523 ', 'HTVYY10000')",support_threshold='0.01') 
    csvdata = ADataFrame.objects.filter(associationrules__contains="Rule:('B5', 'FTDES459",support_threshold='0.01')
    for l in csvdata:
        xdata1.append(l.date2str)
        ydata1.append(l.confidence)
    #xdata1 = csvdata.date2str
    #ydata1 = csvdata.support
    
    chartdata = {'x': xdata1, 'y': ydata1}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
                'charttype': charttype,
                'chartdata': chartdata,
                'chartcontainer': chartcontainer,
                'extra': {
                    'x_is_date': False,
                    'x_axis_format': '',
                    'tag_script_js': True,
                    'jquery_on_ready': False,
            }
                            }
    return render_to_response('blog/piechart.html',data)
    

#def people(request):
    #Fdataframe = PersonTable(FDataFrame.objects.all())
    #RequestConfig(request).configure(Fdataframe)
    #RequestConfig(request, paginate={'per_page': 20}).configure(Fdataframe)
    #return render(request, 'blog/people.html', {'Fdataframe': Fdataframe})


def result_detail_date(request,date):
    """
    detail views of a day 
    Fdataframe1 = PersonTable(FDataFrame.objects.filter(date2str=str(date)))
    """
    """Fdataframe1 = FDataFrame.objects.filter(date2str=str(date))"""
    Adataframe =  ADataFrame.objects.filter(date2str=str(date)).filter(associationrules__contains='M').filter(associationrules__contains='FTDES')
    Fdataframe = PersonTable(Adataframe)
    RequestConfig(request).configure(Fdataframe)
    a = FDataFrame.objects.filter(date2str=str(date))
    b = PersonTable(a)
    RequestConfig(request).configure(b)
    #RequestConfig(request, paginate={'per_page': 20}).configure(Fdataframe)
    return render(request,'blog/result_detail.html',{'Fdataframe':Fdataframe, 'table': Fdataframe,'fdata':b})
    
    
def search_result(request):
    text = ''
    if request.method == "GET":
        text = request.GET.get('q')
        logging.debug("search text: %s",text) 
       
    # text = 'M471'
    results = ADataFrame.objects.filter(associationrules__contains = text).filter(associationrules__contains = 'FTDES').order_by('-confidence')
    Search_results = PersonTable(results)
    RequestConfig(request).configure(Search_results)
    return render(request,'blog/result_detail.html',{'table':Search_results}) 
     
def multibarchart(request):
    """
    multibarchart page
    """
    nb_element = 10
    xdata = range(nb_element)
    ydata = [random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)
    ydata3 = map(lambda x: x * 3, ydata)
    ydata4 = map(lambda x: x * 4, ydata)
    xdata1 =[]
    ydata5 =[]
    csvdata = ADataFrame.objects.filter(associationrules="Rule:('FTDES908  ', 'M427')==>('B5', 'HKTYY05208', 'C1')",support_threshold='0.01') 
    for l in csvdata:
        xdata1.append(l.date2str)
        ydata5.append(l.confidence)


    ydata5 = map(float,ydata5)
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}

    chartdata = {
        'x': xdata1,
        'name1': 'confidence of Rule:(FTDES908,M427)==>(B5, HKTYY05208, C1)', 'y1': ydata5, 'extra1': extra_serie,
       
    }

    charttype = "multiBarChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render_to_response('blog/multibarchart.html', data)

    
def scatterchart(request):
    """
    scatterchart page
    """
    nb_element = 50
    xdata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata1 = [i * random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata1)
    ydata3 = map(lambda x: x * 5, ydata1)
    xdata1 =[]
    ydata4 =[]
    csvdata = FDataFrame.objects.filter(frequentitems="C2, B2 ") 
    for l in csvdata:
        xdata1.append(l.date2str)
        ydata4.append(l.support)

    kwargs1 = {'shape': 'circle'}
    kwargs2 = {'shape': 'cross'}
    kwargs3 = {'shape': 'triangle-up'}

    extra_serie1 = {"tooltip": {"y_start": "", "y_end": " balls"}}

    chartdata = {
        'x': xdata1,
        'name1': 'support of (C2,B2) ', 'y1': ydata4, 'kwargs1': kwargs1, 'extra1': extra_serie1,
        
    }
    charttype = "scatterChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
    }
    return render_to_response('blog/scatterchart.html', data)    
    

def stackedareachart(request):
    """
    stackedareachart page
    """
    nb_element = 100
    xdata = range(nb_element)
    xdata = map(lambda x: 100 + x, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)

    extra_serie1 = {"tooltip": {"y_start": "", "y_end": " balls"}}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": " calls"}}

    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2,
    }
    charttype = "stackedAreaChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render_to_response('stackedareachart.html', data)
    
    
#def people(request):
#    Fdataframe = FDataFrame.objects.all()
#    return render(request, 'blog/people.html', {'people': Fdataframe})    


def people(request):
    Fdataframe = PersonTable(FDataFrame.objects.all())
    #RequestConfig(request).configure(Fdataframe)
    RequestConfig(request, paginate={'per_page': 20}).configure(Fdataframe)
    return render(request, 'blog/people.html', {'Fdataframe': Fdataframe})
    
    
def lineplusbarchart(request):
    """
   
    """
    start_time = int(time.mktime(datetime.datetime(2013, 9, 1).timetuple()) * 1000)
    nb_element = 30
    xdata = range(nb_element)
    ytickvalue = map(lambda x: x * 0.05,range(6))
    xdata = map(lambda x: start_time + x * 86330935+90000000, xdata)
    #xdata = map(int,xdata)
    ydata1 =[]
    csvdata = FDataFrame.objects.filter(frequentitems="item:('B5', 'C4')",support_threshold='0.02') 
    for l in csvdata:
        ydata1.append(l.support)
    
    #ydata1 = [float(i) for i in ydata1]
    ydata1 = map(float,ydata1)    
    #ydata1 = map(lambda x:x,ydata1)
    kwargs1 = {}
    kwargs1['bar'] = True

    tooltip_date = "%d %b %Y "
    extra_serie1 = {"tooltip": {"y_start": "$ ", "y_end": ""},
                    "date_format": tooltip_date}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": " min"},
                    "date_format": tooltip_date}
                       
    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata1, 'extra1': extra_serie1, 'kwargs1': kwargs1,
        'name2': 'series 2', 'y2': ydata1, 'extra2': extra_serie2,
    }

    charttype = "linePlusBarChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'focus_enable': True,
            'x_is_date': True,
            'yAxis.tickValues':ytickvalue ,              
        }
    }
    return render_to_response('blog/lineplusbarchart.html', data)
   
 
    """
def lineplusbarchart(request):
    """
    
    """
    start_time = int(time.mktime(datetime.datetime(2013, 9, 1).timetuple()) * 1000)
    nb_element = 100
    xdata = range(30)
    xdata = map(lambda x: start_time + x * 1000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = [i + random.randint(1, 10) for i in reversed(range(nb_element))]

    kwargs1 = {}
    kwargs1['bar'] = True

    tooltip_date = "%d %b %Y "
    extra_serie1 = {"tooltip": {"y_start": "$ ", "y_end": ""},
                    "date_format": tooltip_date}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": " min"},
                    "date_format": tooltip_date}

    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1, 'kwargs1': kwargs1,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2,
    }

    charttype = "linePlusBarChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'x_is_date':True,
            'focus_enable': True,
            'x_axis_format':"%d %b %Y"
        },
    }
    return render_to_response('blog/lineplusbarchart.html', data)
    """
    """
    from django.shortcuts import render_to_response
import random
import datetime
import time

def demo_lineplusbarchart(request):
    """
    """
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = 100
    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = [i + random.randint(1, 10) for i in reversed(range(nb_element))]

    kwargs1 = {}
    kwargs1['bar'] = True

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {"tooltip": {"y_start": "$ ", "y_end": ""},
                    "date_format": tooltip_date}
    extra_serie2 = {"tooltip": {"y_start": "", "y_end": " min"},
                    "date_format": tooltip_date}

    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1, 'kwargs1': kwargs1,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2,
    }

    charttype = "linePlusBarChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'focus_enable': True,
        },
    }
    return render_to_response('lineplusbarchart.html', data)
    """