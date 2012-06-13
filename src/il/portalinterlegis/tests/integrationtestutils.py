from plone.app.testing import IntegrationTesting, \
     SITE_OWNER_NAME, SITE_OWNER_PASSWORD, TEST_USER_NAME, TEST_USER_PASSWORD


# browser builders code from https://dev.plone.org/ticket/11674#comment:3
# pointed from https://dev.plone.org/ticket/12373
class BrowserAwareIntegrationTesting(IntegrationTesting):

    def anonymous_browser(self):
        """Browser of anonymous
        """
        from plone.testing.z2 import Browser
        browser = Browser(self['app'])
        browser.handleErrors = False
        return browser

    def _auth_browser(self, login, password):
        """Browser of authenticated user
        """
        import base64
        browser = self.anonymous_browser()

        basic_auth = 'Basic {0}'.format(
            base64.encodestring('{0}:{1}'.format(login, password))
            )
        browser.addHeader('Authorization', basic_auth)
        return browser

    def manager_browser(self):
        """Browser of Manager
        """
        return self._auth_browser(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def member_browser(self):
        """Browser with Member authentication
        """
        return self._auth_browser(TEST_USER_NAME, TEST_USER_PASSWORD)

