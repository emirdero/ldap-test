import ldap3

login_info = {
    'username': "Joe",
    'password': "password123"
}

settings = {
    'name': "Ldap",
    'host': 'example.ldap.com',
    'port': 389,
    'encryption': 'none',
    'base_dn': "dc=ldap,dc=com",
    'request': "(uid={})",
    'prefix': "",
    'require_cert': True


}

login = login_info["username"].strip().lower()
login_dn = 'uid=' + login + ',ou=people,' + settings['base_dn']
password = login_info["password"]

if password.rstrip() == "":
    print("empty password!")

try:
    # Connect to the ldap
    print("connection to ldap")
    server = ldap3.Server(settings['host'], port=settings['port'], use_ssl=settings["encryption"] == 'ssl', get_info=ldap3.ALL)
    conn = ldap3.Connection(server, user=login_dn, password=password, auto_bind='NONE', version=3, authentication='SIMPLE', client_strategy='SYNC', auto_referrals=True, check_names=True, read_only=False, lazy=False, raise_exceptions=False)
    conn.start_tls()
    if not conn.bind():
        print("ERROR ", conn.result)
    # Start TLS
    # conn.start_tls()
    print("Connected")
except Exception as e:
    print("Can't initialze connection to " + settings['host'] + ': ' + str(e))
    exit(0)

try:
    request = settings["request"].format(login)
    conn.search(settings["base_dn"], request, attributes=["cn", "mail"])
    print("RESPONSE: ")
    print(conn.response)
    response = conn.response
except Exception as ex:
    print("Can't get user data : " + str(ex))
    conn.unbind()
try:
    for entry in response:
        if entry["attributes"]["mail"] != []:
            print(entry['dn'])
            email = entry["attributes"]["mail"][0]
            username = login
            realname = entry["attributes"]["cn"][0]
            print(email)
            print(username)
            print(realname)
            break
    conn.unbind()
except KeyError as e:
    print("Can't get field " + str(e) + " from your LDAP server")
except Exception as e:
    print("Can't get some user fields")
    print(e)
