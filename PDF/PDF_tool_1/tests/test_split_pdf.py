import fitz
import pytest

from split_pdf import split_pdf_window


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


def test_split_pdf_window(pdf_file, tmp_path, monkeypatch):
    save_folder = tmp_path / "output"
    save_folder.mkdir()

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
        ("SPLIT", {"PDF_PATH": str(pdf_file), "SAVE_FOLDER": str(save_folder), "PAGE_NUMS": "1,3,5"}),
    ]

    monkeypatch.setattr("TkEasyGUI.Window.read", mock_read)

    split_pdf_window()

    # 出力ファイルの確認
    output_files = list(save_folder.glob("*.pdf"))
    assert len(output_files) == 3
    for output_file in output_files:
        doc = fitz.open(output_file)
        assert doc.page_count > 0
        doc.close()
