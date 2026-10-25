import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_valid_login(login_page):
    login_page.login("student", "Password123")
    login_page.assert_login_success()


@pytest.mark.parametrize("user,pwd", [
    ("student", "wrongpass"),
    ("wronguser", "Password123"),
    ("", ""),
])
def test_invalid_login(login_page, user, pwd):
    login_page.login(user, pwd)
    login_page.assert_login_error()


def test_password_is_masked(login_page):
    expect(login_page.password).to_have_attribute("type", "password")


def test_no_welcome_before_login(login_page):
    expect(login_page.welcome).to_be_empty()