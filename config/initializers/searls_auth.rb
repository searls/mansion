Rails.application.config.after_initialize do
  Searls::Auth.configure do |config|
    config.app_name = "Mansion"
  end
end
