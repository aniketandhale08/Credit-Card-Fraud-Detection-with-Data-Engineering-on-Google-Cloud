import setuptools

REQUIRED_PACKAGES = ['gcsfs','fsspec','google-cloud-bigquery','firestore','google-cloud-aiplatform','protobuf==4.23.4']
#REQUIRED_PACKAGES = ['gcsfs','fsspec','google-cloud-bigquery','pandas','openpyxl']
PACKAGE_NAME = 'credit_transation'
PACKAGE_VERSION = '0.0.1'
setuptools.setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description='credit card transaction to BQ Dependency Packages',
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
)

