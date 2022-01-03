from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='pxyTools',
      packages=[
          "pxyTools"
      ],
      version='1.1.1',
      description='A collection of python tools to save time on my personal projects',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Proxymiity/pxyTools-python',
      download_url='https://github.com/Proxymiity/pxyTools-python/releases',
      changelog='https://github.com/Proxymiity/pxyTools-python/releases',
      documentation='https://github.com/Proxymiity/pxyTools-python/wiki',
      source='https://github.com/Proxymiity/pxyTools-python/tree/main/pxyTools',
      author='Proxymiity',
      author_email='dev@ayaya.red',
      license='MIT',
      install_requires=[
            'requests>=2.25.0',
            'img2pdf>=0.4.3',
            'Pillow>=8.4.0',
      ],
      classifiers=[
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Topic :: Internet',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities',
            'Intended Audience :: Developers'
      ],
      zip_safe=False,
      python_requires='>=3.7'
      )
