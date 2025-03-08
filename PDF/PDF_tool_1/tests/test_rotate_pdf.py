import fitz
import pytest

from rotate_pdf import rotate_pdf_pages_window


@pytest.fixture
def pdf_file(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    doc = fitz.open()
    for i in range(5):
        page = doc.new_page()
        page.insert_text((72, 72), f"Page {i + 1}")
    doc.save(pdf_path)
    doc.close()
    return pdf_path


def test_rotate_pdf_pages_window(pdf_file, tmp_path, monkeypatch):
    save_path = tmp_path / "rotated.pdf"

    def mock_popup_error(*args, **kwargs):
        pass

    def mock_popup(*args, **kwargs):
        pass

    def mock_read():
        return events.pop(0)

    monkeypatch.setattr("TkEasyGUI.popup_error", mock_popup_error)
    monkeypatch.setattr("TkEasyGUI.popup", mock_popup)

    # テスト用のイベントと値を設定
    events = [
        ("FILE_PATH", {"FILE_PATH": str(pdf_file)}),
        (
            "ROTATE",
            {"FILE_PATH": str(pdf_file), "SAVE_PATH": str(save_path), "ROTATION": "右 90 度", "ALL_PAGES": True},
        ),
    ]

    monkeypatch.setattr("TkEasyGUI.Window.read", mock_read)

    rotate_pdf_pages_window()

    # 出力ファイルの確認
    doc = fitz.open(save_path)
    assert doc.page_count == 5
    for page in doc:
        assert page.rotation == 90
    doc.close()
