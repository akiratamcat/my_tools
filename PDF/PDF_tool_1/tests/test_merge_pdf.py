import fitz
import pytest

from merge_pdf import merge_pdf_window


@pytest.fixture
def pdf_files(tmp_path):
    pdf_paths = []
    for i in range(2):
        pdf_path = tmp_path / f"test_{i + 1}.pdf"
        doc = fitz.open()
        for j in range(3):
            page = doc.new_page()
            page.insert_text((72, 72), f"Page {j + 1} of PDF {i + 1}")
        doc.save(pdf_path)
        doc.close()
        pdf_paths.append(pdf_path)
    return pdf_paths


def test_merge_pdf_window(pdf_files, tmp_path, monkeypatch):
    output_file = tmp_path / "merged.pdf"

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
        ("ADD_FILES", {"ADD_FILES": [str(pdf) for pdf in pdf_files]}),
        ("MERGE", {"OUTPUT_FILE": str(output_file)}),
    ]

    monkeypatch.setattr("TkEasyGUI.Window.read", mock_read)

    merge_pdf_window()

    # 出力ファイルの確認
    doc = fitz.open(output_file)
    assert doc.page_count == 6
    doc.close()
