import pytest


@pytest.fixture
def data():
    print("setup")
    yield {"name": "Sunil"}
    print("teardown")


def test_fixture(data):
    assert data["name"] == "Sunil"


@pytest.mark.skip(reason="abhi nahi")
def test_skipped():
    assert False


@pytest.mark.xfail(reason="known bug")
def test_expected_fail():
    assert 1 == 2


def test_exception():
    with pytest.raises(ValueError):
        int("abc")


def test_approx():
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_tmp(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("hi")
    assert f.read_text() == "hi"


@pytest.mark.parametrize("a,b,r", [(1, 2, 3), (2, 3, 5)])
def test_add(a, b, r):
    assert a + b == r