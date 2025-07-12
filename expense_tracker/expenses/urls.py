from django.urls import path
from . import views 
urlpatterns = [
    path('',views.expense_list,name='index'),  
    path('addExpense/',views.addExpense,name='addExpense'),  
    path('<int:expenseId>/removeExpense/',views.removeExpense,name='removeExpense'),  
    path('<int:expenseId>/editExpense/',views.editExpense,name='editExpense'),  
    path('downloadfile/',views.download_expenses,name='download'),  
    path('category/<str:category>/',views.analyze_category,name='categoryChart'),  
    path('register/',views.registerUser,name='register'),  
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    
]