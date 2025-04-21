import ipaddress
import logging
from dataclasses import dataclass

# Настройка логгера
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Создаем dataclass для хранения информации о подсети
@dataclass
class IPv6SubnetInfo:
    network_address: str
    broadcast_address: str
    netmask: str
    hostmask: str
    prefix_length: int
    num_addresses: int
    is_private: bool
    is_global: bool
    is_link_local: bool
    is_multicast: bool
    is_reserved: bool
    address_range: str

def ipv6_subnet_calculator(ipv6_address, prefix_length):
    try:
        # Создаем объект IPv6Network
        network = ipaddress.IPv6Network(f"{ipv6_address}/{prefix_length}", strict=False)
        
        # Создаем объект dataclass с информацией о подсети
        subnet_info = IPv6SubnetInfo(
            network_address=str(network.network_address),
            broadcast_address=str(network.broadcast_address),
            netmask=str(network.netmask),
            hostmask=str(network.hostmask),
            prefix_length=network.prefixlen,
            num_addresses=network.num_addresses,
            is_private=network.is_private,
            is_global=network.is_global,
            is_link_local=network.is_link_local,
            is_multicast=network.is_multicast,
            is_reserved=network.is_reserved,
            address_range=f"{network.network_address} - {network.broadcast_address}"
        )
        
        return subnet_info
    
    except ipaddress.AddressValueError as e:
        # Логируем ошибку
        logging.error(f"Invalid IPv6 address or prefix length: {e}")
        return None
    except Exception as e:
        # Логируем другие возможные ошибки
        logging.error(f"An unexpected error occurred: {e}")
        return None

# Пример использования
result = ipv6_subnet_calculator("2001:0db8:85a3::", 64)
if result:
    print(result)
else:
    print("Failed to calculate subnet information.")

