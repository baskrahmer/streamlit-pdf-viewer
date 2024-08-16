import os
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests import ROOT_DIRECTORY
from tests.e2e_utils import StreamlitRunner

BASIC_EXAMPLE_FILE = os.path.join(ROOT_DIRECTORY, "tests", "streamlit_apps", "example_resolution_boost.py")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "firefox_user_prefs": {
            "pdfjs.disabled": False,
        }
    }


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(Path(BASIC_EXAMPLE_FILE)) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


def test_should_render_template_check_container_size(page: Page):
    expect(page.get_by_text("Test PDF Viewer with different resolution boosts")).to_be_visible()
    page.wait_for_selector('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]')
    page.locator('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]').nth(6)
    iframe_components = page.locator('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]').all()
    assert len(iframe_components) == 6

    expect(iframe_components[0]).to_be_visible()
    expect(iframe_components[1]).to_be_visible()
    expect(iframe_components[2]).to_be_visible()
    expect(iframe_components[3]).not_to_be_visible()
    expect(iframe_components[4]).not_to_be_visible()
    expect(iframe_components[5]).not_to_be_visible()

    tab1 = page.get_by_text('tab 1')
    expect(tab1).to_be_visible()

    tab2 = page.get_by_text('tab 2')
    expect(tab2).to_be_visible()

    # Tab 1
    iframe_frame_0 = page.frame_locator('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]').nth(0)
    expect(iframe_frame_0.locator('div[id="pdfContainer"]')).to_be_visible()
    expect(iframe_frame_0.locator('div[id="pdfViewer"]')).to_be_visible()

    iframe_frame_1 = page.frame_locator('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]').nth(1)
    expect(iframe_frame_1.locator('div[id="pdfContainer"]')).to_be_visible()
    expect(iframe_frame_1.locator('div[id="pdfViewer"]')).to_be_visible()

    iframe_frame_2 = page.frame_locator('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]').nth(2)
    expect(iframe_frame_2.locator('div[id="pdfContainer"]')).to_be_visible()
    expect(iframe_frame_2.locator('div[id="pdfViewer"]')).to_be_visible()

    expect(iframe_components[0].locator('div[id="pdfViewer"]').get_by_text("from LaH10 to room–temperature").nth(
        0)).to_be_hidden()
    expect(iframe_components[1].locator('div[id="pdfViewer"]').get_by_text("from LaH10 to room–temperature").nth(
        0)).to_be_hidden()
    expect(iframe_components[2].locator('div[id="pdfViewer"]').get_by_text("from LaH10 to room–temperature").nth(
        0)).to_be_hidden()

    # click on the second tab and verify that the PDF is visible
    tab2.click()

    iframe_components = page.locator('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]').all()
    assert len(iframe_components) == 6

    expect(iframe_components[0]).not_to_be_visible()
    expect(iframe_components[1]).not_to_be_visible()
    expect(iframe_components[2]).not_to_be_visible()
    expect(iframe_components[3]).to_be_visible()
    expect(iframe_components[4]).to_be_visible()
    expect(iframe_components[5]).to_be_visible()

    iframe_frame_3 = page.frame_locator('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]').nth(3)
    expect(iframe_frame_3.locator('div[id="pdfContainer"]')).to_be_visible()
    expect(iframe_frame_3.locator('div[id="pdfViewer"]')).to_be_visible()

    iframe_frame_4 = page.frame_locator('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]').nth(4)
    expect(iframe_frame_4.locator('div[id="pdfContainer"]')).to_be_visible()
    expect(iframe_frame_4.locator('div[id="pdfViewer"]')).to_be_visible()

    iframe_frame_5 = page.frame_locator('iframe[title="streamlit_pdf_viewer.streamlit_pdf_viewer"]').nth(5)
    expect(iframe_frame_5.locator('div[id="pdfContainer"]')).to_be_visible()
    expect(iframe_frame_5.locator('div[id="pdfViewer"]')).to_be_visible()

    expect(iframe_frame_3.locator('div[id="pdfViewer"]').get_by_text("from LaH10 to room–temperature").nth(
        0)).to_be_visible()
    expect(iframe_frame_4.locator('div[id="pdfViewer"]').get_by_text("from LaH10 to room–temperature").nth(
        0)).to_be_visible()
    expect(iframe_frame_5.locator('div[id="pdfViewer"]').get_by_text("from LaH10 to room–temperature").nth(
        0)).to_be_visible()
