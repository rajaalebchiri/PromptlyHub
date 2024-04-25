# PromptlyHub


## Introduction
A simple REST API built with Flask for generating, and managing AI prompts.


## Features
- CRUD operations for managing AI prompts.
- User authentication and management.
- Supports operations on prompt examples and tags.
- Swagger documentation is now available for easier API navigation and testing.
- Database has been migrated to PostgreSQL for better scalability and performance.
- New feature: Get prompts by category/tag.
  - Accepts: Category/Tag name
  - Returns: Prompts belonging to the specified category/tag

## Installation

### Prerequisites

- Docker
- Python 3.10
- PostgreSQL

### Setup

1. **Clone the repository**:
   ```bash
   git clone [repository-url]
   cd promptlyhub
   ````

2. **Setting Up Your Development Environment**
    
    **Environment Variables:**
        
    Rename `.env.test` to `.env` and ensure all necessary environment variables are correctly set up for your local development.
    
    **Database Configuration:**
        
    Ensure PostgreSQL is set up and configured in your `.env` file.

3. **Build the Docker image**:
    ```bash
    docker build -t promptlyhub .
    ````

4. **Run the container**:
    ```bash
    docker run -p 5050:5050 promptlyhub
    ````

## API Documentation

Access the Swagger UI to see and interact with the API's endpoints by navigating to:
`{{url}}/swagger-uir`

### Detailed Endpoint Descriptions

#### Prompts

##### List all prompts:
- **Endpoint**: `GET /prompts`
- **Description**: Retrieves a list of all prompts.

##### List prompts by category:
- **Endpoint**: `GET /prompts/{TAG}`
- **Description**: Retrieves a list of all prompts with a specific tag.

##### Create a Prompt
- **Endpoint**: `POST /prompt`
- **Description**: Creates a new prompt.

##### Retrieve a prompt by ID
- **Endpoint**: `GET /prompt/{PROMPT_ID}`
- **Description**: Get a prompt by ID.

##### Update a prompt by ID
- **Endpoint**: `PUT /prompt/{PROMPT_ID}`
- **Description**: Update a prompt by ID.

##### Delete a prompt by ID
- **Endpoint**: `DELETE /prompt/{PROMPT_ID}`
- **Description**: Delete a prompt by ID.


#### Examples

##### Retrieve examples for a specific prompt:
- **Endpoint**: `GET /prompt/{PROMPT_ID}/examples`
- **Description**: Retrieves all examples associated with a specific prompt.
  
##### Create an example for a prompt:
- **Endpoint**: `POST /example`
- **Description**: Create an Example associated with a specific prompt.
    ```JSON
    {
    "details": "Suggest 10 blog post ideas",
    "prompt_id": "1"
    }
    ```

##### Update an example by ID:
- **Endpoint**: `PUT /example/{EXAMPLE_ID}`
- **Description**: Update example Informations by ID.

##### Delete an example by ID:
- **Endpoint**: `DELETE /example/{EXAMPLE_ID}`
- **Description**: Delete Example by ID.

#### Tags

##### Retrieve tags for a specific prompt:
- **Endpoint**: `GET /prompt/{PROMPT_ID}/tag`
- **Description**: Retrieves all tags associated with a specific prompt.

##### Associate a tag with a prompt:
- **Endpoint**: `POST /prompt/{PROMPT_ID}/tag`
- **Description**: Add a tag to a prompt

##### Delete a tag:
- **Endpoint**: `DELETE /tag/{TAG_ID}`
- **Description**: Delete a tag associated with a specific prompt
  
### Authentication

##### Register a user:
- **Endpoint**: `POST /register`
- **Description**: Create a new user
    ```json
    {
    "username": "rajaa-leb",
    "password": "admin"
    }
    ````

##### Authenticate a user (login):
- **Endpoint**: `POST /login`
- **Description**: Log in a user.


##### Log out the current user:
- **Endpoint**: `POST /logout`
- **Description**: Log out a user.


##### Retrieve user details:
- **Endpoint**: `GET /user/{USER_ID}`
- **Description**: Get details about a specified user.


##### Delete a user:
- **Endpoint**: `DELETE /user/{USER_ID}`
- **Description**: Delete a user account.


## Usage
To interact with the API, start by registering as a new user or logging in to receive a token. This token must be included in the Authorization header for accessing protected routes.

```bash
curl -X POST http://127.0.0.1:5050/login -d '{"username":"user-data", "password":"password"}'
````

## Contributing
Contributions to PromptlyHub are welcome. Please fork the repository, make your changes, and submit a pull request.

## License
PromptlyHub is released under the MIT License. This license permits anyone to use, modify, distribute, and sell this software for any purpose, provided they include the original copyright and permission notice in any copy of the software or substantial portions of it. For more detailed information, please refer to the LICENSE file in the repository.
