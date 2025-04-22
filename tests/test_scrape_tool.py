import unittest
import re
from tests.support.scrape_helper import ScrapeHelper

class TestScrapeTool(unittest.TestCase):
    def setUp(self):
        self.listings = ScrapeHelper.get_listings('suumo', '静岡')

    def test_scrape_suumo_new_listing_fields(self):
        new_listing = next((l for l in self.listings if l.get('new_or_used') == 'new'), None)
        self.assertIsNotNone(new_listing, 'Should find at least one new listing')
        self.assertRegex(new_listing['suumo_id'], r'^\d+$')
        self.assertEqual(new_listing['source'], 'suumo')
        self.assertTrue(new_listing['title'])
        self.assertRegex(new_listing['url'], r'^https://suumo.jp/')
        self.assertRegex(new_listing['price'], r'万円')
        self.assertTrue(new_listing['address'])
        self.assertRegex(new_listing['station'], r'浜松')
        # area and balcony may be None for new listings
        self.assertIn(new_listing['new_or_used'], ['new'])
        self.assertTrue(new_listing['layout'])
        self.assertTrue(new_listing['built'])
        # property_name, homes_id, athome_id may be None or missing

    def test_scrape_suumo_used_listing_fields(self):
        used_listing = next((l for l in self.listings if l.get('new_or_used') == 'used'), None)
        self.assertIsNotNone(used_listing, 'Should find at least one used listing')
        self.assertRegex(used_listing['suumo_id'], r'^\d+$')
        self.assertEqual(used_listing['source'], 'suumo')
        self.assertTrue(used_listing['title'])
        self.assertRegex(used_listing['url'], r'^https://suumo.jp/')
        self.assertRegex(used_listing['price'], r'万円')
        self.assertTrue(used_listing['address'])
        self.assertRegex(used_listing['station'], r'浜松|静岡|沼津')
        self.assertRegex(used_listing['area'], r'm2')
        self.assertRegex(used_listing['layout'], r'\dLDK')
        if used_listing.get('balcony'):
            self.assertRegex(used_listing['balcony'], r'm2')
        self.assertRegex(used_listing['built'], r'\d{4}年\d{1,2}月')
        self.assertIn(used_listing['new_or_used'], ['used'])
        # property_name, homes_id, athome_id may be None or missing

if __name__ == '__main__':
    unittest.main()
