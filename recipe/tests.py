from functools import partial
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipebook.models import RecipeBook
from review.models import Review
from .models import Recipe
from . import views


RECIPE_FIELDS = ['title', 'description', 'ingredients', 'directions']


def create_recipe_and_user(username='lydia'):
    """Returns a new user and recipe authored by that user."""
    user = User(username=username)
    user.save()
    recipe = Recipe(
        user=user,
        title="test recipe",
        description="this is a test recipe",
        ingredients="food",
        directions="make it"
    )
    recipe.save()
    return user, recipe


class RecipeDetailTests(TestCase):
    """Test viewing a recipe."""

    def setUp(self):
        """Initialize a recipe to be tested."""
        self.user, self.recipe = create_recipe_and_user()
        url = reverse('view_recipe', args=[self.recipe.id])
        self.response = self.client.get(url)

    def test_shows_title(self):
        """Test response has title."""
        self.assertContains(self.response, self.recipe.title)

    def test_shows_description(self):
        """Test response has description."""
        self.assertContains(self.response, self.recipe.description)

    def test_shows_ingredients(self):
        """Test response has ingredients."""
        self.assertContains(self.response, self.recipe.ingredients)

    def test_shows_directions(self):
        """Test response has directions."""
        self.assertContains(self.response, self.recipe.directions)

    def test_shows_edit_link(self):
        """Test response has link to edit when logged in."""
        self.client.force_login(self.user)
        view_url = reverse('view_recipe', args=[self.recipe.id])
        response = self.client.get(view_url)
        edit_url = reverse('edit_recipe', args=[self.recipe.id])
        self.assertContains(response, edit_url)

    def test_shows_edit_only_authenticated(self):
        """Test response has link to edit only when logged in."""
        url = reverse('edit_recipe', args=[self.recipe.id])
        self.assertNotContains(self.response, url)

    def test_shows_delete(self):
        """Test response has link to delete when logged in."""
        self.client.force_login(self.user)
        view_url = reverse('view_recipe', args=[self.recipe.id])
        response = self.client.get(view_url)
        delete_url = reverse('delete_recipe', args=[self.recipe.id])
        self.assertContains(response, delete_url)

    def test_shows_delete_only_authenticated(self):
        """Test response has link to delete only when logged in."""
        url = reverse('delete_recipe', args=[self.recipe.id])
        self.assertNotContains(self.response, url)

    def test_has_recipe_book_form(self):
        """Test logged in GET has form for adding recipe to recipebooks."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('view_recipe', args=[self.recipe.id])
        )
        url = reverse('recipe_update_recipebooks', args=[self.recipe.id])
        self.assertContains(response, 'action="{}"'.format(url))

    def test_has_recipe_books(self):
        """Test logged in GET has form for adding recipe to recipebooks."""
        self.client.force_login(self.user)
        recipebook = RecipeBook(
            user=self.user,
            title='good recipes',
            description='recipe'
        )
        recipebook.save()
        response = self.client.get(
            reverse('view_recipe', args=[self.recipe.id])
        )
        self.assertContains(response, recipebook.title)

    def test_logged_out_has_no_recipe_book_form(self):
        """Test logged out GET has no form for adding to recipebooks."""
        response = self.client.get(
            reverse('view_recipe', args=[self.recipe.id])
        )
        url = reverse('recipe_update_recipebooks', args=[self.recipe.id])
        self.assertNotContains(response, 'action="{}"'.format(url))

    def test_user_only_has_own_recipe_books(self):
        recipebook = RecipeBook(
            user=self.user,
            title='good recipes',
            description='recipe'
        )
        recipebook.save()
        user = User(username='other')
        user.save()
        self.client.force_login(user)
        response = self.client.get(
            reverse('view_recipe', args=[self.recipe.id])
        )
        self.assertNotContains(response, recipebook.title)


class RecipeCreateTestCase(TestCase):
    """Test creating a recipe."""

    def setUp(self):
        user = User(username='lydia')
        user.save()
        self.client.force_login(user)
        self.data = dict(
            title='test recipe',
            description='this is a test recipe',
            ingredients='food',
            directions='make it'
        )
        self.get = self.client.get(reverse('new_recipe'))
        self.post = self.client.post(reverse('new_recipe'), self.data)

    def test_get_create_recipe(self):
        """Get the create recipe page."""
        self.assertEquals(self.get.status_code, 200)

    def test_get_create_recipe_has_form(self):
        """Test the create recipe page has a form."""
        self.assertContains(self.get, '</form>')

    def test_form_method_post(self):
        """Test the create recipe page has a form with method=POST."""
        self.assertContains(self.get, 'method="POST"')

    def test_form_has_inputs(self):
        """Test the create recipe page has a form with method=POST."""
        for name in RECIPE_FIELDS:
            self.assertContains(self.get, 'name="{}"'.format(name))

    def test_post_create_recipe_redirects(self):
        """Posts a recipe using the create view."""
        self.assertEquals(self.post.status_code, 302)

    def test_post_create_recipe(self):
        """Posts a recipe using the create view."""
        count = Recipe.objects.count()
        self.client.post(reverse('new_recipe'), self.data)
        self.assertEquals(Recipe.objects.count(), count + 1)

    def test_create_recipe_without_field_does_nothing(self):
        """Test POSTing a recipe without fields doesn't update DB."""
        count = Recipe.objects.count()
        for field in RECIPE_FIELDS:
            data = self.data.copy()
            del data[field]
            self.client.post(reverse('new_recipe'), data)
            self.assertEquals(Recipe.objects.count(), count)

    def test_post_unauthenticated(self):
        """Test POSTing a recipe while not logged in."""
        self.client.logout()
        count = Recipe.objects.count()
        self.client.post(reverse('new_recipe'), self.data)
        self.assertEquals(Recipe.objects.count(), count)


class ViewLogicTests(TestCase):
    """Test helper functions behind view."""

    def test_structure_directions(self):
        structured = list(views.structureDirections("""Season
        Mix cubed tofu with lime juice, turmeric, salt, and black pepper.

        Fry
        Combine tofu and chopped onions in frying pan.

        Simmer
        Bring tofu, onions, coconut milk, and curry paste to simmer.
        """))
        self.assertEquals(structured[0]['summary'], 'Season')
        self.assertEquals(structured[1]['summary'], 'Fry')
        self.assertEquals(
            structured[1]['details'],
            'Combine tofu and chopped onions in frying pan.'
        )
        self.assertEquals(structured[2]['summary'], 'Simmer')


class SearchViewTests(TestCase):
    """Test search functionality."""

    def setUp(self):
        """Insert some recipes into the db"""
        self.title = 'good recipe'
        self.user = User(username="friend")
        self.user.save()
        self.add_recipe(self.user, self.title)
        self.add_recipe(self.user, 'bad_recipe')
        self.response = self.get_response()

    def get_response(self, query='good'):
        url = reverse('recipe_search') + '?q={}'.format(query)
        return self.client.get(url)

    def add_recipe(self, user, title):
        """Insert a recipe with self.title into the database."""
        Recipe(
            user=user,
            title=title,
            description='test',
            ingredients='test',
            directions='test'
        ).save()

    def test_search_for_good_recipe(self):
        self.assertContains(self.response, self.title)

    def test_search_for_good_recipe_retains_search(self):
        """Test that search bar contains query."""
        self.assertContains(self.response, 'value="good"')

    def test_search_paginates(self):
        for i in range(50):
            self.add_recipe(self.user, self.title)
        self.assertContains(self.get_response(), self.title, 10)

    def test_search_short_words_returns_nothing(self):
        for c1, c2 in zip(self.title, self.title[1:]):
            self.assertNotContains(self.get_response(c1 + c2), self.title)

    def test_empty_search_returns_nothing(self):
        self.assertNotContains(self.get_response(''), self.title)

    def test_get_without_querystring(self):
        status_code = self.client.get(reverse('recipe_search')).status_code
        self.assertEqual(status_code, 200)


class EditViewTests(TestCase):
    """Test editing recipes."""

    def setUp(self):
        """Create recipe to be edited."""
        self.user, self.recipe = create_recipe_and_user()
        self.client.force_login(self.user)

    def edit_recipe_title(self, to):
        """Edit posted recipe's title using self.client."""
        data = dict(
            title=to,
            description='test',
            ingredients='test',
            directions='test'
        )
        url = reverse('edit_recipe', args=[self.recipe.id])
        self.client.post(url, data)

    def test_edit_title(self):
        """Test editing title."""
        new_title = 'new title'
        self.edit_recipe_title(new_title)
        recipe = Recipe.objects.filter(id=self.recipe.id).first()
        self.assertEqual(recipe.title, new_title)

    def test_editing_recipe_maintains_count(self):
        """Test editing title."""
        new_title = 'new title'
        count = Recipe.objects.count()
        self.edit_recipe_title(new_title)
        self.assertEqual(count, Recipe.objects.count())

    def test_wrong_user_cannot_edit(self):
        """Test that a user who does not own a recipe cannot edit it."""
        evil_user = User(username="evil")
        evil_user.save()
        self.client.force_login(evil_user)
        self.edit_recipe_title('bad')
        recipe = Recipe.objects.filter(id=self.recipe.id).first()
        self.assertEqual(recipe.title, self.recipe.title)


class DeleteViewTests(TestCase):
    """Test deleting recipes."""

    def setUp(self):
        """Create recipe to be deleted."""
        self.user, self.recipe = create_recipe_and_user()
        self.client.force_login(self.user)

    def test_delete_view_has_method_post(self):
        """Test delete view has method="POST"."""
        url = reverse('delete_recipe', args=[self.recipe.id])
        self.assertContains(self.client.get(url), 'method="POST"')

    def test_deleting_recipe_decrements_count(self):
        """Test deleting a recipe decrements the number of recipes."""
        count = Recipe.objects.count()
        url = reverse('delete_recipe', args=[self.recipe.id])
        self.client.post(url)
        self.assertEqual(count - 1, Recipe.objects.count())

    def test_wrong_user_cannot_delete(self):
        """Test that a user who does not own a recipe cannot delete it."""
        count = Recipe.objects.count()
        evil_user = User(username="evil")
        evil_user.save()
        self.client.force_login(evil_user)
        self.client.post(reverse('delete_recipe', args=[self.recipe.id]))
        self.assertEqual(count, Recipe.objects.count())

    def test_unauthorized_redirects(self):
        """Test an unauthorized user gets redirected to login."""
        self.client.logout()
        url = reverse('delete_recipe', args=[self.recipe.id])
        self.assertEqual(self.client.get(url).status_code, 302)


class AddRecipeBookTests(TestCase):
    """Test adding a recipe to recipebooks."""

    def setUp(self):
        """Create a recipe and two recipebooks."""
        self.user, self.recipe = create_recipe_and_user()
        self.client.force_login(self.user)
        self.rb1 = RecipeBook(
            title='one',
            description='one',
            user=self.user
        )
        self.rb2 = RecipeBook(
            title='two',
            description='two',
            user=self.user
        )
        self.rb1.save()
        self.rb2.save()
        self.url = reverse('recipe_update_recipebooks', args=[self.recipe.id])
        self.postData = partial(self.client.post, self.url)

    def test_add_recipe_to_book(self):
        """Test POSTing to recipe_add_recipebook."""
        self.assertEqual(self.recipe.recipebooks.count(), 0)
        self.postData(dict(books=[self.rb1.id, self.rb2.id]))
        self.assertEqual(self.recipe.recipebooks.count(), 2)

    def test_get_does_nothing(self):
        self.postData(dict(books=[self.rb1.id, self.rb2.id]))
        count = self.recipe.recipebooks.count()
        self.client.get(self.url)
        self.assertEqual(self.recipe.recipebooks.count(), count)

    def test_wrong_user_does_not_update(self):
        self.user, _ = create_recipe_and_user('bad')
        self.client.force_login(self.user)
        self.postData(dict(books=[self.rb1.id]))
        self.assertEqual(self.rb1.recipes.count(), 0)

    def test_logged_out_does_not_update(self):
        self.client.logout()
        self.postData(dict(books=[self.rb1.id]))
        self.assertEqual(self.rb1.recipes.count(), 0)

    def test_can_add_recipe_by_other_user(self):
        count = self.rb1.recipes.count()
        _, other_recipe = create_recipe_and_user('someone')
        self.rb1.recipes.add(other_recipe)
        self.assertEqual(self.rb1.recipes.count(), count + 1)


class DisplayReviewTests(TestCase):
    """Test displaying reviews on recipe page."""

    def view_recipe(self):
        url = reverse('view_recipe', args=[self.recipe.id])
        return self.client.get(url)

    def setUp(self):
        """Create a review to be displayed."""
        self.user, self.recipe = create_recipe_and_user()
        self.review = Review(
            user=self.user,
            recipe=self.recipe,
            title='review',
            body='this is a review',
            score=3
        )
        self.review.save()
        self.response = self.view_recipe()

    def test_review_fields_displayed(self):
        """Test review's fields are displayed on recipe response."""
        for field in ['recipe', 'title', 'body', 'score']:
            self.assertContains(self.response, getattr(self.review, field))

    def test_review_form_displayed(self):
        """Test review's has creation form"""
        self.client.force_login(self.user)
        url = reverse('new_review', args=[self.recipe.id])
        self.assertContains(self.view_recipe(), 'action="{}"'.format(url))

    def test_review_form_logged_out_not_displayed(self):
        """Test review's has creation form"""
        url = reverse('new_review', args=[self.recipe.id])
        self.assertNotContains(self.view_recipe(), 'action="{}"'.format(url))

    def test_review_by_user_has_delete_link(self):
        """Test link to delete review exists while logged in."""
        self.client.force_login(self.user)
        response = self.view_recipe()
        url = reverse('delete_review', args=[self.review.id])
        self.assertContains(response, 'href="{}"'.format(url))

    def test_review_logged_out_has_no_delete_link(self):
        """Test link to delete review does not exist while logged out."""
        url = reverse('delete_review', args=[self.review.id])
        self.assertNotContains(self.response, 'href="{}"'.format(url))

    def test_review_other_user_has_no_delete_link(self):
        """Test link to delete review does not exist while logged out."""
        user = User(username='someone')
        user.save()
        self.client.force_login(user)
        url = reverse('delete_review', args=[self.review.id])
        self.assertNotContains(self.response, 'href="{}"'.format(url))


class RecipeReviewsTests(TestCase):
    def setUp(self):
        self.user, self.recipe = create_recipe_and_user()
        self.reviews = [
            Review(
                user=self.user,
                recipe=self.recipe,
                title='this is a review',
                body='review body',
                score=5,
            ) for i in range(30)
        ]
        for review in self.reviews:
            review.save()
        url = reverse('recipe_reviews', args=[self.recipe.id])
        self.response = self.client.get(url)

    def test_has_titles(self):
        self.assertContains(self.response, self.reviews[0].title, 10)


class RecipeModalFormsTests(TestCase):
    def setUp(self):
        self.user, self.recipe = create_recipe_and_user()
        self.client.force_login(self.user)
        url = reverse('view_recipe', args=[self.recipe.id])
        self.response = self.client.get(url)

    def assert_has_form(self, url_name):
        url = reverse(url_name, args=[self.recipe.id])
        self.assertContains(self.response, 'action="{}"'.format(url))

    def test_recipe_view_has_edit_form(self):
        self.assert_has_form('edit_recipe')

    def test_recipe_view_has_delete_form(self):
        self.assert_has_form('delete_recipe')


class DerivedRecipeTests(TestCase):
    def setUp(self):
        self.user, self.origin_recipe = create_recipe_and_user()
        self.derived_recipe = Recipe(
            user=self.user,
            title="derived recipe",
            description="this recipe is derived from another",
            ingredients="food",
            directions="make it",
            origin_recipe=self.origin_recipe
        )
        self.derived_recipe.save()

    def test_derived_recipe_view_links_origin(self):
        origin_recipe_url = reverse(
            'view_recipe', args=[self.origin_recipe.id]
        )
        derived_recipe_url = reverse(
            'view_recipe', args=[self.derived_recipe.id]
        )
        response = self.client.get(derived_recipe_url)
        self.assertContains(response, origin_recipe_url)

    def test_derived_recipe_view_has_origin_title(self):
        derived_recipe_url = reverse(
            'view_recipe', args=[self.derived_recipe.id]
        )
        response = self.client.get(derived_recipe_url)
        self.assertContains(response, self.origin_recipe.title)

    def test_derive_recipe_form_in_recipe_view_logged_in(self):
        self.client.force_login(self.user)
        url = reverse('view_recipe', args=[self.origin_recipe.id])
        response = self.client.get(url)
        self.assertContains(response, 'name="origin_recipe"')
        value_attribute = 'value="{}"'.format(self.origin_recipe.id)
        self.assertContains(response, value_attribute)

    def test_derive_recipe_form_not_in_recipe_view_not_logged_in(self):
        url = reverse('view_recipe', args=[self.origin_recipe.id])
        response = self.client.get(url)
        self.assertNotContains(response, 'name="origin_recipe"')
        value_attribute = 'value="{}"'.format(self.origin_recipe.id)
        self.assertNotContains(response, value_attribute)

    def test_derive_recipe_view_has_form(self):
        self.client.force_login(self.user)
        url = reverse('derive_recipe', args=[self.origin_recipe.id])
        response = self.client.get(url)
        self.assertContains(response, 'name="origin_recipe"')
        value_attribute = 'value="{}"'.format(self.origin_recipe.id)
        self.assertContains(response, value_attribute)

    def test_derive_recipe_view_redirects_not_logged_in(self):
        url = reverse('derive_recipe', args=[self.origin_recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_post_derived_recipe(self):
        self.client.force_login(self.user)
        url = reverse('new_recipe')
        self.client.post(url, dict(
            title="derived recipe",
            description="this recipe is derived from another",
            ingredients="food",
            directions="make it",
            origin_recipe=self.origin_recipe.id
        ))
        posted_recipe = Recipe.objects.order_by('date_created').last()
        self.assertEqual(posted_recipe.origin_recipe, self.origin_recipe)

    def test_post_derived_wrong_recipe(self):
        self.client.force_login(self.user)
        url = reverse('new_recipe')
        self.client.post(url, dict(
            title="incorrectly derived recipe",
            description="this recipe is derived from another",
            ingredients="food",
            directions="make it",
            origin_recipe=0
        ))
        posted_recipe = Recipe.objects.order_by('date_created').last()
        self.assertEqual(posted_recipe.origin_recipe, None)


class DerivedRecipesViewTests(TestCase):
    def setUp(self):
        self.user, self.origin_recipe = create_recipe_and_user()
        for i in range(30):
            Recipe(
                user=self.user,
                title="derived recipe",
                description="this recipe is derived from another",
                ingredients="food",
                directions="make it",
                origin_recipe=self.origin_recipe
            ).save()
        url = reverse('derived_recipes', args=[self.origin_recipe.id])
        self.response = self.client.get(url)

    def test_get_derived_recipes_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_derived_recipes_view_has_recipes(self):
        self.assertContains(self.response, 'derived recipe', 10)

    def test_recipe_links_derivation_list(self):
        view_recipe_url = reverse('view_recipe', args=[self.origin_recipe.id])
        recipe_response = self.client.get(view_recipe_url)
        derived_url = reverse('derived_recipes', args=[self.origin_recipe.id])
        self.assertContains(recipe_response, 'href="{}"'.format(derived_url))
