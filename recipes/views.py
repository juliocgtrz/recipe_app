from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView   #to display lists and details
from .models import Recipe   #to access Recipe model
from django.contrib.auth.mixins import LoginRequiredMixin   #to protect class-based view
from django.contrib.auth.decorators import login_required   #to protect function-based views
from .forms import RecipesSearchForm, AddRecipeForm
import pandas as pd
from .utils import get_chart
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'recipes/home.html')

def about(request):
    return render(request, "recipes/about.html")
    
class RecipeListView(LoginRequiredMixin, ListView):             #class-based "protected" view
    model = Recipe                                              #specify model
    template_name = 'recipes/list.html'                         #specify template

class RecipeDetailView(LoginRequiredMixin, DetailView):         #class-based "protected" view
    model = Recipe                                              #specify model
    template_name = 'recipes/detail.html'                       #specify template

@login_required                                                 #function-based "protected" view
def search(request):
    #create an instance of RecipesSearchForm defined in recipes/forms.py
    form = RecipesSearchForm(request.POST or None)

    #initialize dataframe to None
    recipes_df = None

    bar_chart = None
    pie_chart = None
    line_chart = None

    if request.method == "POST" and form.is_valid():
        #retrieves the search criteria from the form
        search_by = form.cleaned_data.get("search_by")
        search_term = form.cleaned_data.get("search_term")
        cooking_time = form.cleaned_data.get("cooking_time")
        difficulty = form.cleaned_data.get("difficulty")

        #filters the queryset based on the form input
        qs = Recipe.objects.all()

        if search_by == "name" and search_term:
            qs = qs.filter(name__icontains=search_term)
        elif search_by == "cooking_time" and cooking_time is not None:
            qs = qs.filter(cooking_time=cooking_time)
        elif search_by == "difficulty" and difficulty:
            qs = [recipe for recipe in qs if recipe.difficulty == difficulty]

        #checks if the queryset is not empty
        if qs:
            #converts list to pandas dataframe, else converts queryset to pandas DataFrame
            if isinstance(qs, list):
                recipes_df = pd.DataFrame([recipe.__dict__ for recipe in qs])
            else:
                recipes_df = pd.DataFrame(qs.values())

            recipes_df.index += 1

            #retrieves each Recipe object using its id, then calls get_absolute_url() on it to generate the link
            def format_recipe_name_table(row):
                recipe = Recipe.objects.get(id=row["id"])
                return f"<a href='{recipe.get_absolute_url()}'>{row['name']}</a>"
            
            def format_recipe_name_chart(row):
                return row["name"]

            recipes_df["name_table"] = recipes_df.apply(format_recipe_name_table, axis=1)
            recipes_df["name_chart"] = recipes_df.apply(format_recipe_name_chart, axis=1)

            #calculates difficulty and number of ingredients for each recipe
            recipes_df["difficulty"] = [recipe.difficulty for recipe in qs]
            recipes_df["number_of_ingredients"] = recipes_df["ingredients"].apply(lambda x: len(x.split(", ")))

            #generate charts
            bar_chart = get_chart("#1", recipes_df, labels=recipes_df["name_chart"].values)
            pie_chart = get_chart("#2", recipes_df, labels=recipes_df["difficulty"].values)
            line_chart = get_chart("#3", recipes_df, labels=recipes_df["name_chart"].values)

            recipes_df = recipes_df[["name_table", "cooking_time", "difficulty"]]
            recipes_df = recipes_df.rename(columns={"name_table": "Name"})
            recipes_df = recipes_df.rename(columns={"cooking_time": "Cooking Time in Minutes"})
            recipes_df.columns = recipes_df.columns.str.capitalize()

            #convert DataFrame to HTML for display
            recipes_df = recipes_df.to_html(escape=False)


    #pack up data to be sent to template in the context dictionary
    context = {
        "form": form,
        "recipes_df": recipes_df,
        "bar_chart": bar_chart,
        "pie_chart": pie_chart,
        "line_chart": line_chart,
    }

    #loads page using "context" information
    return render(request, "recipes/search.html", context)

@login_required                                             #function-based "protected" view
def add_recipe(request):

    if request.method == "POST":
        #create an instance of AddRecipeForm with the submitted data and files
        add_recipe_form = AddRecipeForm(request.POST, request.FILES)

        #validate form data
        if add_recipe_form.is_valid():
            #save form data to database
            add_recipe_form.save()

            #add a success message to display to user
            messages.success(request, "Recipe added successfully")

            #redirect user to add_recipe page
            return redirect("recipes:list")
    else:
        #create an empty form instance if request method is not POST
        add_recipe_form = AddRecipeForm()

    #prepare data to send from view to template
    context = {
        "add_recipe_form": add_recipe_form
    }

    #load page using context information
    return render(request, "recipes/add_recipe.html", context)