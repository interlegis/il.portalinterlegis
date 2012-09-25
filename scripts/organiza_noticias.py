from DateTime import DateTime
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser

class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return self.getUserName()

tmp_user = UnrestrictedUser(old_sm.getUser().getId(), '', ['Manager'], '')
tmp_user = tmp_user.__of__(portal.acl_users)
newSecurityManager(None, tmp_user)


todas_noticias = portal.portal_catalog(portal_type='News Item')
noticias = portal.noticias

for brain in todas_noticias:
    obj = brain.getObject()
    data = DateTime(obj.creation_date)
    ano, mes = str(data.year()), '%02d' % data.month()

    if ano not in noticias:
        noticias.invokeFactory('Folder', id=ano, title=ano)
    noticias_ano = noticias[ano]

    if mes not in noticias_ano:
        noticias_ano.invokeFactory('Folder', id=mes, title=mes)

    ref = obj.aq_parent.manage_cutObjects(brain.id)
    noticias_ano[mes].manage_pasteObjects(ref)

    print obj

import transaction
transaction.commit()

