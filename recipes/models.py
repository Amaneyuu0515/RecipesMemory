from django.db import models


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ("和食", "和食"),
        ("洋食", "洋食"),
        ("スイーツ", "スイーツ"),
    ]

    title = models.CharField(max_length=100)
    ingredients = models.TextField(verbose_name="材料")
    instructions = models.TextField(verbose_name="作り方")
    image = models.ImageField(upload_to="recipe_images/", blank=True, null=True)
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, default="和食"
    )  # ←追加
    created_at = models.DateTimeField(auto_now_add=True)

    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title
