  

# GraphQL Recipe Management (Django + Strawberry)

  

A small **Dockerized Django project exposing a GraphQL API for managing recipes and ingredients**. It uses:

  

- **Django** (REST framework for serializers)

- **Strawberry for GraphQL**

- **djangorestframework-simplejwt** for JWT authentication

- **PostgreSQL** via Docker Compose

- **WhiteNoise** to serve static files (admin UI)

  

This README explains how to run the project locally with Docker, how to use the GraphQL API (with JWT authentication), and where to find the main code pieces.

  

## ⚖️ Repository layout

  

- **`manage.py`** - Django management script

- **`schema.py`** - (project-level) Strawberry schema entrypoint

- **`config/`** - Django project settings, URLs and WSGI

- **`config/settings/`** - base & environment settings

- **`recipe/`** - Django app with models, serializers and GraphQL schema

- **`recipe/schema.py`** - Strawberry types, queries and mutations

- **`recipe/serializers.py`** - DRF serializers used by GraphQL mutations

- **`recipe/urls.py`** - app-level GraphQL route wrapper

  

Other important files:

  

- **`Dockerfile`**, **`docker-compose.yml`** - Docker configuration


- **`.env`** - environment variables used by Docker and Django (should not be committed)

  

## 🛠️ Quick start (Docker)

  

Prerequisites: Docker and Docker Compose installed.

  

1. Create or copy a `.env` file at the project root and set at minimum:

  

- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (required by Postgres image on first init)

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`

  

2. Build and start the services:

  

```powershell

docker-compose up --build

```

  

To run detached and tail logs:

  

```powershell

docker-compose up --build -d

docker-compose logs -f web

```


  

3. Inside the `web` container create a superuser if you need admin access:

  

```powershell

docker-compose run web python manage.py createsuperuser

```

  

4. Run migrations (if not already applied by container startup):

  

```powershell

docker-compose run web python manage.py makemigrations

docker-compose run web python manage.py migrate

```
## 🏂 Demo user (create_demo_user)

  

- The management command `python manage.py create_demo_user` reads the following environment variables:

-  `DEMO_USERNAME` (username to create/update)

-  `DEMO_PASSWORD` (password to set)

-  `DEMO_EMAIL` (optional email)

-  `DEMO_IS_SUPERUSER` (optional; values `1`, `true`, `yes` are treated as true)

  

- **Behavior**: This is an alternative way to create Demo user, Incase If you can't use `docker-compose run web python manage.py createsuperuser`.  If `DEMO_USERNAME` or `DEMO_PASSWORD` are not provided the command will skip quietly (it prints a short warning and exits successfully). When both are present the command will create or update the user, set the password, and apply the `is_superuser`/`is_staff` flags. This way we can make a default user even when we deploy this app into a cloud service.

  

Example usage snippet:

  
```powershell

docker-compose run web python manage.py migrate

docker-compose run web python manage.py create_demo_user

```

  

- Example environment variables (You have to set these in your host/service UI of Web service, do not commit them to source control):

-  `DEMO_USERNAME=demo`

-  `DEMO_PASSWORD=<secure-password>`

-  `DEMO_EMAIL=demo@example.com`

-  `DEMO_IS_SUPERUSER=False`

  

- **Security**: Never commit credentials into the repository. Use your hosting provider's secret/env management to store demo account credentials.
  

## 🖥️ Static files / Admin UI

  

Static files are collected during the Docker build and served by **WhiteNoise**. If the Django admin appears unstyled:

  

- Confirm `whitenoise` is present in `requirements.txt` and `WhiteNoiseMiddleware` is added to `MIDDLEWARE` in `config/settings/base.py`.

- Rebuild the image to pick up changes:

  

```powershell

docker-compose up --build

```

  

Then open the admin at `http://localhost:8000/admin/` and log in with the superuser.

  

## 🍓 GraphQL API

  

- GraphQL endpoint: `POST /graphql/`

- JWT token endpoint: `POST /api/token/` (DRF SimpleJWT)

  

Authentication: obtain an `access` token from `/api/token/` and include it on GraphQL requests using the `Authorization: Bearer <access_token>` header. The project wires JWT authentication at the GraphQL URL wrapper and resolvers expect `info.context['request']` to contain the Django request.

  

Example: obtain a token with curl (PowerShell):

  

```powershell

curl -X POST http://localhost:8000/api/token/  -H "Content-Type: application/json"  -d '{"username":"<username>","password":"<password>"}'

```

  

Example GraphQL query (ingredients):

  

```graphql

query  {

ingredients(search: "salt",  first: 10,  offset: 0)  {

id

name

description

}

}

```

  

Call via curl (replace `<ACCESS_TOKEN>`):

  

```powershell

curl -X POST http://localhost:8000/graphql/  -H "Content-Type: application/json"  -H "Authorization: Bearer <ACCESS_TOKEN>"  -d '{"query":"query { ingredients(first: 10) { id name } }"}'

```

  

Example GraphQL mutation (create a recipe with ingredient IDs):

  

```graphql

mutation  {

createRecipe(name: "Pasta",  instructions: "Boil.",  ingredientIds: [1,2])  {

id

name

ingredientCount

ingredients  {  id  name  }

}

}

```

  

Call it via curl:

  

```powershell

curl -X POST http://localhost:8000/graphql/  -H "Content-Type: application/json"  -H "Authorization: Bearer <ACCESS_TOKEN>"  -d '{"query":"mutation { createRecipe(name:\"Pasta\", instructions:\"Boil.\", ingredientIds:[1,2]) { id name ingredients { id name } } }"}'

```

  

Mutations and queries are implemented in `recipe/schema.py` and mutations generally use DRF serializers found in `recipe/serializers.py` for validation and creation.

  

## 📚 Development notes

  

- **Schema location**: `recipe/schema.py`. Resolvers receive `info.context['request']` with the Django `request` set by the GraphQL URL wrapper.

- **JWT auth**:  `recipe/urls.py` include a small wrapper that authenticates using DRF's `JWTAuthentication` and sets `request.user` before invoking the Strawberry `GraphQLView`.

- **Permissions**: Strawberry permission classes (e.g. an `IsAuthenticated` permission) used to avoid repeating authentication checks in every resolver.

- **Performance**: The `recipes` resolver uses `prefetch_related('ingredients')` to avoid N+1 queries when resolving nested ingredients.

**Notes**: The `create_demo_user` command reads `DEMO_USERNAME` and `DEMO_PASSWORD` from env and will create or update the account. No default credentials are set in the code.

  

  

## ⚠️ Troubleshooting

  

- "Database is uninitialized and superuser password is not specified": make sure `POSTGRES_PASSWORD` is set in `.env` so the Postgres container initializes.

- `relation 'recipe_recipe' does not exist`: run migrations with `python manage.py migrate` inside the `web` service.

- Admin static assets 404: rebuild image so `collectstatic` runs and verify WhiteNoise is configured in `config/settings/base.py`.

  

## 🔬 Next steps / improvements

  

- Add unit and integration tests for GraphQL resolvers and mutations.

- Add role-based authorization or more granular permissions.

  

## 📧 Contributing

  

Project is developed by **JIT100**. Found an issue or want to request a feature?

+ Please open an Issue on GitHub.
  

---

 