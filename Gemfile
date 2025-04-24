source "https://rubygems.org"

ruby "~> 3.4.1"

gem "rails"

# Model stuff
gem "pg"

# Networking stuff
gem "puma"
gem "rack-cors", require: "rack/cors"

# Background stuff
gem "solid_queue"
gem "actioncable-enhanced-postgresql-adapter"

# Scraping stuff
gem "httparty"
gem "nokogiri"

# Engine stuff
gem "mission_control-jobs"
gem "searls-auth"

# Frontend stuff
gem "propshaft"
gem "importmap-rails"
gem "turbo-rails"
gem "stimulus-rails"
gem "tailwindcss-rails"

# Handy stuff
gem "bootsnap", require: false

group :development, :test do
  gem "debug", platforms: %i[mri windows], require: "debug/prelude"
  gem "dotenv-rails"
  gem "good_migrations"

  gem "standard", require: false
  gem "standard-rails", require: false
  gem "brakeman", require: false

  gem "awesome_print"
end

group :development do
  gem "web-console"
  gem "letter_opener"
end

group :test do
  gem "capybara"
  gem "capybara-playwright-driver"
  gem "mocktail"
  gem "simplecov", require: false
end

group :production do
  gem "honeybadger"
end
