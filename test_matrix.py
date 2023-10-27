import pytest

from .matrix import Matrix, MatrixError, parse_matrix


def test_matrix_sum():
    m_1 = Matrix([[1, 1], [-2, 3]])
    m_2 = Matrix([[3, 4], [-1, 9]])

    result = m_1 + m_2

    assert result == Matrix([[4, 5], [-3, 12]])

#
# def test_bad_matrix_sum():
#     m_1 = Matrix([[1, 1], [-2, 3]])
#     m_2 = Matrix([[3, 4], [-1, 9], [-1, 9]])
#
#     was_exception = False
#     try:
#         m_1 + m_2
#     except MatrixError:
#         was_exception = True
#
#     assert was_exception


def test_bad_matrix_sum():
    m_1 = Matrix([[1, 1], [-2, 3]])
    m_2 = Matrix([[3, 4], [-1, 9], [-1, 9]])

    with pytest.raises(MatrixError):
        m_1 + m_2


@pytest.mark.parametrize(
    'input_str, is_error',
    [
        ('[[2,3]]', False),
        ('[[2,3], [1,3,2]]', True),
        ('123', False),
        ('[]', True),
        (';', True),
        ('[[2,3], 2]', True),
        ('hh', True)
    ]
)
def test_parse_matrix(input_str, is_error):
    x = parse_matrix(input_str)

    assert (x is None) == is_error

def test_matrix_mul1():
    m_1 = Matrix([[1, 1], [-2, 3]])
    m_2 = Matrix([[3, 4], [-1, 9]])
    result = m_1 * m_2

    assert result == Matrix([[2, 13], [-9, 19]])

def test_matrix_mul2():
    m_1 = Matrix([[1, 1], [-2, 3]])
    m_2 = 3
    result = m_1 * m_2

    assert result == Matrix([[3, 3], [-6, 9]])

def test_bad_matrix_mul():
    m_1 = Matrix([[1, 1], [-2, 3]])
    m_2 = Matrix([[3, 4], [-1, 9], [-1, 9]])

    with pytest.raises(MatrixError):
        m_1 * m_2

def test_matrix_pow1():
    m_1 = Matrix([[1, 1], [-2, 3]])
    pow = 4
    result = m_1 ** pow

    assert result == Matrix([[-31, 24], [-48, 17]])

def test_matrix_pow2():
    m_1 = Matrix([[1, 1], [-2, 3]])
    pow = 3
    result = m_1 ** pow

    assert result == Matrix([[-9, 11], [-22, 13]])

def test_matrix_pow3():
    m_1 = Matrix([[1, 1], [-2, 3]])
    pow = 0
    result = m_1 ** pow

    assert result == Matrix([[1, 0], [0, 1]])

def test_bad_matrix_pow():
    m_1 = Matrix([[1, 1], [-2, 3], [-1, 9]])
    pow = 2
    with pytest.raises(MatrixError):
        m_1 ** pow

def test_matrix_transpose():
    m_1 = Matrix([[1, 1], [-2, 3]])
    result = m_1.transpose()

    assert result == Matrix([[1, -2], [1, 3]])

def test_matrix_size():
    m_1 = Matrix([[1, 1], [-2, 3]])
    result = m_1.size()

    assert result == '2 x 2'
