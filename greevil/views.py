from django.shortcuts import render,HttpResponse
from django.http import HttpResponseNotAllowed
import boto3
from boto3.dynamodb.conditions import Key

def query_user(email):
    dynamodb = boto3.resource('dynamodb',region_name="us-east-1")
    
    table = dynamodb.Table('greevil-users')
    response = table.query(
        KeyConditionExpression=Key('CustomerId').eq(email)
    )
    return response['Items']




def start(request,email_id):
    
    # if not request.is_ajax() or not request.method=='POST':
        # return HttpResponseNotAllowed(['POST'])
    request.session['email'] = email_id
    return HttpResponse(email_id)
    
    # """Start page with a documentation.
    # """
    # email = email_id
    # return render(
    #     request,
    #     "greevil/start.html",
    #     {
    #         "nav_active": "start"
    #     }
    # )

def login(request):
    """Start page with a documentation.
    """
    return render(
        request,
        "greevil/login.html"
    )

def dashboard(request):
    """Dashboard page.
    """
    return render(
        request,
        "greevil/sb_admin_dashboard.html",
        {
            "nav_active": "dashboard"
        }
    )

def charts(request):
    """Charts page.
    """
    return render(request, "greevil/sb_admin_charts.html",
                  {"nav_active":"charts"})
def tables(request):
    """Tables page.
    """
    return render(request, "greevil/sb_admin_tables.html",
                  {"nav_active":"tables"})
def forms(request):
    """Forms page.
    """
    return render(request, "greevil/sb_admin_forms.html",
                  {"nav_active":"forms"})
def bootstrap_elements(request):
    """Bootstrap elements page.
    """
    return render(request, "greevil/sb_admin_bootstrap_elements.html",
                  {"nav_active":"bootstrap_elements"})
def bootstrap_grid(request):
    """Bootstrap grid page.
    """
    return render(request, "greevil/sb_admin_bootstrap_grid.html",
                  {"nav_active":"bootstrap_grid"})
def dropdown(request):
    """Dropdown  page.
    """
    return render(request, "greevil/sb_admin_dropdown.html",
                  {"nav_active":"dropdown"})
def rtl_dashboard(request):
    """RTL Dashboard page.
    """
    return render(request, "greevil/sb_admin_rtl_dashboard.html",
                  {"nav_active":"rtl_dashboard"})




def blank(request):
    """Blank page.
    """
    # user_details = query_user("acquil98@gmail.com")
    print(request.session["email"])
    user_details = query_user(request.session["email"])

    context = {
        'users':user_details,
        "nav_active":"blank"
        }
    return render(request, "greevil/sb_admin_blank.html",
                  context)
    

