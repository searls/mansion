require "application_system_test_case"

class SuumoTest < ApplicationSystemTestCase
  Capybara.always_include_port = false

  def test_known_suumo_used_link_still_works
    visit "https://suumo.jp/jj/bukken/ichiran/JJ012FC001/?ar=050&bs=011&md=2&md=3&md=4&md=5&et=10&fw=静岡&po=16&pj=2&pc=100&cnb=0&cn=10"

    assert_equal "100", find('select[name="pc"]', match: :first).value
    assert_equal "&po=16&pj=2", find("#js-sortbox").value # by construction year descending
  end

  def test_known_suumo_new_link_still_works
    visit "https://suumo.jp/jj/bukken/ichiran/JJ011FC001/?ar=050&bs=010&tj=0&po=5&pj=1&pc=100&fw=静岡&md=2&md=3&md=4&md=5"

    assert_equal "100", find('select[name="pc"]', match: :first).value
    assert_equal "51", find("#js-sortbox-sortPulldown").value # by price ascending
  end
end
