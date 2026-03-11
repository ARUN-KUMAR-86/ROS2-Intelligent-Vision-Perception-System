from setuptools import find_packages, setup

package_name = 'ros_camera_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    ('share/' + package_name + '/launch', ['launch/vision_launch.py']),
    ('share/' + package_name + '/models',
        ['models/haarcascade_frontalface_default.xml']),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='arun',
    maintainer_email='arunsivakumar@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'camera_node = ros_camera_vision.camera_node:main',
        'vision_node = ros_camera_vision.vision_node:main',
    ],
},
)
