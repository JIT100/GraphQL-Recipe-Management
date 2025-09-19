import strawberry
from typing import List, Optional
from strawberry.types import Info
from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer
from .auth import IsAuthenticated


@strawberry.type
class IngredientType:
    id: strawberry.ID
    name: str
    description: Optional[str]


@strawberry.type
class RecipeType:
    id: strawberry.ID
    name: str
    instructions: Optional[str]
    ingredients: List[IngredientType]

    @strawberry.field
    def ingredient_count(self) -> int:
        return len(self.ingredients)


@strawberry.type()
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def ingredients(self, info: Info, search: Optional[str] = None, first: Optional[int] = 10, offset: Optional[int] = 0) -> List[IngredientType]:
        
        qs = Ingredient.objects.all()
        if search:
            qs = qs.filter(name__icontains=search)
        qs = qs.order_by('name')[offset: offset + first]
        return [IngredientType(id=i.id, name=i.name, description=i.description) for i in qs]

    @strawberry.field(permission_classes=[IsAuthenticated])
    def recipes(self, info: Info, id: Optional[int] = None) -> List[RecipeType]:

        if id:
            qs = Recipe.objects.filter(id=id).prefetch_related('ingredients')
        else:
            qs = Recipe.objects.all().prefetch_related('ingredients')
        result = []
        for r in qs:
            ingredients = [IngredientType(id=i.id, name=i.name, description=i.description) for i in r.ingredients.all()]
            result.append(RecipeType(id=r.id, name=r.name, instructions=r.instructions, ingredients=ingredients))
        return result



@strawberry.type()
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_ingredient(self, info: Info, name: str, description: Optional[str] = None) -> IngredientType:
        serializer = IngredientSerializer(data={"name": name, "description": description})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return IngredientType(id=instance.id, name=instance.name, description=instance.description)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_ingredient(self, info: Info, id: int, name: Optional[str] = None, description: Optional[str] = None) -> IngredientType:
        inst = Ingredient.objects.get(pk=id)
        data = {}
        if name is not None:
            data['name'] = name
        if description is not None:
            data['description'] = description
        serializer = IngredientSerializer(inst, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return IngredientType(id=instance.id, name=instance.name, description=instance.description)

    @strawberry.mutation
    def delete_ingredient(self, info: Info, id: int) -> bool:
        instance = Ingredient.objects.get(pk=id)
        instance.delete()
        return True

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_recipe(self, info: Info, name: str, instructions: Optional[str] = None, ingredient_ids: Optional[List[int]] = None) -> RecipeType:
        serializer = RecipeSerializer(data={"name": name, "instructions": instructions})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if ingredient_ids:
            instance.ingredients.set(Ingredient.objects.filter(id__in=ingredient_ids))
        ingredients = [IngredientType(id=i.id, name=i.name, description=i.description) for i in instance.ingredients.all()]
        return RecipeType(id=instance.id, name=instance.name, instructions=instance.instructions, ingredients=ingredients)

    @strawberry.mutation
    def add_ingredient_to_recipe(self, info: Info, recipe_id: int, ingredient_id: int) -> RecipeType:
        r = Recipe.objects.get(pk=recipe_id)
        ing = Ingredient.objects.get(pk=ingredient_id)
        r.ingredients.add(ing)
        ingredients = [IngredientType(id=i.id, name=i.name, description=i.description) for i in r.ingredients.all()]
        return RecipeType(id=r.id, name=r.name, instructions=r.instructions, ingredients=ingredients)

    @strawberry.mutation
    def remove_ingredient_from_recipe(self, info: Info, recipe_id: int, ingredient_id: int) -> RecipeType:
        r = Recipe.objects.get(pk=recipe_id)
        ing = Ingredient.objects.get(pk=ingredient_id)
        r.ingredients.remove(ing)
        ingredients = [IngredientType(id=i.id, name=i.name, description=i.description) for i in r.ingredients.all()]
        return RecipeType(id=r.id, name=r.name, instructions=r.instructions, ingredients=ingredients)


schema = strawberry.Schema(query=Query, mutation=Mutation)
