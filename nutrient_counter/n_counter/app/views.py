from django.shortcuts import render, redirect
from .models import Food, Consume, HealthGoal
from django.contrib.auth import logout
from django.http import JsonResponse
from .forms import HealthGoalForm, FoodForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/') 
def index(request):
    if request.method == "POST":
        if "food_consumed" in request.POST:
            food_consumed = request.POST['food_consumed']
            c = Food.objects.get(name=food_consumed)
            user = request.user
            Consume.objects.create(user=user, food_consumed=c)

        elif "daily_calorie_goal" in request.POST:
            user = request.user
            health_goal, created = HealthGoal.objects.get_or_create(user=user)
            form = HealthGoalForm(request.POST, instance=health_goal)
            if form.is_valid():
                form.save()

    foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)
    health_goal, _ = HealthGoal.objects.get_or_create(user=request.user)

    total_calories = sum(item.food_consumed.calorie for item in consumed_food)
    total_carbs = sum(item.food_consumed.carbs for item in consumed_food)
    total_proteins = sum(item.food_consumed.proteins for item in consumed_food)
    total_fats = sum(item.food_consumed.fats for item in consumed_food)

    form = HealthGoalForm(instance=health_goal)

    return render(request, 'app/index.html', {
        'foods': foods,
        'consumed_food': consumed_food,
        'health_goal': health_goal,
        'total_calories': total_calories,
        'total_carbs': total_carbs,
        'total_proteins': total_proteins,
        'total_fats': total_fats,
        'form': form
    })

@login_required
def update_goals(request):
    goal, created = HealthGoal.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = HealthGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = HealthGoalForm(instance=goal)
    return render(request, "app/update_goals.html", {"form": form})


def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == "POST":
        consumed_food.delete()
        return redirect('/')
    return render(request, 'app/delete.html')


def add_food(request):
    if request.method == "POST":
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the food to the global registry
            return redirect("index")  # Redirects back to the homepage
    else:
        form = FoodForm()
    return render(request, "app/add_food.html", {"form": form})


# def nutrient_data(request):
    # user = request.user

    # Получаем или создаем цели здоровья пользователя
    # health_goal, _ = HealthGoal.objects.get_or_create(user=user)

    # Считаем фактическое потребление
    # consumed_food = Consume.objects.filter(user=user)
    # labels = [item.food_consumed.name for item in consumed_food]
    # total_calories = sum(item.food_consumed.calorie for item in consumed_food)
    # total_carbs = sum(item.food_consumed.carbs for item in consumed_food)
    # total_proteins = sum(item.food_consumed.proteins for item in consumed_food)
    # total_fats = sum(item.food_consumed.fats for item in consumed_food)

    # consumed = Consume.objects.filter(user=request.user)
    # data = {
    #     "labels": [c.food_consumed.name for c in consumed],
    #     "carbs": [c.food_consumed.carbs for c in consumed],
    #     "proteins": [c.food_consumed.proteins for c in consumed],
    #     "fats": [c.food_consumed.fats for c in consumed],
    #     "calories": [c.food_consumed.calorie for c in consumed],

        # "actual": {
        #     "labels": labels,
        #     "calories": total_calories,
        #     "carbs": total_carbs,
        #     "proteins": total_proteins,
        #     "fats": total_fats,
        # },
        # "goal": {
        #     "calories": health_goal.daily_calorie_goal,
        #     "carbs": health_goal.carb_goal,
        #     "proteins": health_goal.protein_goal,
        #     "fats": health_goal.fat_goal,
        # }
    # }

    # return JsonResponse(data)

@login_required
def nutrient_data(request):
    consumed = Consume.objects.filter(user=request.user)
    goal, _ = HealthGoal.objects.get_or_create(user=request.user)

    data = {
        "labels": [c.food_consumed.name for c in consumed],
        "carbs": [c.food_consumed.carbs for c in consumed],
        "proteins": [c.food_consumed.proteins for c in consumed],
        "fats": [c.food_consumed.fats for c in consumed],
        "calories": [c.food_consumed.calorie for c in consumed],
        "goal_carbs": goal.carb_goal,
        "goal_proteins": goal.protein_goal,
        "goal_fats": goal.fat_goal,
        "goal_calories": goal.daily_calorie_goal,
    }
    return JsonResponse(data)



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "app/register.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect('/')