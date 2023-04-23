# planner with fastapi

`python3 -m venv venv`
`source venv/bin/activate`

`pip install fastapi uvicorn "pydantic[email]"`
`pip install sqlmodel`

`pip install passlib[bcrypt]`
`pip install python-jose[cryptography] python-multipart`

### mongodb docker

`docker run --name mongodb-local -d -p 27017:27017 mongo`
