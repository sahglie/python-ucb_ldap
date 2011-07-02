import re

class Person:
    """Represents a Person object from the UC Berkeley LDAP people
       container

       ou=people,dc=berkeley,dc=edu"""

    def __init__(self, attributes = {}):
        """Expects a dictionary containing the attributes returned
        from a single LDAP person entry.  Required attributes include:
        ['sn', 'givenname', 'uid', 'mail']

        The following is a sample dictionary containing all the attributes 
        returned from and ldap query.

        {'cn': ['Hansen, Steven A', 'HANSEN, STEVEN', 'HANSEN, STEVE ANTONE'], 
        'objectClass': ['top', 'person', 'organizationalperson', 'inetorgperson', 
                        'berkeleyEduPerson', 'eduPerson', 'ucEduPerson'], 
        'street': ['Banway, Room 547A'], 
        'berkeleyEduUnitCalNetDeptName': ['IST-Application Services'], 
        'berkeleyEduMiddleName': ['A'], 
        'uid': ['61065'], 
        'title': ['Programmer / Analyst'], 
        'berkeleyEduModDate': ['20110630172046Z'], 
        'berkeleyEduMaxExpDate': ['20110529232442Z'], 
        'postalCode': ['94720-4870'], 
        'mail': ['runner@berkeley.edu'], 
        'postalAddress': ['Banway, Room 547A$Berkeley, CA 94720-4870'], 
        'departmentNumber': ['JKASD'], 
        'berkeleyEduDeptUnitHierarchyString': ['UCBKL-AVCIS-VRIST-JKASD'], 
        'telephoneNumber': ['+1 510 508-1888'], 
        'displayName': ['Steven A Hansen'], 
        'l': ['Berkeley'], 
        'o': ['University of California, Berkeley'], 
        'st': ['CA'], 
        'berkeleyEduPrimaryDeptUnitHierarchyString': ['UCBKL-AVCIS-VRIST-JKASD'], 
        'berkeleyEduUnitHRDeptName': ['Application Services'], 
        'sn': ['Hansen'], 
        'ou': ['people'], 
        'givenName': ['Steven', 'Steven A', 'STEVE ANTONE'], 
        'berkeleyEduPrimaryDeptUnit': ['JKASD'], 
        'berkeleyEduAffiliations': ['STUDENT-STATUS-EXPIRED', 
                                    'AFFILIATE-TYPE-ADVCON-ATTENDEE', 
                                    'EMPLOYEE-TYPE-STAFF']}
        """
        for attr in attributes.keys():
            setattr(self, self.__class__.__normalize(attr), attributes[attr])

        if hasattr(self, 'uid'):
            self.uid = self.uid[0]

    def get_first_name(self):
        return self.given_name[0]

    def get_last_name(self):
        return self.sn[0]

    def get_email(self):
        return self.mail[0]

    first_name = property(get_first_name)
    last_name = property(get_last_name)
    email = property(get_email)

    @staticmethod
    def __normalize(string):
        """Changes a camel case string to snake case:

        Person.__to_underscore("camelCaseMethod")
        => 'camel_case_method'
        """
        string = string.replace("berkeleyEdu", "")
        iter = re.finditer(r'[A-Z]?[a-z]+', string)
        new_str = ""
        for i in iter:
            new_str += "%s_" % i.group()
        
        return new_str[0:-1].lower()
        
    def __str__(self):
        atts = ('uid', self.uid,
                'first_name', self.first_name,
                'last_name', self.last_name,
                'email', self.email)
        return "<models.Person {%s: %s, %s: %s, %s: %s, %s: %s}>" % atts
