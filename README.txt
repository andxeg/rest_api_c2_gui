THIS FILE CONTAINS ALL INFORMATION ABOUT DEVELOPED REST_PROGRAM

====================================USEFUL LINKS===============================
------------------------------------REST TOOLS---------------------------------
1.  See in google flask authentication cookie
2.  See in google flask authentication and authorization
3.  Flask Basic Auth http://flask.pocoo.org/snippets/8/
4.  http://www.moserware.com/2009/06/first-few-milliseconds-of-https.html
5.  https://realpython.com/blog/python/using-flask-login-for-user-management-with-flask/
6.  !!! Json Web Tokens -> https://realpython.com/blog/python/token-based-authentication-with-flask/
7.  Flask-Login Tokens Tutorial -> http://thecircuitnerd.com/flask-login-tokens/
8.  https://habrahabr.ru/post/222983/

9.  Json Web Tokens. Good link!!!
    https://realpython.com/blog/python/token-based-authentication-with-flask/

10. Python datetime.
    How create from string datetime object -> http://stackoverflow.com/questions/466345/converting-string-into-datetime
    strptime
    Read also -> http://strftime.org/


11. Flask for production. See -> Deploying to the web-server.
    http://flask.pocoo.org/docs/0.12/quickstart/#deploying-to-a-web-server

------------------------------------OPEN_SSL-----------------------------------
1.  Generate key and crt with subjectAltNames. https://docs.oracle.com/cd/E52668_01/E66514/html/ceph-issues-24424028.html
2.  Generate key and crt with subjectAltNames. http://apetec.com/support/generatesan-csr.htm
3.  GOOD LINK. http://wiki.cacert.org/FAQ/subjectAltName
4.  GOOD LINK. http://stackoverflow.com/questions/21488845/how-can-i-generate-a-self-signed-certificate-with-subjectaltname-using-openssl
5.  GOOD LINK. http://stackoverflow.com/questions/10175812/how-to-create-a-self-signed-certificate-with-openssl/27931596#27931596
6.  GOOD LINK. https://jamielinux.com/docs/openssl-certificate-authority/sign-server-and-client-certificates.html



===============================OPEN_SSL_USEFUL_COMMANDS========================

1.  SHOW CSR-file. CSR - certificate signing request
    $ openssl req -text -noout -in cert_sign_req.csr

2.  SHOW CRT-file.
    $ openssl x509 -in self_signed.crt  -text -noout



===================================HOW_LAUNCH_REST=============================

1.  See chapters 'PYTHON' and 'OS' in requirements.txt. Install all packages.
2.  Generate certificate. See instruction below.
    HOW GENERATE SELF-SIGNED CERTIFICATE WITH subjectAltName
    PRELIMINARIES
        a.  Find openssl config file in system and copy it to your directory.
            Openssl config path example: /etc/ssl/openssl.cnf

        b.  Open config file and make some modifications.

        c.  Find [ req ], uncomment
            'req_extensions = v3_req' and
            'x509_extensions = v3_ca'
            Actually to generate the self-sigened certificate is sufficient uncomment only v3_ca.

        d.  Find [ v3_req ], add some parameters:
            subjectKeyIdentifier = hash
            basicConstraints = CA:FALSE
            keyUsage = nonRepudiation, digitalSignature, keyEncipherment
            subjectAltName = @alternate_names

        e.  Find [ v3_ca ], add some parameters:
            subjectAltName = @alternate_names

        f.  Add [ alternate_names] to the end of config file.
            [ alternate_names]
            IP.1 = 0.0.0.0
            IP.2 = 127.0.0.1
            DNS.1 = mysite.ru

        g.  Find [ CA_default ], uncomment
            'copy_extensions = copy'

    FAST METHOD
        a.  $ openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out self_signed.crt -config ./openssl.cnf
        b.  Generate without subjectAltNames:
            $ openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out self_signed.crt -subj /CN=0.0.0.0
            CN - Common Name

    SLOW METHOD
        For this method you must comment line 'keyUsage = nonRepudiation, digitalSignature, keyEncipherment' in [ v3_req ]
        a.  Create private key.
            $ openssl genrsa -out private.key 2048

        b.  Create CSR(Certificate signing request).
            $ openssl req -new -out cert_sign_req.csr -key private.key -config openssl.cnf

        c.  Create self-signed certificate.
            $ openssl x509 -req -days 365 -in cert_sign_req.csr -signkey private.key -out self_signed.crt -extensions v3_req -extfile openssl.cnf
