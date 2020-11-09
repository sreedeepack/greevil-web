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
    print(response)
    json_response = response.json()
    exp_list = json_response['data']
    return JsonResponse({'Result': 'Added Successfully'})


@csrf_exempt
def add_expense(request):
    print("Django add_expense")
    # email = get_email(request)
    email = request.session['email']
    data = {
        "email": request.POST.get('expense-for-input'),
        "amount": request.POST.get('expense-amount-input'),
        'date': request.POST.get('expense-date-input'),
        'description': request.POST.get('expense-description-input'),
        'comments': request.POST.get('expense-comments-input'),
        'payor': request.POST.get('expense-by-input')
    }
    if data['email'] == data['payor'] and data['email'] != email:
        return JsonResponse({"Result": "Sorry! You cannot do that!"})

    response = requests.post(f"{APP_SERVER}/expenses/add/", json=data)

    return JsonResponse({'Result': 'Added Successfully'})


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
    context = {
        "APP_SERVER": APP_SERVER
    }
    return render(
        request,
        "greevil/login.html",
        context
    )


def logout(request):
    """
    Logout
    """


def register(request):
    """
    New user registration page.
    """
    context = {
        "APP_SERVER": APP_SERVER
    }
    return render(
        request,
        "greevil/register.html",
        context
    )


def forgot_view(request):
    """

    """
    context = {
        "APP_SERVER": APP_SERVER
    }
    return render(
        request,
        "greevil/forgot_password.html",
        context
    )


def forgot_confirm_view(request):
    """

    """
    context = {
        "APP_SERVER": APP_SERVER
    }
    return render(
        request,
        "greevil/forgot_confirm.html",
        context
    )


def register_confirm(request):
    """
    Confirmation with OTP
    """
    context = {
        "APP_SERVER": APP_SERVER
    }
    return render(
        request,
        "greevil/confirm.html",
        context
    )


def dashboard(request):
    """
    Dashboard page.
    """
    email = get_email(request)

    data = {
        "email": email,
        # "from_date": "2020-10-27",
        # "to_date": "2020-10-27"
    }
    response = requests.post(f"{APP_SERVER}/expenses/stats/", json=data)
    json_response = response.json()
    exp_list = json_response['data']['exp_list']

    area_chart = json_response['data']['area_chart']
    bar_chart = json_response['data']['bar_chart']

    new_expenses = json_response['data']['new_expenses']
    monthly_expenses = json_response['data']['monthly_expenses']

    friends_amount = json_response['data']['friends_amount']
    owed_amount = json_response['data']['owed_amount']

    context = {
        "monthly_expense": monthly_expenses,
        "friends_payment": friends_amount,
        "owed_amount": owed_amount,
        "new_expenses": new_expenses,
        "area_chart": area_chart,
        "area_chart_y": area_chart,
        "expenses": exp_list,
        "nav_active": "dashboard"
    }

    return render(
        request,
        "greevil/sb_admin_dashboard.html",
        context
    )


def charts(request):
    """
    Charts page.
    """
    email = get_email(request)

    data = {
        "email": email,
        # "from_date": "2020-10-27",
        # "to_date": "2020-10-27"
    }
    headers = {
        'Accept': 'application/xml',
    }
    response = requests.post(f"{APP_SERVER}/expenses/stats/predict/", json=data, headers=headers)
    xml_response = response.text
    prediction_area_chart = xml_response

    response = requests.post(f"{APP_SERVER}/expenses/stats/", json=data)
    json_response = response.json()

    area_chart = json_response['data']['area_chart']
    bar_chart = json_response['data']['bar_chart']
    pie_chart = json_response['data']['pie_chart']

    context = {
        "prediction_area_chart": str(prediction_area_chart),
        "pie_chart": pie_chart,
        "area_chart": area_chart,
        "bar_chart": bar_chart,
        "nav_active": "charts"
    }

    return render(request,
                  "greevil/sb_admin_charts.html",
                  context)


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


def handler404(request, exception, template_name="greevil/404.html"):
    """Custom 404  page.
    """
    response = render(request, template_name)
    response.status_code = 404
    return response


def handler500(request, exception, template_name="greevil/500.html"):
    """Custom 500  page.
    """
    response = render(request, template_name)
    response.status_code = 500
    return response


def rtl_dashboard(request):
    """RTL Dashboard page.
    """
    return render(request, "greevil/sb_admin_rtl_dashboard.html",
                  {"nav_active": "rtl_dashboard"})


def add(request):
    """.
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


def add_expense_view(request):
    """.
    Adding expenses
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
    return render(request, "greevil/sb_admin_add_exp.html",
                  context)
