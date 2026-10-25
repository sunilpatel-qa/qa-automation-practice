from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error = page.get_by_role("alert")
        self.welcome = page.locator("#welcome")

    def open(self):
        self.page.goto("/")

    def login(self, user: str, pwd: str):
        self.username.fill(user)
        self.password.fill(pwd)
        self.login_button.click()

    def assert_login_success(self):
        expect(self.welcome).to_have_text("Welcome student")

    def assert_login_error(self, message="Invalid credentials"):
        expect(self.error).to_have_text(message)