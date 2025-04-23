# Add your own tasks in files placed in lib/tasks ending in .rake,
# for example lib/tasks/capistrano.rake, and they will automatically be available to Rake.

require_relative "config/application"

if Rails.env.production?
  require "honeybadger/init/ruby"
  Honeybadger.install_at_exit_callback
end

Rails.application.load_tasks

unless Rails.env.production?
  require "standard/rake"
  task :default do
    ENV["CI"] = "true"
    Rake::Task["standard:fix"].invoke
    Rake::Task["test"].invoke
    Rake::Task["test:system"].invoke
  end
end
