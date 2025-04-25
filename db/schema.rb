# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[8.0].define(version: 2025_04_23_162322) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "pg_catalog.plpgsql"

  create_table "listings", force: :cascade do |t|
    t.string "suumo_id", null: false
    t.string "suumo_url", null: false
    t.string "raw_title"
    t.string "title"
    t.string "raw_price"
    t.integer "min_price_man_en"
    t.integer "max_price_man_en"
    t.string "raw_address"
    t.string "prefecture"
    t.string "city"
    t.string "ward"
    t.string "town"
    t.string "chome"
    t.string "block_number"
    t.string "building_number"
    t.string "building_name"
    t.string "postal_code"
    t.string "raw_station"
    t.string "station_name"
    t.string "station_line"
    t.integer "station_minutes_walk"
    t.integer "station_meters_distance"
    t.string "raw_area"
    t.integer "min_area_square_centimeters"
    t.integer "max_area_square_centimeters"
    t.string "raw_layout"
    t.string "layouts", array: true
    t.string "raw_balcony"
    t.boolean "balcony"
    t.integer "balcony_area_square_centimeters"
    t.string "raw_construction_date"
    t.integer "construction_year"
    t.boolean "construction_complete"
    t.boolean "used"
    t.datetime "refreshed_at", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["suumo_id"], name: "index_listings_on_suumo_id", unique: true, where: "(suumo_id IS NOT NULL)"
  end

  create_table "users", force: :cascade do |t|
    t.string "email", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["email"], name: "index_users_on_email", unique: true
  end
end
