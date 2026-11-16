import datetime as dt, unittest
from tool import expiry_status
class CertTests(unittest.TestCase):
    def test_expiry_bands(self):
        now=dt.datetime(2026,1,1,tzinfo=dt.timezone.utc)
        self.assertEqual(expiry_status("Jan 02 00:00:00 2026 GMT",now)["status"],"critical")
        self.assertEqual(expiry_status("Feb 15 00:00:00 2026 GMT",now)["status"],"soon")
        self.assertEqual(expiry_status("May 01 00:00:00 2026 GMT",now)["status"],"okay")
    def test_expired(self):
        now=dt.datetime(2026,1,2,tzinfo=dt.timezone.utc)
        self.assertEqual(expiry_status("Jan 01 00:00:00 2026 GMT",now)["status"],"expired")
if __name__=="__main__": unittest.main()
