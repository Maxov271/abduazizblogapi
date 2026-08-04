"""
Namunaviy ma'lumotlar bilan to'ldirish: python manage.py seed_demo
Faqat birinchi marta sozlash uchun qulay bo'lsin deb yozilgan — keyin
hammasini admin panelda (/admin/) tahrirlaysiz.
"""
from django.core.management.base import BaseCommand
from core.models import (
    Profile, SiteSettings, Service, SkillGroup, JourneyEntry, PortfolioCategory,
)


class Command(BaseCommand):
    help = "Boshlang'ich namunaviy ma'lumotlarni yuklaydi"

    def handle(self, *args, **options):
        SiteSettings.load()

        profile = Profile.load()
        if not profile.full_name or profile.full_name == "Islom Farkhodov":
            profile.about_intro = "Bu yerga o'zingiz haqingizda matn yozing (admin panel -> Profil)."
            profile.save()

        if not Service.objects.exists():
            Service.objects.bulk_create([
                Service(icon="brain", title="Xizmat nomi 1", description="Tavsif...", order=1),
                Service(icon="code", title="Xizmat nomi 2", description="Tavsif...", order=2),
            ])

        if not SkillGroup.objects.exists():
            SkillGroup.objects.bulk_create([
                SkillGroup(label="Frontend", items="React, Next.js, TailwindCSS", level_percent=85, order=1),
                SkillGroup(label="Backend", items="Django, PostgreSQL", level_percent=80, order=2),
            ])

        if not JourneyEntry.objects.exists():
            JourneyEntry.objects.create(title="Boshlanish", year="2020", description="...", order=1)

        if not PortfolioCategory.objects.exists():
            for i, name in enumerate(["Landing Pages", "Full Stack Apps", "Bots", "Designs"], start=1):
                PortfolioCategory.objects.create(name=name, order=i)

        self.stdout.write(self.style.SUCCESS("Namunaviy ma'lumotlar tayyor. Endi /admin/ orqali tahrirlang."))
