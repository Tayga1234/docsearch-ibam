from dataclasses import asdict, dataclass
from secrets import compare_digest, token_urlsafe

from fastapi import Depends, Header, HTTPException

ROLE_USER = "user"
ROLE_ADMIN = "admin"


@dataclass(frozen=True)
class AuthUser:
    username: str
    name: str
    title: str
    role: str

    def to_public(self) -> dict:
        data = asdict(self)
        data["is_admin"] = self.role == ROLE_ADMIN
        return data


DEMO_USERS = {
    "fatou": {
        "password": "isgo",
        "user": AuthUser(
            username="fatou",
            name="Fatou Sanou",
            title="Bibliothécaire",
            role=ROLE_USER,
        ),
    },
    "admin": {
        "password": "archives",
        "user": AuthUser(
            username="admin",
            name="Gaetan KOROGO",
            title="Administrateur des archives",
            role=ROLE_ADMIN,
        ),
    },
}

_sessions: dict[str, AuthUser] = {}


def authenticate(username: str, password: str) -> AuthUser | None:
    record = DEMO_USERS.get(username.strip().lower())
    if record is None:
        return None
    if not compare_digest(record["password"], password):
        return None
    return record["user"]


def create_session(user: AuthUser) -> str:
    token = token_urlsafe(32)
    _sessions[token] = user
    return token


def get_session(token: str) -> AuthUser | None:
    return _sessions.get(token)


def drop_session(token: str) -> None:
    _sessions.pop(token, None)


def get_current_user(authorization: str | None = Header(default=None)) -> AuthUser:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Connexion requise")
    token = authorization.split(" ", 1)[1].strip()
    user = get_session(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Session expirée. Reconnectez-vous.")
    return user


def require_admin(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if user.role != ROLE_ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Cette action est réservée à l'administrateur.",
        )
    return user
