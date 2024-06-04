import os
import subprocess


def generate_cert_and_key(certfile, keyfile):
    # Generate private key
    subprocess.run(['openssl', 'genpkey', '-algorithm', 'RSA', '-out', keyfile], check=True)
    # Create certificate signing request (CSR)
    subprocess.run(['openssl', 'req', '-new', '-key', keyfile, '-out', 'cert.csr', '-subj', '/CN=localhost'], check=True)
    # Generate self-signed certificate
    subprocess.run(['openssl', 'x509', '-req', '-days', '365', '-in', 'cert.csr', '-signkey', keyfile, '-out', certfile], check=True)
    # Clean up CSR file
    os.remove('cert.csr')


def check_and_generate_cert_and_key(certfile, keyfile):
    if not os.path.exists(certfile) or not os.path.exists(keyfile):
        print("Certificate or key file not found, generating new ones...")
        generate_cert_and_key(certfile, keyfile)
    else:
        print("Certificate and key files exist.")


if __name__ == "__main__":
    certfile = 'certfile.pem'
    keyfile = 'keyfile.pem'
    check_and_generate_cert_and_key(certfile, keyfile)
    print(f"Certificate file: {certfile}")
    print(f"Key file: {keyfile}")
