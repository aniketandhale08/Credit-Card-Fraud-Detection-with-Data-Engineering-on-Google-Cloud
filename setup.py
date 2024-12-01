import setuptools  

REQUIRED_PACKAGES = [
    'apache-beam[gcp]==2.46.0',
    'google-cloud-bigquery',
    'google-cloud-firestore',
    'google-cloud-aiplatform',
    'google-cloud-pubsub',
    'oauth2client',
    'protobuf',
    'google-api-python-client',
    'fsspec',
    'gcsfs',
    'pandas'
]


PACKAGE_NAME = 'credit_transaction'
PACKAGE_VERSION = '0.0.1'

setuptools.setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description='Credit card transaction to BQ pipeline',
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(), # Use setuptools.find_packages()
    include_package_data=True,
)
