from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

print(find_packages(where='euler_angle_visualization'))

setup(
    name='Euler angle visualization',
    url='https://github.com/klosteraner/Euler-Angles-Visual',
    author='klosteraner',
    author_email='martin.zaenker@mailbox.org',
    description='The app visualizes various rotation conventions, in particular different Euler angle conventions.',
    license='MIT',
    packages=find_packages(where='euler_angle_visualization'),
    package_dir={'': 'euler_angle_visualization'},
    py_modules=['euler_angle_visualization'],
    entry_points={
        'console_scripts': [
            'euler_angle_visualization=euler_angle_visualization:run',
        ],
    },
    install_requires=['mayavi', 'numpy', 'vtk', 'pyface', 'PyQt5'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent'
    ]
)
