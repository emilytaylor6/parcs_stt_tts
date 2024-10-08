from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'parcs_tts'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'action'), glob('action/*.action')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hello-robot',
    maintainer_email='emilytaylorr22@gmail.com',
    description='A text to speech node.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'parcs_tts = parcs_tts.parcs_tts:main',
            'parcs_tts_test = parcs_tts.parcs_tts_test:main',
            'tts_tester = parcs_tts.tts_tester:main',
        ],
    },
)
