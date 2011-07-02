import ldap
import models

class Person:
    HOSTS = {
        'prod': 'ldap.berkeley.edu',
        'test': 'ldap-test.berkeley.edu',
        }

    BASE_DN = 'ou=people,dc=berkeley,dc=edu'

    def __init__(self, env='test'):
        if env in Person.HOSTS.keys():
            self.ldap_host = Person.HOSTS[env]
        else:
            raise ValueError("env argument must be one of 'test' or 'prod'")

    def set_ldap_host(self, host):
        if host in Person.HOSTS.values():
            self.ldap_host = host
        else:
            raise StandardError('invalid host name')

    ldap_host = property(set_ldap_host)

    def find_by_uid(self, uid):
        """Find a Person entry in LDAP by their uid:

        s = search.Person()
        p = s.find_by_uid(61065)
        p.first_name
        => 'Steven'
        p.last_name
        => 'Hansen'
        """

        conn = ldap.open(self.ldap_host)
        conn.simple_bind('', '')
        results = conn.search_s(Person.BASE_DN, ldap.SCOPE_SUBTREE, "(&(uid=%s))" % uid)
        conn.unbind()
        
        if results:
            return models.Person(results[0][1])
        return None
