import datetime
import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Experience, Project

PASSWORD = "test-password"

class PortfolioAPITestMixin:
    model = None
    url_prefix = None  
    text_field = None 
    search_param = None  
    search_hit = None  
    expected_fields = set()
    required_fields = ()
    invalid_create_cases = []  
    invalid_patch_cases = []  

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password=PASSWORD, email="owner@example.com",
        )
        self.editor = User.objects.create_user(username="editor", password=PASSWORD)
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.visitor = User.objects.create_user(username="visitor", password=PASSWORD)

        self.item = self.make_item()
        self.original_text = getattr(self.item, self.text_field)
        self.original_description = self.item.description
        self.list_url = reverse(f"api:{self.url_prefix}-list")
        self.detail_url = reverse(f"api:{self.url_prefix}-detail", args=[self.item.id])
        self.star_url = reverse(f"api:{self.url_prefix}-star", args=[self.item.id])

    def make_item(self):
        raise NotImplementedError

    def payload(self, **changes):
        raise NotImplementedError

    def snapshot(self):
        """Current database row of self.item, to prove a rejected request changed nothing."""
        return self.model.objects.filter(pk=self.item.pk).values().get()

    def csrf_client(self, username):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username=username, password=PASSWORD))
        return client

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.item.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])

        detail = self.client.get(self.detail_url)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["id"], str(self.item.id))

    def test_response_exposes_only_declared_fields(self):
        self.item.starred_by.add(self.owner)
        response = self.client.get(self.detail_url)
        self.assertEqual(set(response.data), self.expected_fields)
        self.assertEqual(response.data["starred_by_names"], "owner")
        body = response.content.decode()
        self.assertNotIn("owner@example.com", body)
        self.assertNotIn("pbkdf2", body)

    def test_search_and_empty_results(self):
        found = self.client.get(self.list_url, {self.search_param: self.search_hit})
        self.assertEqual(len(found.data), 1)
        missing = self.client.get(self.list_url, {self.search_param: "not-found"})
        self.assertEqual(missing.status_code, status.HTTP_200_OK)
        self.assertEqual(missing.data, [])

    def test_missing_item_returns_404(self):
        url = reverse(f"api:{self.url_prefix}-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_regular_user_cannot_write(self):
        before = self.snapshot()
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            for response in (
                self.client.post(self.list_url, self.payload(), format="json"),
                self.client.put(self.detail_url, self.payload(), format="json"),
                self.client.patch(
                    self.detail_url, {self.text_field: "Changed"}, format="json",
                ),
                self.client.delete(self.detail_url),
            ):
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.snapshot(), before)

    def test_staff_without_editor_group_cannot_update(self):
        before = self.snapshot()
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(
            self.detail_url, {self.text_field: "Changed"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.snapshot(), before)

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.detail_url, {self.text_field: "Changed"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(getattr(self.item, self.text_field), "Changed")
        self.assertEqual(self.item.description, self.original_description)

        response = self.client.put(self.detail_url, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(
            getattr(self.item, self.text_field), self.payload()[self.text_field],
        )

    def test_editor_cannot_create_or_delete(self):
        before = self.snapshot()
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.list_url, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.snapshot(), before)

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.model.objects.filter(pk=response.data["id"]).exists())
        self.assertEqual(self.model.objects.count(), 2)

    def test_owner_can_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url, {self.text_field: "Changed"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(getattr(self.item, self.text_field), "Changed")
        self.assertEqual(self.item.description, self.original_description)

        response = self.client.put(
            self.detail_url, {self.text_field: "Incomplete"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.detail_url, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(self.model.objects.filter(pk=self.item.pk).exists())

    def test_wrong_method_on_list(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in self.invalid_create_cases:
            with self.subTest(changes=changes):
                response = self.client.post(
                    self.list_url, self.payload(**changes), format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
        self.assertEqual(self.model.objects.count(), 1)

    def test_required_fields_are_enforced(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for field in self.required_fields:
            self.assertIn(field, response.data)
        self.assertEqual(self.model.objects.count(), 1)

    def test_patch_validation(self):
        before = self.snapshot()
        self.client.force_authenticate(user=self.owner)
        for changes, field in self.invalid_patch_cases:
            with self.subTest(changes=changes):
                response = self.client.patch(self.detail_url, changes, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
        self.assertEqual(self.snapshot(), before)

    def test_tags_are_stripped_from_text(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url,
            self.payload(**{self.text_field: "<b>Clean</b> text"}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[self.text_field], "Clean text")
        created = self.model.objects.get(pk=response.data["id"])
        self.assertEqual(getattr(created, self.text_field), "Clean text")

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        response = self.client.post(
            self.list_url,
            {
                **self.payload(),
                "id": forged_id,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [self.visitor.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["id"], forged_id)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")
        created = self.model.objects.get(pk=response.data["id"])
        self.assertEqual(created.starred_by.count(), 0)

    def test_star_requires_login(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.item.starred_by.count(), 0)

    def test_star_toggles_for_every_logged_in_role(self):
        for user in (self.visitor, self.editor, self.owner):
            with self.subTest(user=user.username):
                self.client.force_authenticate(user=user)

                response = self.client.post(self.star_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data["is_starred"])
                self.assertEqual(response.data["star_count"], 1)
                self.assertTrue(self.item.starred_by.filter(pk=user.pk).exists())

                response = self.client.post(self.star_url)
                self.assertFalse(response.data["is_starred"])
                self.assertEqual(response.data["star_count"], 0)
                self.assertFalse(self.item.starred_by.filter(pk=user.pk).exists())

    def test_is_starred_is_computed_per_user(self):
        self.client.force_authenticate(user=self.visitor)
        self.client.post(self.star_url)

        self.client.force_authenticate(user=self.editor)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "visitor")

    def test_star_account_comes_from_request_user(self):
        self.client.force_authenticate(user=self.visitor)
        self.client.post(
            self.star_url, {"user": self.owner.id, "user_id": self.owner.id}, format="json",
        )
        usernames = list(self.item.starred_by.values_list("username", flat=True))
        self.assertEqual(usernames, ["visitor"])

    def test_star_missing_item_and_wrong_method(self):
        self.client.force_authenticate(user=self.visitor)
        missing = reverse(f"api:{self.url_prefix}-star", args=[uuid.uuid4()])
        self.assertEqual(self.client.post(missing).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_writes_without_csrf_are_rejected(self):
        before = self.snapshot()

        owner = self.csrf_client("owner")
        response = owner.post(self.list_url, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = owner.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        editor = self.csrf_client("editor")
        response = editor.patch(
            self.detail_url, {self.text_field: "Changed"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        visitor = self.csrf_client("visitor")
        response = visitor.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.item.starred_by.count(), 0)

    def test_session_write_with_csrf_token_succeeds(self):
        client = self.csrf_client("owner")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload(), format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.count(), 2)


class ProjectRolesAPITest(PortfolioAPITestMixin, APITestCase):
    model = Project
    url_prefix = "project"
    text_field = "title"
    search_param = "title"
    search_hit = "PORT"
    expected_fields = {
        "id", "title", "description", "tech_stack", "project_url",
        "project_image_url", "star_count", "is_starred", "starred_by_names",
    }
    required_fields = ("title", "description", "tech_stack")
    invalid_create_cases = [
        ({"title": "   "}, "title"),
        ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
        ({"project_url": "javascript:alert(1)"}, "project_url"),
    ]
    invalid_patch_cases = [
        ({"title": "   "}, "title"),
        ({"project_url": "javascript:alert(1)"}, "project_url"),
    ]

    def make_item(self):
        return Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )

    def payload(self, **changes):
        return {
            "title": "New project",
            "description": "A useful app",
            "tech_stack": "Python",
            "project_url": "https://example.com/",
            "project_image_url": "",
            **changes,
        }


class ExperienceAPITest(PortfolioAPITestMixin, APITestCase):
    model = Experience
    url_prefix = "experience"
    text_field = "title"
    search_param = "title"
    search_hit = "INTERN"
    expected_fields = {
        "id", "title", "description", "category", "thumbnail", "started_at",
        "ended_at", "star_count", "is_starred", "starred_by_names",
    }
    required_fields = ("title", "description", "started_at")
    invalid_create_cases = [
        ({"title": "   "}, "title"),
        ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
        ({"description": "<b></b>"}, "description"),
        ({"category": "not-a-category"}, "category"),
        ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
        ({"started_at": "01-06-2025"}, "started_at"),
        ({"started_at": "2025-06-01", "ended_at": "2025-01-01"}, "ended_at"),
    ]
    invalid_patch_cases = [
        ({"title": "<b></b>"}, "title"),
        ({"category": "not-a-category"}, "category"),
        ({"ended_at": "2023-01-01"}, "ended_at"),
    ]

    def make_item(self):
        return Experience.objects.create(
            title="Backend Intern",
            description="Built REST APIs",
            category="internship",
            started_at=datetime.date(2024, 1, 1),
        )

    def payload(self, **changes):
        return {
            "title": "Freelance Developer",
            "description": "Small client websites",
            "category": "freelance",
            "thumbnail": "",
            "started_at": "2025-01-01",
            "ended_at": None,
            **changes,
        }


class EducationAPITest(PortfolioAPITestMixin, APITestCase):
    model = Education
    url_prefix = "education"
    text_field = "institution"
    search_param = "institution"
    search_hit = "INDONESIA"
    expected_fields = {
        "id", "institution", "degree", "description", "started_at", "ended_at",
        "star_count", "is_starred", "starred_by_names",
    }
    required_fields = ("institution", "degree", "description", "started_at")
    invalid_create_cases = [
        ({"institution": "   "}, "institution"),
        ({"institution": "<b></b>"}, "institution"),
        ({"degree": "<b></b>"}, "degree"),
        ({"description": "<b></b>"}, "description"),
        ({"started_at": "01-06-2025"}, "started_at"),
        ({"started_at": "2025-06-01", "ended_at": "2025-01-01"}, "ended_at"),
    ]
    invalid_patch_cases = [
        ({"institution": "<b></b>"}, "institution"),
        ({"ended_at": "2020-01-01"}, "ended_at"),
    ]

    def make_item(self):
        return Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1",
            description="Computer Science",
            started_at=datetime.date(2023, 8, 1),
        )

    def payload(self, **changes):
        return {
            "institution": "Institut Teknologi Bandung",
            "degree": "S2",
            "description": "Software engineering",
            "started_at": "2025-08-01",
            "ended_at": None,
            **changes,
        }