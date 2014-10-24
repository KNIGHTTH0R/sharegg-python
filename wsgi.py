import os

from sharegg.server import app as application, run

if __name__ == '__main__':

    ip = os.environ.get('OPENSHIFT_PYTHON_IP', '0.0.0.0')
    port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8051))

    application.config['PROPAGATE_EXCEPTIONS'] = True

    run(ip, port)