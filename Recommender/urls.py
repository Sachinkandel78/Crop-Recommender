from django.urls import path
from .views import * #Yo line le views.py file ma define gareko sabai functions lai import garne ho, jasle garda hamile home ra signup_view functions lai url patterns ma use garna sakchau.

urlpatterns = [
    path('',home, name='home'),   #Yo khali huda home page ma janey url ho. Yo home function lai call garne ho, jun views.py ma define gareko cha.
    path('signup/',signup_view, name='signup'),  #Yo signup page ma janey url ho. Yo signup_view function lai call garne ho, jun views.py ma define gareko cha.
    path('predict/',predict_view, name='predict'),
    #Yesko matlab jaba eg; www.cropreccommender/predict vanni khulxa taba yesley predict_view function call garxa ani tes vitrako function execute garxa.def predict(request): return render(request, "predict.html")
    path('logout/',logout_view, name='logout'),
    path('login/',login_view, name='login'),
    path('user_history/',user_history_view, name='user_history'),
    path('history_delete/<int:id>/',user_delete_prediction, name='user_delete_prediction'),
    
]
