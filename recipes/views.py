from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from .forms import RecipeForm
from django.urls import reverse
import qrcode
import io
import base64
from django.http import JsonResponse


def index(request):
    selected_category = request.GET.get("category", "")

    if selected_category and selected_category != "全て":
        recipes = Recipe.objects.filter(category=selected_category).order_by(
            "-created_at"
        )
    else:
        recipes = Recipe.objects.all().order_by("-created_at")

    # カテゴリリストと選択フラグを作る
    categories = ["全て", "和食", "洋食", "スイーツ"]
    categories_with_selected = []
    for cat in categories:
        categories_with_selected.append(
            {"name": cat, "selected": (cat == selected_category)}
        )

    return render(
        request,
        "recipes/index.html",
        {"recipes": recipes, "categories": categories_with_selected},
    )


def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)  # ←ここを追加
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = RecipeForm()
    return render(request, "recipes/create.html", {"form": form})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipes/detail.html", {"recipe": recipe})


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        form = RecipeForm(
            request.POST, request.FILES, instance=recipe
        )  # ← request.FILES を追加
        if form.is_valid():
            form.save()
            return redirect("recipe_detail", recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "recipes/edit.html", {"form": form, "recipe": recipe})


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        recipe.delete()
        return redirect("index")
    return render(request, "recipes/delete_confirm.html", {"recipe": recipe})


def qr_view(request):
    url = "http://10.111.1.180:8000/"  # スマホからアクセスするURL

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "recipes/qr.html", {"qr_code": img_str})


def recipe_qr(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    url = request.build_absolute_uri(reverse("recipe_detail", args=[recipe_id]))

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "recipes/qr.html", {"qr_code": img_str, "recipe": recipe})


def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.is_favorite = not recipe.is_favorite
    recipe.save()
    return JsonResponse({"is_favorite": recipe.is_favorite})
