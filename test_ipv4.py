import pytest
from ipv4 import calculate_subnet, SubnetInfo  # Замените your_module на имя вашего модуля

# Тестовые случаи
@pytest.mark.parametrize("ip, subnet_mask, expected", [
    # Тест 1: Обычная подсеть /24
    ("192.168.1.0", "255.255.255.0", SubnetInfo(
        network_address="192.168.1.0",
        broadcast_address="192.168.1.255",
        netmask="255.255.255.0",
        num_hosts=254,
        first_host="192.168.1.1",
        last_host="192.168.1.254"
    )),
    # Тест 2: Подсеть /30 (маленькая подсеть)
    ("10.0.0.0", "255.255.255.252", SubnetInfo(
        network_address="10.0.0.0",
        broadcast_address="10.0.0.3",
        netmask="255.255.255.252",
        num_hosts=2,
        first_host="10.0.0.1",
        last_host="10.0.0.2"
    )),
    # Тест 3: Подсеть /16 (большая подсеть)
    ("172.16.0.0", "255.255.0.0", SubnetInfo(
        network_address="172.16.0.0",
        broadcast_address="172.16.255.255",
        netmask="255.255.0.0",
        num_hosts=65534,
        first_host="172.16.0.1",
        last_host="172.16.255.254"
    )),
    # Тест 4: Подсеть /32 (одноадресная подсеть)
    ("192.168.1.1", "255.255.255.255", SubnetInfo(
        network_address="192.168.1.1",
        broadcast_address="192.168.1.1",
        netmask="255.255.255.255",
        num_hosts=0,
        first_host="192.168.1.1",
        last_host="192.168.1.1"
    )),
])
def test_calculate_subnet(ip, subnet_mask, expected):
    # Вызываем функцию и сравниваем результат с ожидаемым
    result = calculate_subnet(ip, subnet_mask)
    assert result == expected

# Тест на некорректные данные
def test_invalid_subnet():
    with pytest.raises(ValueError):
        calculate_subnet("192.168.1.256", "255.255.255.0")  # Некорректный IP-адрес
