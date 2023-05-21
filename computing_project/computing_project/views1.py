import datetime as dt 
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate,logout 
from django.shortcuts import redirect, render
from django.contrib import messages
from cassandra.cluster import Cluster
from django.views import View
from django.http import JsonResponse
import pytz
from .models import Alert


 ###      Login In       ####
def my_view(request):
    if request.method == "POST":
        login_id = request.POST.get('login_id')
        password = request.POST.get('password')
        print(login_id,password)
        print(request.POST)

        # Check if login_id is None or an empty string
        if login_id is None or login_id == '':
            messages.error(request, 'Invalid login_id')
            return render(request, 'index.html')

        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect('test')

        query = "SELECT * FROM test.access WHERE login = %s AND password = %s ALLOW FILTERING"
        result = session.execute(query, [login_id, password])
        print(login_id,password)
        #request.session['login_id'] = log_in


        if result.one() is not None:
            # Connect or perform any additional actions here
            return redirect('/dashboard')

    return render(request, 'index.html')


###     Page de Garde     ###
def homepage_render(request):
    if request.method == "POST":
        return my_view(request)
    else:
        return render(request, 'index.html')
   
### Dashboard view ###
def dashboard_render(request):
    page = render(request, 'dashboard.html')
    return page   

### Log Out view ####  de
def logout_view(request):
    logout(request)
    return redirect('/index')
    # Redirect to a success page
    
 

####   Graphique et Caclul Total de Production ####

def test_view(request):
    if request.method == 'POST':
        home_id = request.POST.get('home_id')  # Récupérer la valeur de home_id soumise par l'utilisateur
        selected_date = request.POST.get('selected_date')  # Récupérer la valeur de selected_date soumise par l'utilisateur

        if home_id is not None and home_id != '' and selected_date is not None and selected_date != '':
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect('test')

            rows1 = session.execute("SELECT day,ts,p_cons FROM test.power WHERE home_id = %s AND day = %s",
                                    [home_id, selected_date])
            #print(rows1)  # Remplacez par le nom de votre table
            rows2 = session.execute("SELECT day,ts, p_prod FROM test.power WHERE home_id = %s AND day = %s",
                                    [home_id, selected_date])
            rows3 = session.execute("SELECT day,ts,p_tot FROM test.power WHERE home_id = %s AND day = %s",
                                    [home_id, selected_date])
            
            
            # Mettez les données dans le format requis pour le graphique
            tz = pytz.timezone('Europe/Brussels')
            data1 = [{'label': row.ts.replace(tzinfo = dt.timezone.utc).astimezone(tz).strftime('%d/%m/%Y %H:%M:%S'), 'value': row.p_cons} for row in rows1]
            data2 = [{'label': row.ts.replace(tzinfo = dt.timezone.utc).astimezone(tz).strftime('%d/%m/%Y %H:%M:%S'), 'value': row.p_prod} for row in rows2]
            data3 = [{'label': row.ts.replace(tzinfo = dt.timezone.utc).astimezone(tz).strftime('%d/%m/%Y %H:%M:%S'), 'value': row.p_tot}  for row in rows3] #Faire du * -1

            transformed_data1 = [{'label': item['label'], 'value': abs(item['value'])} for item in data1]
            transformed_data2 = [{'label': item['label'], 'value': abs(item['value'])} for item in data2]
            transformed_data3 = [{'label': item['label'], 'value': abs(item['value'])} for item in data3]

            context = {
                'data1': transformed_data1,
                'data2': transformed_data2,
                'data3': transformed_data3,
                }
            
            # Calcul de la différence d'énergie
            energy_consumed_db = float(request.POST.get('p_cons', 0.0))  # Remplacez 0.0 par une valeur par défaut appropriée
            energy_produced_db = float(request.POST.get('p_prod', 0.0))
            query = "SELECT p_prod, p_cons FROM test.power WHERE home_id = %s"
            result = session.execute(query, [home_id])

            row = result.one()
            if row:
                energy_produced_db = row.p_prod
                energy_consumed_db = row.p_cons
                difference = round(energy_consumed_db - energy_produced_db)
            else:
                difference = None

            context['difference'] = difference

            return render(request, 'dashboard.html', context)
    
    return render(request, 'dashboard.html')



###    SYSTEM D'ALTERTE    #####

class AlertView(View):
    def get(self, request, login):
        # Retrieve alerts based on the login
        alerts = Alert.objects.filter(login=login).values('message', 'created_at')

        # Convert alerts to a list
        alerts_list = list(alerts)

        # Return the alerts as JSON response
        return JsonResponse({'alerts': alerts_list}, safe=False)   
    




###      SUPPERPOSITION DES GRAPHIQUES     ####
def graph_view(request):
    if request.method == 'POST':
        home_id1 = request.POST.get('home_id1')  # Récupérer la valeur de home_id pour le premier graphique
        home_id2 = request.POST.get('home_id2')  # Récupérer la valeur de home_id pour le deuxième graphique
        selected_date = request.POST.get('selected_date')  # Récupérer la valeur de selected_date soumise par l'utilisateur
        selected_data = request.POST.get('data_type')  # Récupérer la valeur de selected_data (p_cons ou p_prod)

        if home_id1 is not None and home_id1 != '' and home_id2 is not None and home_id2 != '' and selected_date is not None and selected_date != '':
            cluster = Cluster(['127.0.0.1'])
            session = cluster.connect('test')

            # Récupérer les données pour le premier graphique (home_id1)
            rows1 = session.execute(
                "SELECT day,ts, p_prod, p_cons,p_tot FROM test.power WHERE home_id = %s AND day = %s", [home_id1, selected_date])

            # Récupérer les données pour le deuxième graphique (home_id2)
            rows2 = session.execute(
                "SELECT day,ts, p_prod, p_cons ,p_tot FROM test.power WHERE home_id = %s AND day = %s", [home_id2, selected_date])
           

            # Mettez les données dans le format requis pour les graphiques
            tz = pytz.timezone('Europe/Brussels')
            data1 = [{'label': row.ts.replace(tzinfo = dt.timezone.utc).astimezone(tz).strftime('%d/%m/%Y %H:%M:%S'), 'value': getattr(row, selected_data)} for row in rows1]
            data2 = [{'label': row.ts.replace(tzinfo = dt.timezone.utc).astimezone(tz).strftime('%d/%m/%Y %H:%M:%S'), 'value': getattr(row, selected_data)} for row in rows2]
            # Créer le dictionnaire requis pour le template
            transformed_data1 = [{'label': item['label'], 'value': abs(item['value'])} for item in data1]
            transformed_data2 = [{'label': item['label'], 'value': abs(item['value'])} for item in data2]
    
            #current_datetime = dt.now()
            #alerts = Alert.objects.filter(date=current_datetime.date(), time=current_datetime.time())


            context = {
                'data1': transformed_data1,
                'data2': transformed_data2,
                #'alerts': alerts 
                }
            context = {'data1': data1, 'data2': data2,}
            return render(request, 'graph.html', context)

    return render(request, 'graph.html')
 




 