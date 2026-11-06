from datetime import date

from django.test import TestCase
from django.urls import reverse

from main.models import Education, Experience


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=date(2025, 1, 1),
        )
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            description="Information Systems",
            degree="S1",
            started_at=date(2025, 8, 25),
        )
        self.experience_list_url = reverse("api:experience-list")
        self.experience_detail_url = reverse(
            "api:experience-detail", args=[self.experience.id],
        )
        self.education_list_url = reverse("api:education-list")
        self.education_detail_url = reverse(
            "api:education-detail", args=[self.education.id],
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_education")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, self.experience_list_url)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertNotContains(response, self.experience.title)

    def test_experience_data_comes_from_api(self):
        response = self.client.get(self.experience_list_url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], self.experience.title)
        self.assertEqual(data[0]["description"], self.experience.description)
        self.assertEqual(data[0]["category"], "part-time")
        self.assertIsNone(data[0]["ended_at"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(self.experience_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        page = self.client.get(reverse("main:show_experience"))
        self.assertContains(page, "No experiences have been added or found.")

    def test_completed_experience(self):
        self.assertIsNone(self.client.get(self.experience_detail_url).json()["ended_at"])

        self.experience.ended_at = date(2025, 8, 25)
        self.experience.save()
        self.experience.refresh_from_db()

        self.assertFalse(self.experience.is_ongoing)
        response = self.client.get(self.experience_detail_url)
        self.assertEqual(response.json()["ended_at"], "2025-08-25")

    def test_education_model(self):
        self.assertEqual(str(self.education), "Universitas Indonesia")
        self.assertEqual(self.education.degree, "S1")
        self.assertTrue(self.education.is_ongoing)

    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, 'id="education-search-form"')
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, self.education_list_url)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertNotContains(response, self.education.description)
        
    def test_education_data_comes_from_api(self):
        response = self.client.get(self.education_list_url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["institution"], self.education.institution)
        self.assertEqual(data[0]["description"], self.education.description)
        self.assertEqual(data[0]["degree"], "S1")
        self.assertIsNone(data[0]["ended_at"])

    def test_empty_education_page(self):
        Education.objects.all().delete()

        response = self.client.get(self.education_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        page = self.client.get(reverse("main:show_education"))
        self.assertContains(page, "No education records have been added or found.")

    def test_completed_education(self):
        self.assertIsNone(self.client.get(self.education_detail_url).json()["ended_at"])

        self.education.ended_at = date(2025, 8, 25)
        self.education.save()
        self.education.refresh_from_db()

        self.assertFalse(self.education.is_ongoing)
        response = self.client.get(self.education_detail_url)
        self.assertEqual(response.json()["ended_at"], "2025-08-25")