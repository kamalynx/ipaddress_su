import pytest
from ipv6 import ipv6_subnet_calculator, IPv6SubnetInfo  # Замените `your_module` на имя вашего модуля

# Тест для корректного IPv6 адреса и префикса
def test_valid_ipv6_subnet():
    result = ipv6_subnet_calculator("2001:0db8:85a3::", 64)
    
    # Проверяем, что результат не None
    assert result is not None
    
    # Проверяем, что результат является объектом IPv6SubnetInfo
    assert isinstance(result, IPv6SubnetInfo)
    
    # Проверяем конкретные значения
    assert result.network_address == "2001:db8:85a3::"
    assert result.broadcast_address == "2001:db8:85a3:ffff:ffff:ffff:ffff:ffff"
    assert result.netmask == "ffff:ffff:ffff:ffff::"
    assert result.hostmask == "::ffff:ffff:ffff:ffff"
    assert result.prefix_length == 64
    assert result.num_addresses == 18446744073709551616
    assert result.is_private is False
    assert result.is_global is True
    assert result.is_link_local is False
    assert result.is_multicast is False
    assert result.is_reserved is False
    assert result.address_range == "2001:db8:85a3:: - 2001:db8:85a3:ffff:ffff:ffff:ffff:ffff"

# Тест для некорректного IPv6 адреса
def test_invalid_ipv6_address():
    result = ipv6_subnet_calculator("invalid_ipv6", 64)
    
    # Проверяем, что функция вернула None
    assert result is None

# Тест для некорректной длины префикса
def test_invalid_prefix_length():
    result = ipv6_subnet_calculator("2001:0db8:85a3::", 129)  # Префикс больше 128
    
    # Проверяем, что функция вернула None
    assert result is None

# Тест для частного IPv6 адреса
def test_private_ipv6_subnet():
    result = ipv6_subnet_calculator("fd00::", 64)
    
    # Проверяем, что результат не None
    assert result is not None
    
    # Проверяем, что адрес является частным
    assert result.is_private is True

# Тест для multicast IPv6 адреса
def test_multicast_ipv6_subnet():
    result = ipv6_subnet_calculator("ff02::1", 64)
    
    # Проверяем, что результат не None
    assert result is not None
    
    # Проверяем, что адрес является multicast
    assert result.is_multicast is True

# Тест для link-local IPv6 адреса
def test_link_local_ipv6_subnet():
    result = ipv6_subnet_calculator("fe80::", 64)
    
    # Проверяем, что результат не None
    assert result is not None
    
    # Проверяем, что адрес является link-local
    assert result.is_link_local is True

# Тест для зарезервированного IPv6 адреса
def test_reserved_ipv6_subnet():
    result = ipv6_subnet_calculator("::", 128)  # Неопределенный адрес
    
    # Проверяем, что результат не None
    assert result is not None
    
    # Проверяем, что адрес является зарезервированным
    assert result.is_reserved is True
