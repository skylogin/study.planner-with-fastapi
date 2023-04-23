# planner with fastapi

`python3 -m venv venv`
`source venv/bin/activate`

`pip install fastapi uvicorn "pydantic[email]"`
`pip install sqlmodel`

`pip install passlib[bcrypt]`
`pip install python-jose[cryptography] python-multipart`

`pip install pytest`
`pip install httpx pytest-asyncio`

`pip install coverage`

### mongodb docker

`docker run --name mongodb-local -d -p 27017:27017 mongo`

### coverage

`coverage run -m pytest`
`coverage report`
`coverage html`

### build

`docker build -t event-planner-api .`
`docker-compose up -d`
