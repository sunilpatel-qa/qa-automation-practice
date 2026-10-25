import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def open_site(page: Page):
    page.goto("/")          # --base-url se judta hai


@pytest.mark.smoke
def test_title(page: Page):
    expect(page).to_have_title("QA Practice Site")


@pytest.mark.smoke
@pytest.mark.parametrize("user,pwd,ok", [
    ("student", "Password123", True),
    ("student", "wrong", False),
    ("", "", False),
])
def test_login(page: Page, user, pwd, ok):
    page.get_by_placeholder("Username").fill(user)
    page.get_by_placeholder("Password").fill(pwd)
    page.get_by_role("button", name="Login").click()
    if ok:
        expect(page.locator("#welcome")).to_have_text("Welcome student")
    else:
        expect(page.get_by_role("alert")).to_have_text("Invalid credentials")


def test_checkbox_radio_dropdown(page: Page):
    page.get_by_label("I agree").check()
    expect(page.get_by_label("I agree")).to_be_checked()
    page.get_by_label("Female").check()
    page.get_by_label("City").select_option("Pune")
    expect(page.locator("#city-out")).to_have_text("Selected: Pune")


def test_alert(page: Page):
    page.on("dialog", lambda d: d.accept())
    page.get_by_role("button", name="Show alert").click()
    expect(page.locator("#result")).to_have_text("Alert closed")


def test_confirm_cancel(page: Page):
    page.on("dialog", lambda d: d.dismiss())
    page.get_by_role("button", name="Show confirm").click()
    expect(page.locator("#result")).to_have_text("You clicked Cancel")


def test_iframe(page: Page):
    expect(page.frame_locator("#frame1").get_by_text("Hello from iframe")).to_be_visible()


def test_new_tab(page: Page, context):
    with context.expect_page() as info:
        page.get_by_text("Open new tab").click()
    new = info.value
    new.wait_for_load_state()
    expect(new.locator("h3")).to_have_text("New Window")


def test_upload(page: Page, tmp_path):
    f = tmp_path / "resume.txt"
    f.write_text("hello")
    page.set_input_files("#file", str(f))
    expect(page.locator("#file-out")).to_have_text("Uploaded: resume.txt")


def test_download(page: Page, tmp_path):
    with page.expect_download() as d:
        page.get_by_text("Download sample.txt").click()
    path = tmp_path / d.value.suggested_filename
    d.value.save_as(path)
    assert path.read_text() == "QA practice file"


def test_hover(page: Page):
    page.locator("#hover-me").hover()
    expect(page.locator("#tip")).to_be_visible()


def test_dynamic_loading(page: Page):
    page.get_by_role("button", name="Start").click()
    expect(page.locator("#dyn-out")).to_have_text("Loading...")
    expect(page.locator("#dyn-out")).to_have_text("Finished!", timeout=5000)   # auto-wait


def test_table(page: Page):
    rows = page.locator("#table tr")
    expect(rows).to_have_count(4)
    expect(rows.filter(has_text="Neha")).to_contain_text("Surat")


def test_api_request(playwright, base_url):
    api = playwright.request.new_context(base_url=base_url)
    res = api.get("/users.json")
    assert res.status == 200
    assert len(res.json()) == 3


def test_network_mock(page: Page):
    page.route("**/users.json", lambda r: r.fulfill(json=[{"id": 9}]))
    page.get_by_role("button", name="Load users").click()
    expect(page.locator("#user-count")).to_have_text("Users: 1")


def test_screenshot(page: Page):
    page.screenshot(path="home.png", full_page=True)
