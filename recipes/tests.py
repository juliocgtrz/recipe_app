from django.test import TestCase, Client
from .models import Recipe
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RecipesSearchForm, AddRecipeForm
from django.contrib.messages import get_messages

# Create your tests here.
class RecipeModelTest(TestCase):
    # set up non-modified objects used by all test methods
    def setUpTestData():
        Recipe.objects.create(
            name = "Tea",
            ingredients = "Tea leaves, Sugar, Water",
            cooking_time = 5,
        )

    # NAME
    def test_recipe_name(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for 'name' field and use it to query its data
        field_label = recipe._meta.get_field("name").verbose_name

        # compare the value to the expected result
        self.assertEqual(field_label, "name")

    def test_recipe_name_max_length(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for 'name' field and use it to query its data
        max_length = recipe._meta.get_field("name").max_length

        # compare the value to the expected result
        self.assertEqual(max_length, 50)

    # INGREDIENTS
    def test_ingredients_max_length(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for 'ingredients' field and use it to query its data
        max_length = recipe._meta.get_field("ingredients").max_length

        # compare the value to the expected result
        self.assertEqual(max_length, 225)

    # COOKING TIME
    def test_cooking_time_value(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # get metadata for 'cooking_time' field and use it to query its data
        cooking_time_value = recipe.cooking_time

        # compare the value to the expected result
        self.assertIsInstance(cooking_time_value, int)

    # DIFFICULTY
    def test_difficulty_calculation(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # compare the value to the expected result
        self.assertEqual(recipe.difficulty(), "Easy")

    # URL
    def test_get_absolute_url(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # compare the value to the expected result
        self.assertEqual(recipe.get_absolute_url(), "/list/1")

# SEARCH
class RecipeFormTest(TestCase):
    def test_search_form_valid_data(self):
        #create a RecipesSearchForm instance with valid data
        form = RecipesSearchForm(data={
            "search_by": "name",
            "search_term": "Test Recipe",
            "cooking_time": "",
            "difficulty": "",
        })

        #check if form is valid
        self.assertTrue(form.is_valid())

    def test_search_form_invalid_data(self):
        #create a RecipesSearchForm instance with empty data
        form = RecipesSearchForm(data={})

        #check if form is invalid
        self.assertFalse(form.is_valid())

    def test_search_form_field_labels(self):
        #create a RecipesSearchForm instance
        form = RecipesSearchForm()

        #check if "search_by" field label is "Search by"
        self.assertEqual(form.fields["search_by"].label, "Search by")

        #check if "search_term" field label is "Search term"
        self.assertEqual(form.fields["search_term"].label, "Search term")

        #check if "cooking_time" field label is "Cooking Time (minutes)"
        self.assertEqual(form.fields["cooking_time"].label, "Cooking Time in Minutes")

        #check if "difficulty" field label is "Difficulty"
        self.assertEqual(form.fields["difficulty"].label, "Difficulty")


class RecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #create test user
        cls.user = User.objects.create_user(username="testuser", password="12345")

        #create test recipes
        cls.recipe1 = Recipe.objects.create(name="Recipe 1", ingredients="ingredient1, ingredient2", cooking_time=10)
        cls.recipe2 = Recipe.objects.create(name="Recipe 2", ingredients="ingredient1, ingredient2", cooking_time=20)

    def setUp(self):
        #initialize test client
        self.client = Client()

    def test_recipe_list_view_login_required(self):
        #send GET request to recipe list view
        response = self.client.get(reverse("recipes:list"))

        #check if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:list')}")

    def test_recipe_list_view(self):
        #log test user in
        self.client.login(username="testuser", password="12345")

        #send GET request to recipe list view
        response = self.client.get(reverse("recipes:list"))

        #check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        #check if correct template is used
        self.assertTemplateUsed(response, "recipes/list.html")

        #check if response contains the first recipe name
        self.assertContains(response, "Recipe 1")

        #check if response contains the second recipe name
        self.assertContains(response, "Recipe 2")

    def test_recipe_detail_view_login_required(self):
        #send GET request to recipe detail view for the first recipe
        response = self.client.get(reverse("recipes:detail", kwargs={"pk": self.recipe1.pk}))

        #check if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:detail', kwargs={'pk': self.recipe1.pk})}")

    def test_recipe_detail_view(self):
        #log test user in
        self.client.login(username="testuser", password="12345")

        #sends GET request to recipe detail view for the first recipe
        response = self.client.get(reverse("recipes:detail", kwargs={"pk": self.recipe1.pk}))

        #check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        #check if correct template is used
        self.assertTemplateUsed(response, "recipes/detail.html")

        #check if response contains the first recipe name
        self.assertContains(response, "Recipe 1")

    def test_search_view_login_required(self):
        #send GET request to search view
        response = self.client.get(reverse("recipes:search"))

        #check if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:search')}")

    def test_search_view(self):
        #log test user in
        self.client.login(username="testuser", password="12345")

        #send POST request to search view with valid data
        response = self.client.post(reverse("recipes:search"), data={
            "search_by": "name",
            "search_term": "Recipe 1",
            "cooking_time": "",
            "difficulty": "",
        })

        #check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        #check if correct template is used
        self.assertTemplateUsed(response, "recipes/search.html")

        #check if response contains the first recipe name
        self.assertContains(response, "Recipe 1")

class RecipeFormTest(TestCase):
    #test form validation with valid data
    def test_add_recipe_form_valid_data(self):
        form = AddRecipeForm(data={
            "name": "Test Recipe",
            "ingredients": "Test Ingredients",
            "cooking_time": 30,
            "pic": None     #assuming no file for simplicity
        })

        #form should be valid
        self.assertTrue(form.is_valid())  

    #test form validation with no data
    def test_add_recipe_form_no_data(self):
        form = AddRecipeForm(data={})

        #form should be invalid
        self.assertFalse(form.is_valid())

        #should have errors for all required fields
        self.assertEqual(len(form.errors), 3)


class AddRecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #create a test user
        cls.user = User.objects.create_user(username="testuser", password="12345")

    def setUp(self):
        #create a test client and log in the user
        self.client = Client()
        self.client.login(username="testuser", password="12345")

    #test GET request to add_recipe view
    def test_add_recipe_view_get(self):
        response = self.client.get(reverse("recipes:add_recipe"))
        
        #status code should be 200
        self.assertEqual(response.status_code, 200)

        #should use the correct template
        self.assertTemplateUsed(response, "recipes/add_recipe.html")

        #context should have AddRecipeForm
        self.assertIsInstance(response.context["add_recipe_form"], AddRecipeForm)

    #test POST request with valid data to add_recipe view
    def test_add_recipe_view_post_valid_data(self):
        data = {
            "name": "Test Recipe",
            "ingredients": "Test Ingredients",
            "cooking_time": 30,
            "pic": ""  #assuming no file for simplicity
        }

        response = self.client.post(reverse("recipes:add_recipe"), data)

        #should redirect after successful form submission
        self.assertEqual(response.status_code, 302)
        
        #should redirect to the recipe list view
        self.assertRedirects(response, reverse("recipes:list"))
        
        #one recipe should be created
        self.assertEqual(Recipe.objects.count(), 1)

        #check for success message
        messages = list(get_messages(response.wsgi_request))

        #there should be one message
        self.assertEqual(len(messages), 1)

        #message content should be correct
        self.assertEqual(str(messages[0]), "Recipe added successfully")

    #test POST request with invalid data to add_recipe view
    def test_add_recipe_view_post_invalid_data(self):
        data = {}

        response = self.client.post(reverse("recipes:add_recipe"), data)

        #should return 200 status code
        self.assertEqual(response.status_code, 200)

        #should use the correct template
        self.assertTemplateUsed(response, "recipes/add_recipe.html")

        #form should be invalid
        self.assertFalse(response.context["add_recipe_form"].is_valid())  

    #test that add_recipe view requires login
    def test_add_recipe_view_login_required(self):
        #log out the test user
        self.client.logout()

        response = self.client.get(reverse("recipes:add_recipe"))

        #should redirect to login page with next parameter set to add_recipe URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:add_recipe')}")