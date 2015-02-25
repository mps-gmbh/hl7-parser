from setuptools import setup, find_packages

setup(
    name='hl7parser',
    version='0.5.1',
    description='A simple HL7 parser',
    url='https://github.com/mps-gmbh/hl7-parser',
    author='Medizinische Planungssysteme GmbH',
    license='BSD',
    packages=find_packages(),
    test_suite='hl7parser.tests',
    zip_safe=True,
    classifiers=[
        'License :: OSI Approved :: BSD License',
    ],
)
