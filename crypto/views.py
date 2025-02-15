from django.shortcuts import render
from .utils import fetch_all_prices , query_ollama
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render
import requests
from django.http import JsonResponse

def landing_page(request):
    return render(request, 'landing_page.html')




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html')



@login_required
def home_view(request):
   

    binance_prices, kucoin_prices, bybit_prices = fetch_all_prices()
    combined_prices = []

    all_symbols = set(binance_prices.keys()).union(kucoin_prices.keys()).union(bybit_prices.keys())
    for symbol in all_symbols:
        combined_prices.append({
            "symbol": symbol,
            "binance": binance_prices.get(symbol, "N/A"),
            "kucoin": kucoin_prices.get(symbol, "N/A"),
            "bybit": bybit_prices.get(symbol, "N/A"),
        })

    return render(request, "home.html", {"prices": combined_prices})

@login_required
def best_arbitrage_view(request):
   
    binance_prices, kucoin_prices, bybit_prices = fetch_all_prices()
    all_prices = {
        "Binance": binance_prices,
        "KuCoin": kucoin_prices,
        "Bybit": bybit_prices
    }

    best_opportunity = None

    
    all_symbols = set(binance_prices.keys()) | set(kucoin_prices.keys()) | set(bybit_prices.keys())

    for symbol in all_symbols:
       
        prices = {
            exchange: price[symbol]
            for exchange, price in all_prices.items()
            if symbol in price
        }

       
        if len(prices) >= 2:
            min_exchange = min(prices, key=prices.get)  
            max_exchange = max(prices, key=prices.get)  
            profit = prices[max_exchange] - prices[min_exchange]

           
            if best_opportunity is None or profit > best_opportunity['profit']:
                best_opportunity = {
                    "symbol": symbol,
                    "buy_from": min_exchange,
                    "sell_to": max_exchange,
                    "profit": profit
                }

    return render(request, "best_arbitrage.html", {"opportunity": best_opportunity})

GEMINI_API_KEY = "AIzaSyCzb9sVfdGa88E_Yau9Etp5r3TDNzcbVTw" 
def get_gemini_response(user_input):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyCzb9sVfdGa88E_Yau9Etp5r3TDNzcbVTw"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    data = {
        "query": user_input,
        "context": """
        Ин ассистенти ширкати шумо мебошад.Ширкати ман номаш АРБИТРАЖ ТҶК  ки барои мардуммекунад ки ба осони барои арбитраж кардан имкониятҳо беҳтаринро пайдо намоянд  Танҳо ба саволҳо дар бораи ширкат ҷавоб диҳед. 
        Агар савол ба ширкат алоқаманд набошад, ҷавоб диҳед: "Ман танҳо ба саволҳои марбут ба ширкат ҷавоб медиҳам."

        Маълумоти ширкат:
        - Ном: Ширкати Sample
        - Соли таъсис: 2020
        - Хизматрасониҳо: Рушди веб, машваратҳои IT, ва дастгирии техникӣ
        - Суроға: Душанбе, Тоҷикистон
        - Тамос: +79632626283
        - Почтаи электронӣ: info@sample.com


        """,
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json().get("response", "Мутаассифона, ҷавоб пайдо нашуд.")
        else:
            return f"Хатогӣ дар API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Хатогии пайвастшавӣ: {e}"

'''def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get('message', '')
        bot_response = get_gemini_response(user_message)
        return JsonResponse({'response': bot_response})
    return render(request, 'chat.html')'''



conversation_history = ""

def chat_view(request):
    global conversation_history
    user_input = request.POST.get("user_input", "")
    ai_response = ""

    if user_input:
        ai_response = query_ollama(user_input, conversation_history)
        conversation_history += f"User: {user_input}\nAI: {ai_response}\n"

    return render(request, "chat.html", {
        "conversation_history": conversation_history.split("\n"),
        "user_input": user_input,
        "ai_response": ai_response,
    })
