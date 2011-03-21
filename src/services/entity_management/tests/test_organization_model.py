from services.entity_management.models import OrganizationModel

class TestOrganizationModel:
    def test_should_create_registration_model(self):
        org = OrganizationModel(name = 'OrgName', sector = 'OrgSector'
                                               , addressline1 = 'line1', addressline2 = 'line2'
                                               , city = 'city', state = 'state', zipcode = 'zip'
                                               , office_phone = '123-456-7890', website = 'http://twi.com'
                                               , administrators = ['admin@email.com'])
        assert org.name == 'OrgName'
        assert org.sector == 'OrgSector'
        assert org.addressline1 == 'line1'
        assert org.addressline2 == 'line2'
        assert org.city == 'city'
        assert org.state == 'state'
        assert org.zipcode == 'zip'
        assert org.office_phone == '123-456-7890'
        assert org.website == 'http://twi.com'
        assert 'admin@email.com' in org.administrators
