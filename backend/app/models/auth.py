from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, description="Identifiant")
    password: str = Field(min_length=1, description="Mot de passe")


class AuthUserResponse(BaseModel):
    username: str
    name: str
    title: str
    role: str
    is_admin: bool


class LoginResponse(BaseModel):
    token: str
    user: AuthUserResponse
