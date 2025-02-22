from django import forms
from .models import HealthGoal, Food

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name", "carbs", "proteins", "fats", "calorie"]


class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = ['daily_calorie_goal', 'carb_goal', 'protein_goal', 'fat_goal']

