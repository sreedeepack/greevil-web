import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from greevil.settings import APP_SERVER


def get_email(request):
    """
    Return email session value
    :param request:
    :return: session email
    """
    return request.session['email']


@csrf_exempt
def add_friend(request):
    """
    To add friends
    :param request:
    :return:
    """
    friend_id = request.POST.get('add-friend-email-input')
    id = request.session['email']
    data = {
        "your_id": id,
        "friend_id": friend_id
    }
    response = requests.post(f"{APP_SERVER}/user/add/friend/", json=data)
    json_response = response.json()
    exp_list = json_response['data']

    return JsonResponse({'Result': 'Added Successfully'})


@csrf_exempt
def add_expense(request):
    if request.method == "POST":
        email = get_email(request)
        data = {
            "email": email,
            "amount": request.POST.get('expense-amount-input'),
            'date': request.POST.get('expense-date-input'),
            'description': request.POST.get('expense-description-input'),
            'comments': request.POST.get('expense-comments-input'),
            'payor': request.POST.get('expense-by-input')
        }
        response = requests.post(f"{APP_SERVER}/expenses/add/", json=data)
        return JsonResponse({'Result': 'Successful'})

    else:
        return JsonResponse({'Result': 'Invalid Request'})


@csrf_exempt
def delete_expense(request):
    email = request.session['email']
    id = request.POST.get('id')
    data = {"id": id}
    response = requests.post(f"{APP_SERVER}/expenses/delete/", json=data)

    return JsonResponse({'Result': 'Success'})


@csrf_exempt
def start(request):
    request.session['email'] = request.POST.get('id')
    print("Request session success with", request.POST.get('id'))
    print(f"And request.session[email]={request.session['email']}")
    return JsonResponse({'Result': 'Success'})


def login(request):
    """
    Start page with a documentation.
    """
    return render(
        request,
        "greevil/login.html",
    )

def register(request):
    """
    New user registration page.
    """
    return render(
        request,
        "greevil/register.html",
    )


def register_confirm(request):
    """
    Confirmation with OTP
    """

    return render(
        request,
        "greevil/confirm.html",
    )


def dashboard(request):
    """
    Dashboard page.
    """
    email = get_email(request)
    print(f"Dashboard email {email}")

    data = {
        "email": email,
        # "from_date": "2020-10-27",
        # "to_date": "2020-10-27"
    }
    response = requests.post(f"{APP_SERVER}/user/view/expenses/", json=data)
    json_response = response.json()
    exp_list = json_response['data']
    print(f"Dashboard exp list {exp_list}")

    # TODO move this to app server

    # df = pd.DataFrame(exp_list).sort_values('Date')
    #
    #
    #
    # df['Amount'] = pd.to_numeric(df['Amount'])
    # df['Month'] = pd.to_numeric(df["Date"].apply(lambda x: x[5:7]))
    # df['Year'] = pd.to_numeric(df["Date"].apply(lambda x: x[0:4]))
    # df['Day'] = pd.to_numeric(df["Date"].apply(lambda x: x[8:10]))
    #
    # now = datetime.datetime.now()
    # area_chart = df[df['Year'] == now.year].groupby(['Date'])['Amount'].sum()
    # # bar_chart = df.groupby(['Month'])['Amount'].sum()
    #
    # new_expenses = df[(df['Year'] == now.year) & (df['Month'] == now.month) & (df['Day'] == now.day)]['Amount'].sum()
    # monthly_expenses = df[(df['Year'] == now.year) & (df['Month'] == now.month)]['Amount'].sum()
    #
    # friends_amount = df[(df['By'] != email) & (df['For'] == email)]['Amount'].sum()
    # owed_amount = df[('By' == email) & (df['For'] != email)]['Amount'].sum()
    #

    # context = {
    #     "monthly_expense": monthly_expenses,
    #     "friends_payment": friends_amount,
    #     "owed_amount": owed_amount,
    #     "new_expenses": new_expenses,
    #     "area_chart": area_chart.to_dict(),
    #     # "area_chart_y":area_chart.to_dict(),
    #     "expenses": exp_list,
    #     "nav_active": "dashboard"
    # }
    # context.update(aws_context)
    return render(
        request,
        "greevil/sb_admin_dashboard.html",
        # context
    )


def charts(request):
    """
    Charts page.
    """
    email = request.session['email']

    data = {
        "email": email,
    }
    response = requests.post(f"{APP_SERVER}/user/view/expenses/", json=data)
    json_response = response.json()
    exp_list = json_response['data']

    # df = pd.DataFrame(exp_list).sort_values('Date')
    # df['Amount'] = pd.to_numeric(df['Amount'])
    # df['Month'] = pd.to_numeric(df["Date"].apply(lambda x: x[5:7]))
    # df['Year'] = pd.to_numeric(df["Date"].apply(lambda x: x[0:4]))
    # df['Day'] = pd.to_numeric(df["Date"].apply(lambda x: x[8:10]))
    #
    # now = datetime.datetime.now()
    #
    # area_chart = df[df['Year'] == now.year].groupby(['Date'])['Amount'].sum()
    # bar_chart = df.groupby(['Month'])['Amount'].sum()
    #
    # friends_amount = df[(df['By'] != email) & (df['For'] == email)].groupby(['By'])['Amount'].sum()
    #
    # context = {
    #     "pie_chart": friends_amount.to_dict,
    #     "area_chart": area_chart.to_dict(),
    #     "bar_chart": bar_chart.to_dict(),
    #     "nav_active": "charts"
    # }

    return render(request, "greevil/sb_admin_charts.html", )
    # context)


def tables(request):
    """Tables page.
    """
    email = request.session['email']
    data = {"email": email, }
    response = requests.post(f"{APP_SERVER}/user/view/expenses/", json=data)
    json_response = response.json()
    expense_list = json_response['data']

    context = {
        "nav_active": "tables",
        "expenses": expense_list
    }
    return render(request, "greevil/sb_admin_tables.html",
                  context)


def forms(request):
    """Forms page.
    """
    return render(request, "greevil/sb_admin_forms.html",
                  {"nav_active": "forms"})


def bootstrap_elements(request):
    """Bootstrap elements page.
    """
    return render(request, "greevil/sb_admin_bootstrap_elements.html",
                  {"nav_active": "bootstrap_elements"})


def bootstrap_grid(request):
    """Bootstrap grid page.
    """
    return render(request, "greevil/sb_admin_bootstrap_grid.html",
                  {"nav_active": "bootstrap_grid"})


def dropdown(request):
    """Dropdown  page.
    """
    return render(request, "greevil/sb_admin_dropdown.html",
                  {"nav_active": "dropdown"})


def rtl_dashboard(request):
    """RTL Dashboard page.
    """
    return render(request, "greevil/sb_admin_rtl_dashboard.html",
                  {"nav_active": "rtl_dashboard"})


def add(request):
    """Blank page.
    Adding friends?
    """
    email = request.session["email"]

    response = requests.post(f"{APP_SERVER}/user/search/", json={"email": email})
    json_response = response.json()

    user_details = json_response['data']
    friends = user_details['friend_ids']

    context = {
        'users': email,
        'friends': friends,
        "nav_active": "add"
    }
    return render(request, "greevil/sb_admin_add.html",
                  context)
