from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks

from django.db import models



class HomePage(Page):

    subtitle = RichTextField(blank=True, features=["bold", "italic"])

    hero_image = StreamField(
        [
            ("image", ImageChooserBlock(required=False)),
        ],
        blank=True,
        use_json_field=True,
    )

    content = StreamField(
        [
            ("title", blocks.CharBlock(form_classname="full title")),
            ("text", blocks.RichTextBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("content"),
    ]

class ProjectPage(Page):
    """Page pour chaque projet du portfolio."""

    template = "home/project_page.html"

    description = RichTextField(blank=True)
    hero_image = StreamField(
        [
            ("image", ImageChooserBlock(required=False)),
        ],
        blank=True,
        use_json_field=True,
    )
    content = StreamField(
        [
            ("title", blocks.CharBlock(form_classname="full title")),
            ("text", blocks.RichTextBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    # ⚡ Limiter où cette page peut être créée
    parent_page_types = ["home.PortfolioIndexPage"]
    subpage_types = []  # Les projets n'auront pas d'enfants

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("hero_image"),
        FieldPanel("content"),
    ]


class PortfolioIndexPage(Page):
    """Page d'accueil du portfolio, liste tous les projets."""

    template = "home/portfolio_index_page.html"


    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]



    def get_context(self, request):
        context = super().get_context(request)
        context["projects"] = ProjectPage.objects.child_of(self).live()
        return context



















