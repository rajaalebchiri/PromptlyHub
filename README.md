# PromptlyHub

A simple REST API built with Flask for generating, and managing AI prompts.

## Get Started

Initialize database

```
flask db init
```

migration

```
flask db migrate
```

push migrations

```
flask db upgrade
```

## Endpoints 

### GET /prompts
* **Description:** Retrieves a list of all available prompts.