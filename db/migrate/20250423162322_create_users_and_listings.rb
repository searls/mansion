class CreateUsersAndListings < ActiveRecord::Migration[8.0]
  def change
    create_table :users do |t|
      t.string :email, null: false
      t.timestamps

      t.index :email, unique: true
    end

    create_table :listings do |t|
      t.string :suumo_id, null: false
      t.string :suumo_url, null: false

      t.string :raw_title # 水戸島元町（富士駅） 3560万円
      t.string :title
      t.string :price_description
      t.integer :price_man_en
      t.string :address_description # 浜松市中央区元浜町80番地-1
      t.string :prefecture
      t.string :city
      t.string :ward
      t.string :town
      t.string :chome
      t.string :block_number
      t.string :building_number
      t.string :building_name
      t.string :postal_code

      t.string :station_description # ＪＲ東海道本線/浜松 徒歩9分
      t.integer :station_minutes_walk
      t.integer :station_meters_distance
      t.string :area_description # 71.71m2～85.22m2
      t.integer :area_square_centimeters # 784600
      t.string :layout_description # 2LDK・3LDK
      t.string :balcony_description
      t.string :construction_date_description # 2025年6月下旬予定
      t.integer :construction_year
      t.boolean :construction_complete
      t.boolean :used

      t.datetime :refreshed_at, null: false
      t.timestamps

      t.index :suumo_id, unique: true, where: "suumo_id IS NOT NULL"
    end
  end
end
