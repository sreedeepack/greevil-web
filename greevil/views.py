import json, time, hashlib, datetime
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseNotAllowed,JsonResponse
import boto3
from boto3.dynamodb.conditions import Key
from django.views.decorators.csrf import csrf_exempt
from botocore.exceptions import ClientError
import pandas as pd

def query_user(email, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name="us-east-1")
    
    table = dynamodb.Table('greevil-users')
    response = table.get_item(
        Key={'CustomerId':email}
    )
    return response['Item']


@csrf_exempt
def add_friend(request, dynamodb=None):
    email = request.POST.get('add-friend-email-input')
    id = request.session['email']

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name="us-east-1")

    db_user = query_user(email)
    db_source = query_user(id)
    if db_user==[]:
        return JsonResponse({'Result':'No users Found'})
    elif email == id or email in db_source[0]['Friends']:
        return JsonResponse({'Result':'Already exists!'})

    table = dynamodb.Table('greevil-users')

    response = table.update_item(
        Key={
             'CustomerId' : id 
        }, 
        UpdateExpression="set Friends = list_append(if_not_exists(Friends,:empty_list), :i)",
        ExpressionAttributeValues={
            ':i': [email],
            ':empty_list' : []
        },
    ReturnValues="UPDATED_NEW"
    )

    response = table.update_item(
        Key={
             'CustomerId' : email 
        }, 
        UpdateExpression="set Friends = list_append(if_not_exists(Friends,:empty_list), :i)",
        ExpressionAttributeValues={
            ':i': [id],
            ':empty_list' : []
        },
    ReturnValues="UPDATED_NEW"
    )

    return JsonResponse({'Result':'Added Successfully'})


def add_expense_user_helper(dynamodb, by_id, for_id, h):
    table = dynamodb.Table('greevil-users')

    response = table.update_item(
            Key={
                'CustomerId' : for_id 
            }, 
            UpdateExpression="set Expenses = list_append(if_not_exists(Expenses,:empty_list), :i)",
            ExpressionAttributeValues={
                ':i': [h],
                ':empty_list' : []
            },
        ReturnValues="UPDATED_NEW"
        )
    
    # Paid by someone else
    if by_id != for_id:        
        response = table.update_item(
            Key={
                'CustomerId' : by_id 
            }, 
            UpdateExpression="set Expenses = list_append(if_not_exists(Expenses,:empty_list), :i)",
            ExpressionAttributeValues={
                ':i': [h],
                ':empty_list' : []
            },
        ReturnValues="UPDATED_NEW"
        )

# POST data
@csrf_exempt
def add_expense(request,dynamodb=None):
    
    if request.method == "POST" :
        email = request.session['email']
        s = str(time.time()) + str(email)
        h = hashlib.md5(s.encode('utf-8')).hexdigest()
        

        if not dynamodb:
            dynamodb = boto3.resource('dynamodb',region_name="us-east-1")

        table = dynamodb.Table('greevil-expenses')
        
        response = table.put_item(
            Item={
                    'ExpenseId': h,
                    'Amount': request.POST.get('expense-amount-input'),
                    'Date': request.POST.get('expense-date-input'),
                    'Description':request.POST.get('expense-description-input'),
                    'Comments': request.POST.get('expense-comments-input'),
                    'For': email,
                    'By': request.POST.get('expense-by-input')
                }
        )      
        add_expense_user_helper(dynamodb, request.POST.get('expense-by-input'), email, h)
        # return render("greevil/tables.html")
        return JsonResponse({'Result':'Successful'})
        

    else:
        return JsonResponse({'Result':'Invalid Request'})
        


def query_expenses(expense_id, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name="us-east-1")

    table = dynamodb.Table('greevil-expenses')
    response = table.get_item(
        Key={'ExpenseId':expense_id}
    )
    return response['Item']


@csrf_exempt
def delete_expense(request,dynamodb=None):
    
    email = request.session['email']
    id = request.POST.get('id')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb',region_name="us-east-1")

    table = dynamodb.Table('greevil-expenses')    
    
    response = query_expenses(id, dynamodb)
    by_id = response["By"]
    for_id = response["For"]
    print("part 1")
    by_id_expenses = query_user(by_id, dynamodb)["Expenses"]
    for_id_expenses = query_user(for_id, dynamodb)["Expenses"]
    by_id_expenses.remove(id)
    for_id_expenses.remove(id)
    print("part 2")

    try:
        table.delete_item(
            Key={
                'ExpenseId': id
            }
        )
        print("part 3")

        # Remove from users
        table = dynamodb.Table('greevil-users')
        table.update_item(
            Key={
                'CustomerId' : for_id 
            }, 
            UpdateExpression="set Expenses = :i",
            ExpressionAttributeValues={
                ':i': for_id_expenses,
            },
        ReturnValues="UPDATED_NEW"
        )
        if by_id != for_id:
            table.update_item(
                Key={
                    'CustomerId' : by_id 
                }, 
                UpdateExpression="set Expenses = :i",
                ExpressionAttributeValues={
                    ':i': by_id_expenses,
                },
                ReturnValues="UPDATED_NEW"
            )


    except ClientError as e:
        print(e.response['Error']['Message'])
        return JsonResponse({'Result':'Invalid Request'})

    
    return JsonResponse({'Result':'Success'})


@csrf_exempt
def start(request):
    print("start")
    print(request.method)

    if not request.is_ajax() or not request.method=='POST':
        return JsonResponse({'Result':'Forbidden'})
        
        # return HttpResponseNotAllowed(['POST'])
    
    request.session['email'] = request.POST.get('id')
    print("Request session success with",request.POST.get('id'))
    return JsonResponse({'Result':'Success'})

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
    email = request.session['email']
    l=[]
    for expenses in query_user(email)['Expenses']:
        l.append(query_expenses(expenses))
    df = pd.DataFrame(l).sort_values('Date')
    df['Amount']= pd.to_numeric(df['Amount'])
    df['Month']= pd.to_numeric(df["Date"].apply(lambda x:x[5:7]))
    df['Year']= pd.to_numeric(df["Date"].apply(lambda x:x[0:4]))
    df['Day']= pd.to_numeric(df["Date"].apply(lambda x:x[8:10]))

    now = datetime.datetime.now()
    area_chart = df[df['Year']==now.year].groupby(['Date'])['Amount'].sum()
    # bar_chart = df.groupby(['Month'])['Amount'].sum()

    new_expenses =  df[(df['Year']==now.year) & (df['Month']==now.month) & (df['Day']==now.day)]['Amount'].sum()
    monthly_expenses =  df[(df['Year']==now.year) & (df['Month']==now.month)]['Amount'].sum()

    friends_amount =  df[(df['By']!=email) & (df['For']==email)]['Amount'].sum()
    owed_amount =  df[('By'==email) & (df['For']!=email)]['Amount'].sum()


    context={
        "monthly_expense":monthly_expenses,
        "friends_payment":friends_amount,
        "owed_amount":owed_amount,
        "new_expenses":new_expenses,
        "area_chart":area_chart.to_dict(),
        # "area_chart_y":area_chart.to_dict(),
        "expenses":l,
        "nav_active": "dashboard"
    }
    return render(
        request,
        "greevil/sb_admin_dashboard.html",
        context
    )

def charts(request):
    """Charts page.
    """
    email = request.session['email']
    l=[]
    for expenses in query_user(email)['Expenses']:
        l.append(query_expenses(expenses))

    df = pd.DataFrame(l).sort_values('Date')
    df['Amount']= pd.to_numeric(df['Amount'])
    df['Month']= pd.to_numeric(df["Date"].apply(lambda x:x[5:7]))
    df['Year']= pd.to_numeric(df["Date"].apply(lambda x:x[0:4]))
    df['Day']= pd.to_numeric(df["Date"].apply(lambda x:x[8:10]))

    now = datetime.datetime.now()

    area_chart = df[df['Year']==now.year].groupby(['Date'])['Amount'].sum()
    bar_chart = df.groupby(['Month'])['Amount'].sum()

    
    friends_amount =  df[(df['By']!=email) & (df['For']==email)].groupby(['By'])['Amount'].sum()
    

    context={
        "pie_chart":friends_amount.to_dict,
        "area_chart":area_chart.to_dict(),
        "bar_chart":bar_chart.to_dict(),
        "nav_active": "charts"
    }

    return render(request, "greevil/sb_admin_charts.html",
                  context)

def tables(request):
    """Tables page.
    """
    email = request.session['email']
    expense_list = []
    # print(query_user(email)['Expenses'])
    for expenses in query_user(email)['Expenses']:
        expense_list.append(query_expenses(expenses))
    # print(expense_list)
    context={
        "nav_active":"tables",
        "expenses":expense_list
    }
    return render(request, "greevil/sb_admin_tables.html",
                  context)


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
    print(request.session["email"])
    user_details = query_user(request.session["email"])
    friends = user_details['Friends']
    context = {
        'users':user_details['Email'],
        'friends': friends,
        "nav_active":"blank"
        }
    return render(request, "greevil/sb_admin_blank.html",
                  context)
    

