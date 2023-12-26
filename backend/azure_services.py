from azure.core.exceptions import ResourceNotFoundError
from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.v2023_07_01.models import VirtualMachine, HardwareProfile, OSProfile, NetworkProfile, \
    NetworkInterfaceReference, StorageProfile
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

# Azure Client configuration
credential = AzureCliCredential()
subscription_id = "ea0ab0bd-6f71-4b45-822b-6626ba8ba20e"  # My current active subscription. Replace this with your subscription ID from Azure.
resource_client = ResourceManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

subnet_name = 'mySubnet'
address_space = '10.0.0.0/16'


def create_vnet(rg, location, name, address_space='10.0.0.0/16'):
    """
    Create or get a virtual network.
    """
    try:
        vnet = network_client.virtual_networks.get(rg, name)
        print(f"VNet '{name}' already exists.")
        return vnet
    except ResourceNotFoundError:
        print(f"Creating VNet '{name}'...")
        poller = network_client.virtual_networks.begin_create_or_update(
            rg,
            name,
            {
                'location': location,
                'address_space': {
                    'address_prefixes': [address_space]
                }
            }
        )
        return poller.result()


def create_subnet(rg, vnet_name, subnet_name, subnet_address='10.0.0.0/24'):
    """
    Create or get a subnet within a specified virtual network.
    """
    try:
        vnet = network_client.virtual_networks.get(rg, vnet_name)
        existing_subnet = next((subnet for subnet in vnet.subnets if subnet.name == subnet_name), None)
        if existing_subnet:
            print(f"Subnet '{subnet_name}' already exists.")
            return existing_subnet

        print(f"Creating Subnet '{subnet_name}'...")
        poller = network_client.subnets.begin_create_or_update(
            rg,
            vnet_name,
            subnet_name,
            {'address_prefix': subnet_address}
        )
        return poller.result()
    except Exception as e:
        print(f"An error occurred while creating the subnet: {e}")
        return None


def create_nic(rg, location, public_ip_id, subnet_id, nic_name='myNic'):
    """
    Create a network interface.
    """
    try:
        print(f"Creating NIC '{nic_name}'...")
        poller = network_client.network_interfaces.begin_create_or_update(
            rg,
            nic_name,
            {
                'location': location,
                'ip_configurations': [
                    {
                        'name': 'myIpConfig',
                        'public_ip_address': {'id': public_ip_id},
                        'subnet': {'id': subnet_id}
                    }
                ]
            }
        )
        return poller.result()
    except Exception as e:
        print(f"An error occurred while creating NIC: {e}")
        return None


def create_public_ip(rg, location, public_ip_name='myPublicIP'):
    """
    Create a public IP address.
    """
    try:
        print(f"Creating Public IP '{public_ip_name}'...")
        poller = network_client.public_ip_addresses.begin_create_or_update(
            rg,
            public_ip_name,
            {
                'location': location,
                'sku': {'name': 'Basic'},
                'public_ip_allocation_method': 'Dynamic'
            }
        )
        return poller.result()
    except Exception as e:
        print(f"An error occurred while creating Public IP: {e}")
        return None


def create_vm(resource_group_name, location, vm_name, nic_id, admin_username="adminuser",
              admin_password="nMwmLmdub13i5thHMD0aEw!@"):
    """
    Create a virtual machine.
    :param resource_group_name: Name of the resource group
    :param location: Azure location for the VM
    :param vm_name: Name of the virtual machine
    :param nic_id: Network Interface ID for the VM
    :param admin_username: Admin username for the VM
    :param admin_password: Admin password for the VM
    :return: VirtualMachine object
    """
    # Define the VM hardware profile (VM size)
    hardware_profile = HardwareProfile(vm_size="Standard_DS1_v2")

    # Define the VM OS profile (username, password, and other settings)
    os_profile = OSProfile(
        computer_name=vm_name,
        admin_username=admin_username,
        admin_password=admin_password
    )

    # Define the VM network profile
    network_profile = NetworkProfile(
        network_interfaces=[
            NetworkInterfaceReference(id=nic_id, primary=True)
        ]
    )

    # Define the VM storage profile (OS disk and image reference)
    storage_profile = StorageProfile(
        image_reference={
            'publisher': 'Canonical',
            'offer': '0001-com-ubuntu-server-jammy',
            'sku': '22_04-lts-gen2',
            'version': 'latest'
        },
        os_disk={
            'caching': 'ReadWrite',
            'managed_disk': {
                'storage_account_type': 'Standard_LRS'
            },
            'name': f'{vm_name}_osdisk',
            'create_option': 'FromImage'
        }
    )

    # Create the VM
    vm_parameters = VirtualMachine(
        location=location,
        os_profile=os_profile,
        hardware_profile=hardware_profile,
        network_profile=network_profile,
        storage_profile=storage_profile
    )

    creation_result = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name, vm_name, vm_parameters)

    # Wait for the VM creation to complete
    vm = creation_result.result()

    return vm