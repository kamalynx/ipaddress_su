from ipaddress import IPv4Network, IPv4Address
from dataclasses import dataclass


@dataclass
class SubnetInfo:
    network_address: str
    broadcast_address: str
    netmask: str
    num_hosts: int
    first_host: str
    last_host: str


def calculate_subnet(ipaddress: str, netmask: str) -> SubnetInfo:
    # Создаем объект сети
    network = IPv4Network(f"{ipaddress}/{netmask}", strict=False)

    # Возвращаем информацию о подсети в виде dataclass
    return SubnetInfo(
        network_address=str(network.network_address),
        broadcast_address=str(network.broadcast_address),
        netmask=str(network.netmask),
        num_hosts=network.num_addresses
        - 2,  # Исключаем сетевой и широковещательный адреса
        first_host=str(IPv4Address(int(network.network_address) + 1)),
        last_host=str(IPv4Address(int(network.broadcast_address) - 1)),
    )


if __name__ == "__main__":
    # Пример использования
    ip = "192.168.1.0"
    subnet_mask = "255.255.255.0"
    subnet_info = calculate_subnet(ip, subnet_mask)

    print(subnet_info)
