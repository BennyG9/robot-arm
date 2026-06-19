from setuptools import setup

package_name = 'stm32_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={
        package_name: ['protocol.json'],
    },
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bg99',
    maintainer_email='bennygoldstein99@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'stm32_interface_node = stm32_bridge.stm32_interface_node:main',
        ],
    },
)
