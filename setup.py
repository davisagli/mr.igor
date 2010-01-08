from setuptools import setup, find_packages

version = '1.2'

setup(name='mr.igor',
      version=version,
      description="Mr. Igor provides the parts you need to build your Frankenprogram.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
        ],
      keywords='python imports automatic',
      author='David Glick',
      author_email='dglick@gmail.com',
      url='http://github.com/davisagli/mr.igor',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mr'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pyflakes',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [console_scripts]
      igor = mr.igor:main
      """,
      )
