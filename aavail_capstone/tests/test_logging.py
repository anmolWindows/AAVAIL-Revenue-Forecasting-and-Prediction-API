from app.logging_utils import get_logger

def test_logger_writes_json(tmp_path):
    path = tmp_path / "test.log"
    logger = get_logger("test_logger_unique", str(path))
    logger.info("hello")
    assert path.exists()
    assert "hello" in path.read_text()
