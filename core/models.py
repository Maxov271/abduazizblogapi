from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class SiteSettings(models.Model):
    """Singleton: global site config — favicon, site icon, background, footer text."""
    site_name = models.CharField(max_length=100, default="Hanzo-Dev")
    favicon = models.ImageField(upload_to="site/", blank=True, null=True,
                                 help_text="Brauzer tab belgisi (.ico yoki .png, kvadrat)")
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    background_image = models.ImageField(upload_to="site/", blank=True, null=True,
                                          help_text="Fon rasmi (bo'sh qoldirilsa standart gradient ishlatiladi)")
    accent_color = models.CharField(max_length=7, default="#2f6bff",
                                     help_text="Asosiy rang (hex), masalan #2f6bff")
    telegram_bot_token = models.CharField(max_length=200, blank=True,
                                           help_text="Ixtiyoriy: .env o'rniga shu yerdan ham sozlash mumkin")
    telegram_chat_id = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Site sozlamalari"
        verbose_name_plural = "Site sozlamalari"

    def __str__(self):
        return "Site sozlamalari"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Profile(models.Model):
    """Singleton: left sidebar profile card + About Me intro."""
    full_name = models.CharField(max_length=150, default="Islom Farkhodov")
    display_name = models.CharField(max_length=100, default="Hanzo-Dev",
                                     help_text="Sidebar'da katta harflar bilan chiqadigan nom")
    title = models.CharField(max_length=100, default="Web Developer",
                              help_text="Ism ostidagi badge, masalan 'Web Developer'")
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, help_text="Masalan: Uzbekistan, Tashkent city")

    about_intro = models.TextField(blank=True, help_text="About Me bo'limidagi birinchi paragraflar")
    about_extra = models.TextField(blank=True, help_text="Qo'shimcha paragraf (ixtiyoriy)")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SocialLink(models.Model):
    """Icons row under the sidebar (Threads, Instagram, Telegram, GitHub, ...)."""
    PLATFORM_CHOICES = [
        ("threads", "Threads"), ("instagram", "Instagram"), ("telegram", "Telegram"),
        ("github", "GitHub"), ("linkedin", "LinkedIn"), ("facebook", "Facebook"),
        ("twitter", "X / Twitter"), ("youtube", "YouTube"), ("other", "Boshqa"),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Ijtimoiy tarmoq"
        verbose_name_plural = "Ijtimoiy tarmoqlar"

    def __str__(self):
        return self.get_platform_display()


class Service(models.Model):
    """'What I Do' cards on the About page."""
    ICON_CHOICES = [
        ("brain", "AI / Miya"), ("code", "Kod"), ("laptop-code", "Noutbuk"),
        ("palette", "Dizayn cho'tkasi"), ("rocket", "Raketa"), ("device-mobile", "Telefon"),
    ]
    icon = models.CharField(max_length=30, choices=ICON_CHOICES, default="code")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Xizmat (What I Do)"
        verbose_name_plural = "Xizmatlar (What I Do)"

    def __str__(self):
        return self.title


class InsideWorldCard(models.Model):
    """'Inside Hanzo's World' cards: philosophy / featured projects / playground."""
    CARD_TYPE = [("text", "Oddiy matn karta"), ("list", "Ro'yxat karta")]
    icon = models.CharField(max_length=30, blank=True, help_text="Masalan: layers, brain")
    title = models.CharField(max_length=100)
    card_type = models.CharField(max_length=10, choices=CARD_TYPE, default="text")
    body_text = models.TextField(blank=True, help_text="card_type=text bo'lsa shu ishlatiladi")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Inside World kartasi"
        verbose_name_plural = "Inside World kartalari"

    def __str__(self):
        return self.title


class InsideWorldItem(models.Model):
    """List rows for a list-type InsideWorldCard, e.g. 'Sonar AI — AI chat platform...'."""
    card = models.ForeignKey(InsideWorldCard, related_name="items", on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10, blank=True)
    bold_part = models.CharField(max_length=100, blank=True, help_text="Qalin qism, masalan 'Sonar AI'")
    rest_text = models.CharField(max_length=250, blank=True, help_text="Qolgan matn, masalan '— AI chat platform...'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Inside World qatori"
        verbose_name_plural = "Inside World qatorlari"

    def __str__(self):
        return self.bold_part or str(self.pk)


class SkillGroup(models.Model):
    """Resume page 'My Skills' rows: Frontend / Backend / Mobile / AI / Design."""
    label = models.CharField(max_length=50, help_text="Masalan: Frontend, Backend")
    items = models.CharField(max_length=300, help_text="Vergul bilan: React, Next.js, Vue, TailwindCSS, SASS")
    level_percent = models.PositiveIntegerField(default=80, help_text="Progress bar foizi (0-100)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Skill guruhi"
        verbose_name_plural = "Skill guruhlari (My Skills)"

    def __str__(self):
        return self.label


class JourneyEntry(models.Model):
    """Resume page 'My Journey' timeline items."""
    title = models.CharField(max_length=100, help_text="Masalan: The Spark")
    year = models.CharField(max_length=20, help_text="Masalan: 2019")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Journey yozuvi"
        verbose_name_plural = "My Journey"

    def __str__(self):
        return f"{self.year} — {self.title}"


class PortfolioCategory(models.Model):
    """Filter tabs on Portfolio page: Landing Pages, Full Stack Apps, Bots, Designs."""
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Portfolio kategoriyasi"
        verbose_name_plural = "Portfolio kategoriyalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    """A single portfolio project card."""
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(PortfolioCategory, related_name="projects", on_delete=models.PROTECT)
    cover_image = models.ImageField(upload_to="portfolio/")
    short_description = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Portfolio loyihasi"
        verbose_name_plural = "Portfolio loyihalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProjectGalleryImage(models.Model):
    project = models.ForeignKey(Project, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="portfolio/gallery/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Loyiha rasmi"
        verbose_name_plural = "Loyiha rasmlari"

    def __str__(self):
        return f"{self.project.title} #{self.pk}"


class Tag(models.Model):
    """Shared tags used both by Project and BlogPost, e.g. React, NestJS, AI."""
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


Project.add_to_class("tags", models.ManyToManyField(Tag, related_name="projects", blank=True))


class BlogPost(models.Model):
    """A 'Thread' post."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    excerpt = models.TextField(help_text="Karta ichida ko'rinadigan qisqa matn")
    body = models.TextField(help_text="To'liq post matni (HTML ruxsat etiladi)")
    read_minutes = models.PositiveIntegerField(default=5)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0, help_text="Tabiy (real) ko'rishlar soni — avtomatik oshadi")
    view_boost = models.PositiveIntegerField(default=0, help_text="Ko'rsatiladigan ko'rishlar sonini sun'iy oshirish uchun qo'shiladigan qiymat")

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Thread posti"
        verbose_name_plural = "Thread postlari"

    @property
    def display_views(self):
        return self.view_count + self.view_boost

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("thread_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Guest comments — no login required, name mandatory, hidden until approved by admin."""
    STATUS_CHOICES = [("pending", "Kutilmoqda"), ("approved", "Tasdiqlangan"), ("rejected", "Rad etilgan")]

    post = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE,
                              blank=True, null=True, help_text="Bo'sh bo'lsa — umumiy sayt izohi")
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"

    def __str__(self):
        target = self.post.title if self.post else "Umumiy"
        return f"{self.name} → {target} ({self.get_status_display()})"


class ContactMessage(models.Model):
    """'Let's Build Something' form submissions."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Kontakt xabari"
        verbose_name_plural = "Kontakt xabarlari"

    def __str__(self):
        return f"{self.name} <{self.email}>"


class TeamMember(models.Model):
    """'Mening Jamoam' (Team) page cards."""
    ICON_CHOICES = [
        ("code", "Kod </>"), ("server", "Server"), ("palette", "Dizayn cho'tkasi"),
        ("rocket", "Raketa"), ("brain", "AI / Miya"), ("layers", "Layers"), ("bolt", "Chaqmoq"),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="Masalan: Full Stack Developer")
    avatar = models.ImageField(upload_to="team/", blank=True, null=True)
    icon = models.CharField(max_length=30, choices=ICON_CHOICES, default="code")
    accent_color = models.CharField(max_length=7, default="#7c5cff",
                                     help_text="Karta ustidagi ikon foni (hex), masalan #7c5cff")
    skills = models.CharField(max_length=200, blank=True, help_text="Vergul bilan: Python, Django, Vue.js")
    description = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True, help_text="Shaxsiy portfolio yoki loyiha havolasi")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Jamoa a'zosi"
        verbose_name_plural = "Mening Jamoam"

    def __str__(self):
        return self.name


class StudentCategory(models.Model):
    """Filter tabs on Students page: Frontend, Backend, Python, Design, Office."""
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "O'quvchi kategoriyasi"
        verbose_name_plural = "O'quvchi kategoriyalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Student(models.Model):
    """'Mening O'quvchilarim' (Students) page cards."""
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="students/", blank=True, null=True)
    role = models.CharField(max_length=100, help_text="Masalan: Frontend Student")
    category = models.ForeignKey(StudentCategory, related_name="students", on_delete=models.PROTECT)
    skills = models.CharField(max_length=200, blank=True, help_text="Vergul bilan: HTML, CSS, JavaScript")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    project_count = models.PositiveIntegerField(default=0)
    portfolio_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "O'quvchi"
        verbose_name_plural = "Mening O'quvchilarim"

    def __str__(self):
        return self.name


class SiteStats(models.Model):
    """Singleton: sayt bo'yicha ochiq statistika (tashriflar, izohlar, so'rovlar soni)."""
    total_visits = models.PositiveIntegerField(default=0, help_text="Tabiy (real) sayt tashriflari — avtomatik oshadi")
    visits_boost = models.PositiveIntegerField(default=0, help_text="Ko'rsatiladigan raqamni sun'iy oshirish uchun qo'shiladigan qiymat")

    class Meta:
        verbose_name = "Sayt statistikasi"
        verbose_name_plural = "Sayt statistikasi"

    def __str__(self):
        return "Sayt statistikasi"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def display_visits(self):
        return self.total_visits + self.visits_boost
