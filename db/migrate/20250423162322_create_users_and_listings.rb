class CreateUsersAndListings < ActiveRecord::Migration[8.0]
  def change
    create_table :users do |t|
      t.string :email, null: false
      t.timestamps

      t.index :email, unique: true
    end

    create_table :listings do |t|
      t.string :suumo_id, null: false # 67721355
      t.string :suumo_url, null: false # https://suumo.jp/ms/shinchiku/shizuoka/sc_hamamatsushichuo/nc_67721355/

      t.string :raw_title # サンメゾン浜松元浜
      t.string :title # サンメゾン浜松元浜
      t.string :raw_price # 3530万円・3850万円
      t.integer :min_price_man_en # 3530
      t.integer :max_price_man_en # 3850
      t.string :raw_address # 浜松市中央区元浜町80番地-1
      t.string :prefecture # 静岡県
      t.string :city # 浜松市
      t.string :ward # 中央区
      t.string :town # 元浜町
      t.string :chome # null
      t.string :block_number # 80番
      t.string :building_number # 地-1
      t.string :building_name # null
      t.string :postal_code # null

      t.string :raw_station # ＪＲ東海道本線/浜松 徒歩9分
      t.string :station_name # 浜松駅
      t.string :station_line # ＪＲ東海道本線
      t.integer :station_minutes_walk # 9
      t.integer :station_meters_distance # null
      t.string :raw_area # 71.71m2～85.22m2
      t.integer :min_area_square_centimeters # 717100
      t.integer :max_area_square_centimeters # 852200
      t.string :raw_layout # 2LDK・3LDK
      t.string :layouts, array: true # {'2LDK', '3LDK'}
      t.string :raw_balcony # あり、21.55m2
      t.boolean :balcony # true
      t.integer :balcony_area_square_centimeters # 215500
      t.string :raw_construction_date # 2025年6月下旬予定
      t.integer :construction_year # 2025
      t.boolean :construction_complete # false
      t.boolean :used # false

      t.datetime :refreshed_at, null: false
      t.timestamps

      t.index :suumo_id, unique: true, where: "suumo_id IS NOT NULL"
    end
  end
end
