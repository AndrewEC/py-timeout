from setuptools import setup

if __name__ == '__main__':
    setup(
        name='timeout',
        version='1.0',
        description='Utility to invoke a function with a timeout.',
        author='Andrew Cumming',
        author_email='andrew.e.cumming@gmail.com',
        url='https://github.com/AndrewEC/py-timeout-util',
        packages=['timeout', 'timeout.lib']
    )
