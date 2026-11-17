"""
CampusCare – Session-state based authentication.
Hardcoded demo credentials only; no real password storage.
"""
import streamlit as st

# Demo credentials: {username: (password, role)}
_USERS = {
    "student": ("student123", "student"),
    "admin":   ("admin123",   "admin"),
}

_SESSION_AUTHENTICATED = "authenticated"
_SESSION_ROLE = "role"
_SESSION_USERNAME = "username"


def login(username: str, password: str) -> tuple[bool, str]:
    """Attempt login. Returns (True, role) on success, (False, '') on failure."""
    entry = _USERS.get(username.strip())
    if entry and entry[0] == password:
        st.session_state[_SESSION_AUTHENTICATED] = True
        st.session_state[_SESSION_ROLE] = entry[1]
        st.session_state[_SESSION_USERNAME] = username.strip()
        return True, entry[1]
    return False, ""


def logout() -> None:
    """Clear login keys from session state."""
    for key in (_SESSION_AUTHENTICATED, _SESSION_ROLE, _SESSION_USERNAME):
        st.session_state.pop(key, None)


def get_current_role() -> str:
    """Return the logged-in user's role, or '' if not authenticated."""
    return st.session_state.get(_SESSION_ROLE, "")


def get_current_user() -> str:
    """Return the logged-in username, or '' if not authenticated."""
    return st.session_state.get(_SESSION_USERNAME, "")


def is_authenticated() -> bool:
    """Return True if the user is logged in."""
    return bool(st.session_state.get(_SESSION_AUTHENTICATED, False))
