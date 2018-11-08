from io import StringIO
from .context import parser


def test_vertically_centered_simple():
    data = (
        "Col1,Col2,Col3\n"
        "r1c1,r1c2,r1c3\n"
        ",r2c2a,\n"
        "r2c1,,r2c3\n"
        ",r2c2b,\n"
        "r3c1,r3c2,r3c3"
    )
    data_io = StringIO()
    data_io.write(data)
    stream = parser.parse_vertically_centered_rows(
        data_io.getvalue().splitlines()
    )
    expected_output = (
        '"Col1","Col2","Col3"\r\n'
        '"r1c1","r1c2","r1c3"\r\n'
        '"r2c1","r2c2a r2c2b","r2c3"\r\n'
        '"r3c1","r3c2","r3c3"\r\n'
    )
    assert stream.getvalue() == expected_output


def test_vertically_centered_multiple_nested_rows():
    data = (
        "Col1,Col2,Col3\n"
        "r1c1,r1c2,r1c3\n"
        ",r2c2a,\n"
        "r2c1,,r2c3\n"
        ",r2c2b,\n"
        ",r3c2a,\n"
        "r3c1,,r3c3\n"
        ",r3c2b,\n"
        "r4c1,r4c2,r4c3"
    )
    data_io = StringIO()
    data_io.write(data)
    stream = parser.parse_vertically_centered_rows(
        data_io.getvalue().splitlines()
    )
    expected_output = (
        '"Col1","Col2","Col3"\r\n'
        '"r1c1","r1c2","r1c3"\r\n'
        '"r2c1","r2c2a r2c2b","r2c3"\r\n'
        '"r3c1","r3c2a r3c2b","r3c3"\r\n'
        '"r4c1","r4c2","r4c3"\r\n'
    )
    assert stream.getvalue() == expected_output


def test_vertically_centered_begins_with_nested_rows():
    data = (
        ",r1c2a,\n"
        "r1c1,,r1c3\n"
        ",r1c2b,\n"
        "r2c1,r2c2,r2c3\n"
        "r3c1,r3c2,r3c3"
    )
    data_io = StringIO()
    data_io.write(data)
    stream = parser.parse_vertically_centered_rows(
        data_io.getvalue().splitlines()
    )
    expected_output = (
        '"r1c1","r1c2a r1c2b","r1c3"\r\n'
        '"r2c1","r2c2","r2c3"\r\n'
        '"r3c1","r3c2","r3c3"\r\n'
    )
    assert stream.getvalue() == expected_output


def test_vertically_centered_ends_with_nested_rows():
    data = "r1c1,r1c2,r1c3\n" ",r2c2a,\n" "r2c1,,r2c3\n" ",r2c2b,"
    data_io = StringIO()
    data_io.write(data)
    stream = parser.parse_vertically_centered_rows(
        data_io.getvalue().splitlines()
    )
    expected_output = (
        '"r1c1","r1c2","r1c3"\r\n' '"r2c1","r2c2a r2c2b","r2c3"\r\n'
    )
    assert stream.getvalue() == expected_output
